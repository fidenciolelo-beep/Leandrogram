self.addEventListener('install', function(e) {
  console.log('App instalado!');
});

self.addEventListener('fetch', function(e) {
  e.respondWith(fetch(e.request));
});
