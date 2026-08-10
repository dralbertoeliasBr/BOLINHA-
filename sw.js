/* Service Worker — GaIA · Opera Vox (Sounavy)
   Estratégia: cache-first com atualização em segundo plano.
   O site funciona offline depois da primeira visita. */

const CACHE = 'sounavy-v1';
const ARQUIVOS = [
  './',
  './index.html',
  './manifest.json'
];
/* Os ícones ficam embutidos (base64) dentro do index.html e do manifest.json,
   por isso não precisam de arquivo separado nem entrada própria aqui. */

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(ARQUIVOS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((chaves) =>
      Promise.all(chaves.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    caches.match(e.request).then((cacheado) => {
      const rede = fetch(e.request).then((resp) => {
        if (resp && resp.ok && e.request.url.startsWith(self.location.origin)) {
          const clone = resp.clone();
          caches.open(CACHE).then((c) => c.put(e.request, clone));
        }
        return resp;
      }).catch(() => cacheado);
      return cacheado || rede;
    })
  );
});
