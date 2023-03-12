#!/usr/bin/python3
import base64
import argparse
import os
import random
import string
import zlib

html_template = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Downloader</title>
</head>
<body>
  <h1>Download in Progress...</h1>

  <script>
    const dbName = 'pdfDatabase';
    const storeName = 'pdfStore';
    const dbVersion = 1;

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
      }};
    }};

    dbPromise.onerror = function(event) {{
      console.error('Error opening IndexDB');
    }};

    dbPromise.onerror = function(event) {{
        console.error('Error opening IndexDB');
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
    <title>PDF Upload and Storage</title>

    <script>
      if ('serviceWorker' in navigator) {{
        console.log('Found service worker')
        window.addEventListener('load', function() {{
          navigator.serviceWorker.register('/service-worker.js');
        }});
      }}
    </script>

  </head>
  <body>
    <h1>PDF Upload and Storage</h1>
    <input type="file" id="pdf-file-input">
    <button onclick="savePage()">Save Page to DB</button>
    <button onclick="savePDF()">Save PDF to IndexDB</button>
    <button onclick="displayTableOfContents()">Display Table of Contents</button>
    <button onclick="deleteAll()">Delete All</button>
    <div id="table-of-contents"></div>
    <div id="pdf-display"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.10.377/pdf.min.js"></script>
    <script src="https://cdn.jsdelivr.net/pako/1.0.3/pako.min.js"></script>
    <script>

      // Create a new database and object store
      const dbName = 'pdfDatabase';
      const storeName = 'pdfStore';
      const pageName = 'pages';
      const dbPromise = window.indexedDB.open(dbName, 2);

      dbPromise.onupgradeneeded = function(event) {{
        const db = event.target.result;
        db.objectStoreNames.contains(storeName) || db.createObjectStore(storeName, {{keyPath: 'id', autoIncrement: true}});
        db.objectStoreNames.contains(pageName) || db.createObjectStore(pageName, {{keyPath: 'url'}});
      }}

      function savePage(page) {{
        const db = dbPromise.result;
        var html = document.documentElement.innerHTML;
        var page = {{url: 'reader.html', html: html}};
        const transaction = db.transaction([pageName], 'readwrite');
        const objectStore = transaction.objectStore(pageName);
        const saveRequest = objectStore.add(page);

        saveRequest.onsuccess = function(event) {{
          console.log('PDF saved to IndexDB');
        }};

        saveRequest.onerror = function(event) {{
          console.error('Error saving page to IndexDB');
        }};

        transaction.oncomplete = function(event) {{
          console.log('Transaction complete');
        }};
      }}

      // Save the PDF to IndexDB
      function savePDF() {{
        const pdfFileInput = document.getElementById('pdf-file-input');
        const pdfFile = pdfFileInput.files[0];
        const db = dbPromise.result;
        const tx = db.transaction([storeName], 'readwrite');
        const store = tx.objectStore(storeName);
        const saveRequest = store.add({{file: pdfFile}});

        saveRequest.onsuccess = function(event) {{
          console.log('PDF saved to IndexDB');
        }};

        saveRequest.onerror = function(event) {{
          console.error('Error saving PDF to IndexDB');
        }};

        tx.oncomplete = function(event) {{
          console.log('Transaction complete');
        }};
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
            console.error('No PDF files found in IndexDB');
            return;
            }}

            const tableOfContents = document.getElementById('table-of-contents');
            const table = document.createElement('table');
            const headerRow = document.createElement('tr');
            const headerCell1 = document.createElement('th');
            const headerCell2 = document.createElement('th');
            const headerCell3 = document.createElement('th');
            headerCell1.textContent = 'PDF Name';
            headerCell2.textContent = 'View PDF';
            headerCell3.textContent = 'Delete PDF';
            headerRow.appendChild(headerCell1);
            headerRow.appendChild(headerCell2);
            headerRow.appendChild(headerCell3);
            table.appendChild(headerRow);

            pdfFiles.forEach(function(pdfFile) {{
            const tableRow = document.createElement('tr');
            const tableCell1 = document.createElement('td');
            const tableCell2 = document.createElement('td');
            const tableCell3 = document.createElement('td');
            const viewButton = document.createElement('button');
            const deleteButton = document.createElement('button');
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
        }};

        getRequest.onerror = function(event) {{
            console.error('Error getting PDFs from IndexDB');
        }};
    }}

    function deletePDF(pdfFile) {{
        const db = dbPromise.result;
        const tx = db.transaction([storeName], 'readwrite');
        const store = tx.objectStore(storeName);
        store.delete(pdfFile.id);
        tx.oncomplete = function() {{
            console.log(`PDF file '${{pdfFile.file.name}}' deleted from IndexDB`);
            displayTableOfContents();
        }};
        tx.onerror = function(event) {{
            console.error(`Error deleting PDF file '${{pdfFile.file.name}}' from IndexDB`);
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
            console.log(pdfData.length)
            var deflate = window.pako.inflate(pdfData)
            console.log(deflate.length)
            const blob = new Blob([deflate], {{ type: 'application/pdf' }});
            const url = URL.createObjectURL(blob);

            console.log(url);

            const embed = document.createElement('embed');
            embed.setAttribute('src', url);
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
    html_data = html_template.format(pdf_name=pdf_name, pdf_data=base64_pdf_data, reader_name=reader_name)

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
