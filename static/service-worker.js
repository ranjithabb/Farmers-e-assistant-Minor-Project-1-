const cname="fea"
const staticcasses=[
  './',
  '/templates',
  '/static'
];

self.addEventListener('install',event=>{
  console.log("sw installed");
  event.waitUntill(
    caches.open(cname).then(cache=>{
      console.log('cacthing static data')
      cache.addAll(staticcasses)
    })
  )
})

self.addEventListener('activate',event=>{
  console.log('sw activated');
})

self.addEventListener('fetch',event=>{
  console.log('sw fetched',event);
})