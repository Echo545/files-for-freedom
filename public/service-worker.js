
// Define the cache name and files to be cached
const CACHE_NAME = 'freedom-files';
const pageName = 'pages'
const dbName = 'pdfDatabase'
const urlsToCache = [
  '/4nDI0WO9KiV37AN.html'
];

// Install event listener for service worker
self.addEventListener('install', event => {
  // Perform installation steps
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// Fetch event listener for service worker
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Cache hit - return response
        if (response) {
          return response;
        }
        // If user is offline, retrieve HTML page from IndexedDB
        if (!navigator.onLine) {
          return getHtmlFromIndexedDb(event.request.url);
        }

        // Clone the request
        const fetchRequest = event.request.clone();

        return fetch(fetchRequest)
          .then(response => {
            // Check if we received a valid response
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // Clone the response
            const responseToCache = response.clone();

            // Add the response to the cache
            caches.open(CACHE_NAME)
              .then(cache => {
                cache.put(event.request, responseToCache);
              });

            return response;
          });
      })
  );
});

// Function to retrieve HTML page from IndexedDB
function getHtmlFromIndexedDb(url) {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(dbName);

    request.onerror = function(event) {
      reject(Error('Error opening database'));
    };

    request.onsuccess = function(event) {
      const db = event.target.result;
      const transaction = db.transaction([pageName], 'readonly');
      const objectStore = transaction.objectStore(pageName);
      const getRequest = objectStore.get(url);

      getRequest.onerror = function(event) {
        reject(Error('Error retrieving data from database'));
      };

      getRequest.onsuccess = function(event) {
        if (event.result) {
          resolve(new Response(event.target.result.html, { headers: { 'Content-Type': 'text/html' } }));
        } else {
          reject(Error('No data found in database'));
        }
      };
    };
  });
}
