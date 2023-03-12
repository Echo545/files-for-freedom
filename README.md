# The Files for Freedom Toolkit

Support free access to information using nothing more than your existing web server and a one-liner.

To learn about the mission behind the Files for Freedom movement, and to see a live demo, visit (files-for-freedom.web.app)[https://files-for-freedom.web.app/]

## How it works
### Host:
![dev dia](imgs/jamdev.jpg)
* Dev runs the python script for each pdf, it generates each _/[download].html_ and a single _/[reader].html_
* All the dev has to do is put those files in a secret directory hosted on their website, or root

### User:
![user dia](imgs/jamuser.jpg)
* User will go to a _/[download].html_ (which they know by word of mouth) and on that page the pdf will be put into cache
* Then it will redirect the user to the _/[reader].html_ page

----
## How to use it
```python3 pdf_encoder.py [pdf to encode] [downloader name]```

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