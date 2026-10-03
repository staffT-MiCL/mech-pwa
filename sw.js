// オフラインでも遊べるよう、ゲーム本体を端末に保存する。更新時は CACHE の番号を上げる
const CACHE='mech-v97';
const FILES=['./','./index.html','./manifest.webmanifest','./vendor/three.module.js','./vendor/three.core.js','./icons/icon-192.png','./icons/icon-512.png','./title.png','./img/clients/client-merchant-otto.png','./img/clients/client-veteran-walter.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)));self.skipWaiting()});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))));self.clients.claim()});
self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET')return;
  // 本体はネット優先（最新版を取りに行き、失敗したら保存分）、フォントなどはキャッシュ優先
  const same=new URL(e.request.url).origin===location.origin;
  if(same){e.respondWith(fetch(e.request).then(r=>{const c=r.clone();caches.open(CACHE).then(x=>x.put(e.request,c));return r}).catch(()=>caches.match(e.request).then(r=>r||caches.match('./index.html'))));}
  else{e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request).then(res=>{const c=res.clone();caches.open(CACHE).then(x=>x.put(e.request,c));return res})));}
});
