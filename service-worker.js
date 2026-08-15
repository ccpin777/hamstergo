const CACHE_NAME = 'packing-checklist-cache-v9';
const ASSETS = [
  './',
  './index.html',
  './manifest.json?v=hamstergo-manifest-v2',
  './resources/hamstergo-icon-192.png?v=hamstergo-icon-v2',
  './resources/hamstergo-icon-512.png?v=hamstergo-icon-v2',
  './resources/hamstergo-desktop-icon-v1.png?v=hamstergo-desktop-icon-v1',
  './resources/hamstergo-tab-icon-v2.png?v=hamstergo-tab-icon-v2',
  './resources/hamstergo-icon.webp',
  './resources/briefcase.svg',
  './resources/plus.svg',
  './resources/pencil.svg',
  './resources/export.svg',
  './resources/settings.svg',
  './resources/recheck.svg',
  './resources/check.svg',
  './resources/x.svg',
  './resources/trash.svg',
  './resources/drag.svg',
  './resources/chevron-down.svg',
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
