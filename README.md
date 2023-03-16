# The Files for Freedom Toolkit

Support free access to information using nothing more than your existing web server and a one-liner.

To learn about the mission behind the Files for Freedom, the technical details, and to see a live demo, visit [files-for-freedom.web.app](https://files-for-freedom.web.app/)

## Usage
```python3 pdf_encoder.py [pdf to encode] [name for downloader page]```

## How it works
### Host:
![dev dia](imgs/jamdev.jpg)
* The host runs `pdf_encoder.py` for each target pdf. The tool generates a _/[downloader page].html_ and a single _/[reader].html_
* The host then puts the newly generated HTML files into their web server and shares the URL for their downloader page.

### User:
![user dia](imgs/jamuser.jpg)
* User visits _/[downloader page].html_ which downloads the embedded PDF into the user's local indexedDB.
* The user will be redirected _/[reader].html_ after the download is complete where all the saved PDF's can be easy read and managed.

### Output Description
**downloader .html file:**
 * This file will be what the user visits in order to download the [pdf to encode]
 * Will also have name given [downloader name]

**reader .html file:**
 * This file is what the download pages redirect to, it is a simple page to view and easily read all saved documents.
 * This is also the page that will be cached, so the user can come back to this page offline for reading at anytime.

**.readerName:**
 * Saves the the randomly generated name of the reader page to properly redirect future download pages.


## Next Steps
* The current reader template uses `<embed>` to read the PDF. This doesn't work on many browsers. A more universal solution needs to be implemented.
* Implement automated caching of the reader page using a service worker (or other solution) for offline reading.