const CACHE_NAME = 'packing-checklist-cache';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './resources/icon-192.png',
  './resources/icon-512.png',
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
