#!/usr/bin/python3
import base64
import argparse
import os
import random
import string
import zlib

download_template = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Downloader</title>
</head>
<body>
  <style>
    h1 {{
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
    }}
  </style>

  <h1>Download in Progress...</h1>

  <script>
    const dbName = 'pdfDatabase';
    const storeName = 'pdfStore';
    const dbVersion = 2;

    const dbPromise = indexedDB.open(dbName, dbVersion);

    dbPromise.onupgradeneeded = function(event) {{
      const db = event.target.result;
      const upgradeDb = event.target.result;
      const objectStore = upgradeDb.createObjectStore(storeName, {{ keyPath: 'id', autoIncrement: true }});
    }};

    dbPromise.onsuccess = function(event) {{
      const db = event.target.result;
      const tx = db.transaction([storeName], 'readwrite');
      const store = tx.objectStore(storeName);
      const pdfName = '{pdf_name}';
      const pdfData = '{pdf_data}';
      const pdfFile = b64toPDF(pdfData, pdfName, 'application/pdf')

      const addRequest = store.add({{file: pdfFile}});

      addRequest.onsuccess = function(event) {{
          console.log('PDF file added to IndexDB');
          console.log(addRequest)
          console.log(event)
          tx.oncomplete = function() {{
            toReader();
          }};
      }};

      addRequest.onerror = function(event) {{
          console.error('Error adding PDF file to IndexDB');
          console.log(event)
      }};
    }};

    dbPromise.onerror = function(event) {{
      console.error('Error opening IndexDB');
      console.log(event)
    }};

    function toReader() {{
      window.location.href = '{reader_name}.html';
    }};

    function b64toPDF(b64Data, pdfName, contentType = 'application/pdf') {{
        const byteCharacters = atob(b64Data);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {{
            byteNumbers[i] = byteCharacters.charCodeAt(i);
        }};
        const byteArray = new Uint8Array(byteNumbers);
        const blob = new Blob([byteArray], {{ type: contentType }});
        const pdfFile = new File([blob], pdfName, {{ type: contentType }});
        return pdfFile;
    }};
  </script>
