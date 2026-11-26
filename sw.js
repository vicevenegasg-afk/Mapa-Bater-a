/* Service worker: guarda la app para usarla sin internet. Con internet siempre busca la versión nueva primero. */
const CACHE = "mapa-bateria-56085eef26-i2";
const FILES = ["./", "index.html", "seed.js", "manifest.webmanifest", "icons/icon-180.png", "icons/icon-192.png", "icons/icon-512.png", "icons/icon-maskable-512.png"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const req = e.request; if (req.method !== "GET" || new URL(req.url).origin !== location.origin) return;
  const isPage = req.mode === "navigate" || req.url.endsWith(".html") || req.url.endsWith("/");
  if (isPage) {
    /* red primero (con límite de 3 s), y si no hay señal, la copia guardada */
    e.respondWith(Promise.race([
      fetch(req).then(r => { const copy = r.clone(); caches.open(CACHE).then(c => c.put(req, copy)); return r; }),
      new Promise((_, rej) => setTimeout(() => rej(new Error("lento")), 3000))
    ]).catch(() => caches.match(req).then(r => r || caches.match("index.html"))));
    return;
  }
  e.respondWith(caches.match(req).then(r => r || fetch(req).then(res => { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); return res; })));
});
