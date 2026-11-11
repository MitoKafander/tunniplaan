// Offline copy of the page and the last timetable. Network first, so a new deploy or new data always
// wins when there is a connection; the cache only answers when the network does not.
const CACHE = 'tunniplaan-v1';

self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil(self.clients.claim()));

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;
  e.respondWith(
    fetch(e.request)
      .then(r => {
        if (r.ok) { const copy = r.clone(); caches.open(CACHE).then(c => c.put(url.pathname, copy)); }
        return r;
      })
      .catch(async () => {
        const r = await caches.match(url.pathname);
        if (!r) return Response.error();
        // mark the copy so the page can say it is showing saved data
        const headers = new Headers(r.headers);
        headers.set('x-offline-copy', '1');
        return new Response(r.body, { status: r.status, statusText: r.statusText, headers });
      })
  );
});