</body>
</html>
"""

reader_template = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css">
    <title>Reader</title>
  </head>
  <body>

    <style>
      .container {{
        display: flex;
        flex-direction: column;
        justify-content: center;
      }}

      .container > * {{
        margin: 2px;
        text-align: center;
      }}

      .inlineview {{
        margin-left: 15px;
      }}

      #table-of-contents {{
        margin: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
      }}

      .btn {{
        max-width: 200px;
        margin: 0 auto;
      }}

      #refresh {{
        margin-bottom: 5px;
        margin-top:5px;
      }}
    </style>

    <div class="container">

      <h1>My Reading List</h1>
      <hr>

      <p>Bookmark this page and come back anytime for offline reading of all saved documents.</p>
      <p>Clearing your cache will delete all documents and the offline version of this page.</p>

      <button class="btn btn-primary" id="refresh" onclick="displayTableOfContents()">Refresh</button>
      <button class="btn btn-danger" onclick="deleteAll()">Delete All</button>

      <h5 style="margin-top: 25px">Available Documents</h5>
      <hr>

      <div id="table-of-contents"></div>
      <div id="pdf-display"></div>

    </div>

    <script src="https://cdn.jsdelivr.net/pako/1.0.3/pako.min.js"></script>
    <script>

      // Create a new database and object store
      const dbName = 'pdfDatabase';
      const storeName = 'pdfStore';
      const pageName = 'pages';
      const dbPromise = window.indexedDB.open(dbName, 2);

      dbPromise.onsuccess = function(event) {{
        displayTableOfContents();
      }}

      dbPromise.onupgradeneeded = function(event) {{
        const db = event.target.result;
        db.objectStoreNames.contains(storeName) || db.createObjectStore(storeName, {{keyPath: 'id', autoIncrement: true}});
        db.objectStoreNames.contains(pageName) || db.createObjectStore(pageName, {{keyPath: 'url'}});
      }}

      // Display the table of contents
    function displayTableOfContents() {{
        const db = dbPromise.result;
        const tx = db.transaction([storeName], 'readonly');
        const store = tx.objectStore(storeName);
        const getRequest = store.getAll();

        getRequest.onsuccess = function(event) {{
            const pdfFiles = event.target.result;
            if (pdfFiles.length === 0) {{
              console.log('No PDF files found in IndexDB');
              return;
            }}

            const tableOfContents = document.getElementById('table-of-contents');
            const table = document.createElement('table');

            pdfFiles.forEach(function(pdfFile) {{
            const tableRow = document.createElement('tr');
            const tableCell1 = document.createElement('td');
            const tableCell2 = document.createElement('td');
            const tableCell3 = document.createElement('td');
            const viewButton = document.createElement('button');
            viewButton.className = 'btn btn-info btn-sm inlineview';
            const deleteButton = document.createElement('button');
            deleteButton.className = 'btn btn-danger btn-sm';
            tableCell1.textContent = pdfFile.file.name;
            viewButton.textContent = 'View';
            viewButton.addEventListener('click', function() {{
                displayPDF(pdfFile);
            }});
            deleteButton.textContent = 'Delete';
            deleteButton.addEventListener('click', function() {{
                deletePDF(pdfFile);
            }});
            tableCell2.appendChild(viewButton);
            tableCell3.appendChild(deleteButton);
            tableRow.appendChild(tableCell1);
            tableRow.appendChild(tableCell2);
            tableRow.appendChild(tableCell3);
            table.appendChild(tableRow);
            }});

            tableOfContents.innerHTML = '';
            tableOfContents.appendChild(table);

            const pdf_view = document.getElementById('pdf-display');
            pdf_view.innerHTML = '';
        }};

        getRequest.onerror = function(event) {{
            console.log('No PDFs in IndexDB');
        }};
    }}

    function deletePDF(pdfFile) {{
        const db = dbPromise.result;
        const tx = db.transaction([storeName], 'readwrite');
        const store = tx.objectStore(storeName);
        store.delete(pdfFile.id);
        tx.oncomplete = function() {{
            console.log(`PDF file '${{pdfFile.file.name}}' deleted from IndexDB`);
            // remove all rows from table of contents
            const tableOfContents = document.getElementById('table-of-contents');
            tableOfContents.innerHTML = '';
            displayTableOfContents();
        }};
        tx.onerror = function(event) {{
            console.log(`Error deleting PDF file '${{pdfFile.file.name}}' from IndexDB`);
        }};
    }}

    function deleteAll() {{
        const db = dbPromise.result;
        const tx = db.transaction([storeName], 'readwrite');
        const store = tx.objectStore(storeName);
        const clearRequest = store.clear();

        clearRequest.onsuccess = function(event) {{
            console.log('All PDF files deleted from IndexDB');

            // remove all rows from table of contents
            const tableOfContents = document.getElementById('table-of-contents');
            tableOfContents.innerHTML = '';
        }};
    }}

    function displayPDF(pdfFile) {{
        const pdfDisplay = document.getElementById('pdf-display');
        pdfDisplay.innerHTML = '';

        const fileReader = new FileReader();

        fileReader.onload = function() {{
            const pdfData = new Uint8Array(this.result);
            var deflate = window.pako.inflate(pdfData)
            const blob = new Blob([deflate], {{ type: 'application/pdf' }});
            const url = URL.createObjectURL(blob);

            const embed = document.createElement('object');
            embed.setAttribute('data', url);
            embed.setAttribute('type', 'application/pdf');
            embed.setAttribute('width', '100%');
            embed.setAttribute('height', '800px');
            pdfDisplay.appendChild(embed);
        }};

        fileReader.readAsArrayBuffer(pdfFile.file);
    }}

    </script>
    </body>
</html>
"""

def embed_pdf_in_html(pdf_file_path, downloader_name):
    reader_name = None

    # Make public dir if not exists
    if not os.path.exists('public'):
        os.mkdir('public')

    # Load reader_name if exists
    if os.path.exists('.readerName'):
        with open('.readerName', 'r') as f:
            reader_name = f.read()
    else:
      # Create a new reader_name and save it to .readerName
      reader_name = generate_reader_name()
      with open('.readerName', 'w') as f:
          f.write(reader_name)

    with open(pdf_file_path, 'rb') as f:
        pdf_data = f.read()

    compressed_pdf_data = zlib.compress(pdf_data)
    base64_pdf_data = base64.b64encode(compressed_pdf_data).decode()

    pdf_name = os.path.basename(pdf_file_path)
    html_data = download_template.format(pdf_name=pdf_name, pdf_data=base64_pdf_data, reader_name=reader_name)

    # Save downloader page
    with open(f'public/{downloader_name}.html', 'w') as f:
        f.write(html_data)

    # Save reader page if not exists
    if not os.path.exists(f'public/{reader_name}.html'):
      with open(f'public/{reader_name}.html', 'w') as f:
          f.write(reader_template.format())
      print(f'Reader created: public/{reader_name}.html')
    else:
        print(f'Existing reader: public/{reader_name}.html')

    print(f'New downloader created: public/{downloader_name}.html')


def generate_reader_name():
    random_length = random.randint(6, 20)
    random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=random_length))
    return f"{random_chars}"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Embed PDF in HTML and store in IndexDB')
    parser.add_argument('pdf_file', type=str, help='Path to PDF file')
    parser.add_argument('downloader_name', type=str, help='The filename for the downloader page')
    args = parser.parse_args()

    embed_pdf_in_html(args.pdf_file, args.downloader_name)
