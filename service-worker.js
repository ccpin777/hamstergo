const CACHE_NAME = 'packing-checklist-cache-v10';
const ASSETS = [
  './',
  './index.html',
  './manifest.json?v=hamstergo-manifest-v2',
  './resources/images/hamstergo-safari-icon-v3.png',
  './resources/images/hamstergo-favicon-v3.png',
  './resources/images/hamstergo-desktop-icon-v1.png?v=hamstergo-desktop-icon-v1',
  './resources/images/hamstergo-favicon-v3.png',
  './resources/images/hamstergo-icon.webp',
  './resources/icons/briefcase.svg',
  './resources/icons/plus.svg',
  './resources/icons/pencil.svg',
  './resources/icons/export.svg',
  './resources/icons/settings.svg',
  './resources/icons/recheck.svg',
  './resources/icons/check.svg',
  './resources/icons/x.svg',
  './resources/icons/trash.svg',
  './resources/icons/drag.svg',
  './resources/icons/chevron-down.svg',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  if(event.request.method !== 'GET') return;

  if (event.request.destination === 'image') {
    event.respondWith(
      caches.match(event.request).then((cached) => cached || fetch(event.request).then((response) => {
        if (response && response.status === 200 && response.type === 'basic') {
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, response.clone()));
        }
        return response;
      }))
    );
    return;
  }

  event.respondWith(
    fetch(event.request).then((response) => {
      if(response && response.status === 200 && response.type === 'basic'){
        const responseClone = response.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(event.request, responseClone));
      }
      return response;
    }).catch(() =>
      caches.match(event.request).then((cached) => {
        if(cached) return cached;
        if(event.request.mode === 'navigate') return caches.match('./index.html');
        return Response.error();
      })
    )
  );
});
