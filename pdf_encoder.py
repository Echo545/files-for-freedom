#!/usr/bin/python3
import base64
import argparse
import os
import zlib

html_template = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>{pdf_name}</title>
</head>
<body>
  <h1>{pdf_name}</h1>

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
      const inflatedPdfData = atob(pdfData);
      const byteArray = new Uint8Array(inflatedPdfData.length);
      for (let i = 0; i < inflatedPdfData.length; i++) {{
          byteArray[i] = inflatedPdfData.charCodeAt(i);
      }}
      const blob = new Blob([byteArray], {{ type: 'application/pdf' }});
      const pdfFile = new File([blob], pdfName, {{ type: 'application/pdf' }});

      savePDF(pdfFile)
    }};

    dbPromise.onerror = function(event) {{
      console.error('Error opening IndexDB');
    }};

    function savePDF(pdfFile) {{
    const dbName = 'pdfDatabase';
    const storeName = 'pdfStore';
    const dbVersion = 1;

    const dbPromise = indexedDB.open(dbName, dbVersion);

    dbPromise.onupgradeneeded = function(event) {{
        const db = event.target.result;
        const upgradeDb = event.target.result;
        upgradeDb.createObjectStore(storeName);
    }};

    dbPromise.onsuccess = function(event) {{
        const db = event.target.result;
        const tx = db.transaction([storeName], 'readwrite');
        const store = tx.objectStore(storeName);
        const pdfKey = Math.random().toString(36).substr(2, 9);
        const addRequest = store.put({{key: pdfKey, file: pdfFile}});

        addRequest.onsuccess = function(event) {{
            console.log('PDF file added to IndexDB');
            console.log('PDF key: ' + pdfKey);
        }};

        addRequest.onerror = function(event) {{
            console.error('Error adding PDF file to IndexDB');
        }};
    }};

    dbPromise.onerror = function(event) {{
        console.error('Error opening IndexDB');
    }};
}}

  </script>
</body>
</html>
"""

def embed_pdf_in_html(pdf_file_path):
    with open(pdf_file_path, 'rb') as f:
        pdf_data = f.read()

    compressed_pdf_data = zlib.compress(pdf_data)
    base64_pdf_data = base64.b64encode(compressed_pdf_data).decode()

    pdf_name = os.path.basename(pdf_file_path)
    html_data = html_template.format(pdf_name=pdf_name, pdf_data=base64_pdf_data)
    with open('embedded_pdf.html', 'w') as f:
        f.write(html_data)

    print(f'PDF embedded in HTML file: embedded_pdf.html')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Embed PDF in HTML and store in IndexDB')
    parser.add_argument('pdf_file', type=str, help='Path to PDF file')
    args = parser.parse_args()

    embed_pdf_in_html(args.pdf_file)
