# The Files for Freedom Toolkit

Support free access to information using nothing more than your existing web server and a one-liner.

To learn about the mission behind the Files for Freedom movement, and to see a live demo, visit (files-for-freedom.web.app)[https://files-for-freedom.web.app/]

## How it works


----
## How to use it
pdf_encoder.py [pdf to encode] [downloader name]

### Outputs description
**downloader .html file:**
 * This file will be what the user visits in order to download the [pdf to encode]
 * Will also have name given [downloader name]

**reader .html file:**
 * This file is what the downloaders will redirect to, to read the pdf's they have in cache
 * Will have basic controls for seeing whats there, viewing, and deleting content
 * This is also the page that will be cached, so the user can come back to this page offline
 * The user can also come back to the website has been taken down, as long as the cache doesn't get cleared or updated

**service-worker.js:**
 * makes sure that the reader .html file gets cached

**.readerName:**
 * holds the name of the reader .html
 * so that there aren't many readers but just one

----
### Outputs file paths
#### All public files need to be served
#### .readerName is **not** served
public/[downloader].html
public/[randomstring readerfile].html
public/service-worker.js
.readerName