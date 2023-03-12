# The Files for Freedom Toolkit

Support free access to information using nothing more than your existing web server and a one-liner.

To learn about the mission behind the Files for Freedom movement, the technical details, and to see a live demo, visit [files-for-freedom.web.app](https://files-for-freedom.web.app/)

## Usage
```python3 pdf_encoder.py [pdf to encode] [downloader page name]```

## How it works
### Host:
![dev dia](imgs/jamdev.jpg)
* Run the python tool for each target pdf. The tool generates a _/[downloader page].html_ and a single _/[reader].html_
* Then all the host has to do is put the newly generated HTML in their web server and share the URL.

### User:
![user dia](imgs/jamuser.jpg)
* User visits _/[downlaoder page].html_  and on that page the pdf will be saved in their indexDB cache
* Then it will redirect the user to the _/[reader].html_ page where all the saved PDF's can be easy read and managed.

----
### Outputs description
**downloader .html file:**
 * This file will be what the user visits in order to download the [pdf to encode]
 * Will also have name given [downloader name]

**reader .html file:**
 * This file is what the downloaders will redirect to, to read the pdf's they have in cache
 * Will have basic controls for seeing whats there, viewing, and deleting content
 * This is also the page that will be cached, so the user can come back to this page offline
 * The user can also come back to the website has been taken down, as long as the cache doesn't get cleared or updated


**.readerName:**
 * holds the name of the reader .html
 * so that there aren't many readers but just one

----
### Outputs file paths
#### All public files need to be served
#### Do **not** serve the .readerName
* public/[downloader].html
* public/[randomstring readerfile].html
* .readerName