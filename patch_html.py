p='www/index.html'
s=open(p,encoding='utf-8').read()

old='<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">'
assert old in s
ff=''.join('@font-face{font-family:"Plus Jakarta Sans";font-style:normal;font-weight:%d;font-display:swap;src:url(fonts/plus-jakarta-sans-latin-%d-normal.woff2) format("woff2")}'%(w,w) for w in (400,500,600,700,800))
s=s.replace(old,'<style>'+ff+'</style>')

bridge = r'''<script>
/* Android (Capacitor) bridge: saving/sharing files from the WebView */
(function(){
const C=window.Capacitor, native=!!(C&&C.isNativePlatform&&C.isNativePlatform());
window.NATIVE_APP=native;
if(!native)return;
const P=C.Plugins||{};
function b64FromBlob(b){return new Promise((res,rej)=>{const r=new FileReader();r.onload=()=>res(String(r.result).split(',')[1]);r.onerror=rej;r.readAsDataURL(b)})}
function b64FromText(t){return btoa(unescape(encodeURIComponent(t)))}
async function toCache(name,b64){const r=await P.Filesystem.writeFile({path:'export/'+name,data:b64,directory:'CACHE',recursive:true});return r.uri}
window.nativeShareFiles=async function(files,title){
 const uris=[];
 for(const f of files){const d=f.blob?await b64FromBlob(f.blob):b64FromText(f.text);uris.push(await toCache(f.name,d))}
 await P.Share.share({title:title||'WorkMw',dialogTitle:title||'Share or save',files:uris});
};
const blobs=new Map(), origCreate=URL.createObjectURL.bind(URL);
URL.createObjectURL=function(o){const u=origCreate(o);if(o instanceof Blob)blobs.set(u,o);return u};
const origClick=HTMLAnchorElement.prototype.click;
HTMLAnchorElement.prototype.click=function(){
 if(this.download&&blobs.has(this.href)){
  const b=blobs.get(this.href), name=this.download;
  window.nativeShareFiles([{name,blob:b}],name).catch(e=>{if(!/cancel/i.test(String(e&&e.message||e)))alert('Could not save file: '+(e&&e.message||e))});
  return;
 }
 return origClick.apply(this,arguments);
};
})();
</script>
'''
i=s.index('<script>\n')
s=s[:i]+bridge+s[i:]

old_csv="try{const d=await claude.use('downloads');if(!d)throw 0;await d.save({filename:'workmw-shares.csv',data:csv});b.textContent='Saved'}catch(x){b.textContent='Download not available here'}"
assert old_csv in s
new_csv="try{if(window.NATIVE_APP){await window.nativeShareFiles([{name:'workmw-shares.csv',text:csv}],'workmw-shares.csv');b.textContent='Saved'}else{const d=await claude.use('downloads');if(!d)throw 0;await d.save({filename:'workmw-shares.csv',data:csv});b.textContent='Saved'}}catch(x){b.textContent='Download not available here'}"
s=s.replace(old_csv,new_csv)

old_all="$('pDlAll').onclick=async()=>{vacs[cur]=readForm();const tmp=document.createElement('canvas');"
assert old_all in s
new_all="$('pDlAll').onclick=async()=>{vacs[cur]=readForm();const tmp=document.createElement('canvas');if(window.NATIVE_APP){const fl=[];for(const v of vacs){drawPoster(tmp,v,plLayout);const bl=await new Promise(r=>tmp.toBlob(r,'image/png'));fl.push({name:pName(v),blob:bl})}try{await window.nativeShareFiles(fl,'WorkMw posters');$('pDlAll').textContent='Done'}catch(e){}setTimeout(()=>$('pDlAll').textContent='Download all',1800);return}"
s=s.replace(old_all,new_all)

s=s.replace("Saved on this device only. It will sync across devices when you are signed in to claude.ai.","Saved on this device only.")
open(p,'w',encoding='utf-8').write(s)
print('ok',len(s))
