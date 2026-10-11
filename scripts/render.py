"""Render post pages to 2160x2880 PNG (3:4, DPR 2) with a layout QA gate.

    python render.py posts/p01.html [posts/p02.html ...] [--num 1] [--out out]

Output: out/NN-technext-<slug>.png  (slug = the page <title>, set from the spec). NN = --num for the first page,
then +1, or taken from the file name pNN. QA fails (and no PNG is written) when: brand fonts are not loaded, a
[data-qa="name"] block (headline, ticket, url...) leaves the frame or overlaps another block or the logos, or any
text is under 15 px at post scale (mark decorative micro-text with data-qa-skip), or ANY TEXT OVERFLOWS (owner rule
8 Oct 2026, "always check the overflow text"):
  - HTML/SVG text whose glyph box leaves its [data-qa] block, the frame, or is clipped (scrollWidth > clientWidth);
  - canvas text (fillText/strokeText is hooked on every page) that leaves the frame, sits under a [data-qa] card,
    or collides with other canvas text; pass maxWidth-free short labels, or make the sign bigger.
"""
import argparse, json, pathlib, re, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import cdp
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HOOK = r"""(function(){
  window.__cvText=[];
  var P=CanvasRenderingContext2D.prototype;
  ['fillText','strokeText'].forEach(function(fn){var orig=P[fn];
    P[fn]=function(t,x,y,mw){try{ if(this.canvas&&this.canvas.isConnected&&String(t).trim()){
      var m=this.measureText(t), w=(mw&&m.width>mw)?mw:m.width, al=this.textAlign, x0=x;
      if(al==='center')x0=x-w/2; else if(al==='right'||al==='end')x0=x-w;
      var asc=m.actualBoundingBoxAscent||0, des=m.actualBoundingBoxDescent||0, T=this.getTransform(), d=window.devicePixelRatio||1;
      var pts=[[x0,y-asc],[x0+w,y-asc],[x0,y+des],[x0+w,y+des]].map(function(q){return [(T.a*q[0]+T.c*q[1]+T.e)/d,(T.b*q[0]+T.d*q[1]+T.f)/d]});
      var xs=pts.map(function(q){return q[0]}), ys=pts.map(function(q){return q[1]});
      var cr=this.canvas.getBoundingClientRect(), sx=cr.width/(this.canvas.width/d)||1;
      window.__cvText.push({t:String(t).slice(0,40),r:[cr.left+Math.min.apply(0,xs)*sx,cr.top+Math.min.apply(0,ys)*sx,cr.left+Math.max.apply(0,xs)*sx,cr.top+Math.max.apply(0,ys)*sx]});
    }}catch(e){} return orig.apply(this,arguments);};});
})();"""

QA = r"""(async function(){
  await new Promise(function(r){var n=0;(function w(){if(window.__spReady||!window.SP||n++>200)r();else setTimeout(w,50)})()});
  var FL=['800 20px "Plus Jakarta Sans"','400 20px Inter','600 20px Caveat'];
  await Promise.all(FL.map(function(f){return document.fonts.load(f).catch(function(){})}));
  await document.fonts.ready;
  var errs=[], F={w:1080,h:1440};
  if(/^SCENE ERROR/.test(document.title)) errs.push(document.title);
  var fonts=FL.filter(function(f){return !document.fonts.check(f)});
  if(fonts.length) errs.push('fonts not loaded: '+fonts.join(', '));
  var R={};
  var blocks=[].slice.call(document.querySelectorAll('[data-qa]'));
  if(!blocks.length) blocks=['.sp-card','.sp-cap','.sp-foot'].map(function(n){var e=document.querySelector(n);return e&&(e.firstElementChild||e)}).filter(Boolean);
  blocks.forEach(function(el,i){var r=el.getBoundingClientRect();var n=el.getAttribute('data-qa')||el.className||('b'+i);R[n]=[r.left,r.top,r.right,r.bottom];
    if(r.left<0||r.top<0||r.right>F.w+0.5||r.bottom>F.h+0.5) errs.push(n+' leaves the frame '+JSON.stringify(R[n].map(Math.round)));
    if(r.top<170) errs.push(n+' starts at y '+Math.round(r.top)+' - keep content below 170 (logo row zone)');});
  var tn=document.querySelector('.sp-tn').getBoundingClientRect(), od=document.querySelector('.sp-odoo').getBoundingClientRect();
  R['logo-tn']=[tn.left,tn.top,tn.right,tn.bottom]; R['logo-odoo']=[od.left,od.top,od.right,od.bottom];
  var k=Object.keys(R);
  for(var i=0;i<k.length;i++)for(var j=i+1;j<k.length;j++){var a=R[k[i]],b=R[k[j]];
    if(a[0]<b[2]-1&&b[0]<a[2]-1&&a[1]<b[3]-1&&b[1]<a[3]-1) errs.push(k[i]+' overlaps '+k[j]);}
  var small=[]; document.querySelectorAll('body *').forEach(function(e){
    if(e.closest('[data-qa-skip]')) return;
    var t=[].some.call(e.childNodes,function(n){return n.nodeType==3&&n.textContent.trim()}); if(!t) return;
    var cs=getComputedStyle(e); if(cs.display=='none'||cs.visibility=='hidden'||cs.opacity=='0') return;
    var z=1,p=e; while(p&&p!==document.body){z*=parseFloat(getComputedStyle(p).zoom)||1;p=p.parentElement}
    var px=parseFloat(cs.fontSize)*z;
    if(e instanceof SVGElement&&e.ownerSVGElement){var m=e.getScreenCTM(); if(m) px=parseFloat(cs.fontSize)*Math.hypot(m.a,m.b);}
    if(px<15) small.push(e.textContent.trim().slice(0,30)+' '+px.toFixed(1)+'px');});
  if(small.length) errs.push('text under 15px: '+small.slice(0,5).join(' | '));
  /* ---- overflow: HTML/SVG text ---- */
  function inter(a,b){var w=Math.min(a[2],b[2])-Math.max(a[0],b[0]),h=Math.min(a[3],b[3])-Math.max(a[1],b[1]);return w>0&&h>0?w*h:0}
  var over=[], tw=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT,null), nd;
  while((nd=tw.nextNode())){
    if(!nd.textContent.trim()) continue; var el=nd.parentElement; if(!el||el.closest('[data-qa-skip]')) continue;
    var cs=getComputedStyle(el); if(cs.display=='none'||cs.visibility=='hidden') continue;
    var rg=document.createRange(); rg.selectNodeContents(nd); var rr=rg.getBoundingClientRect(); if(!rr.width) continue;
    var tr=[rr.left,rr.top,rr.right,rr.bottom], lab='"'+nd.textContent.trim().slice(0,28)+'"';
    if(tr[0]<-0.5||tr[1]<-0.5||tr[2]>F.w+0.5||tr[3]>F.h+0.5) over.push(lab+' leaves the frame');
    /* container = nearest ancestor that is visibly a box (background or border); bare headlines have none */
    var box=null, q=el;
    while(q&&q!==document.body&&!q.classList.contains('f')){var qs=getComputedStyle(q);
      if((qs.backgroundColor&&qs.backgroundColor!='rgba(0, 0, 0, 0)'&&qs.backgroundColor!='transparent')||qs.backgroundImage!='none'||parseFloat(qs.borderTopWidth)>0){box=q;break;} q=q.parentElement;}
    if(box){var b=box.getBoundingClientRect(), fs=parseFloat(cs.fontSize)||16, vt=fs*.3;
      if(tr[0]<b.left-1||tr[2]>b.right+1||tr[1]<b.top-vt||tr[3]>b.bottom+vt) over.push(lab+' spills out of its box ('+(box.getAttribute('data-qa')||box.className||box.tagName)+')');}
  }
  document.querySelectorAll('body *').forEach(function(e){ if(e.closest('[data-qa-skip]')) return;
    if(![].some.call(e.childNodes,function(n){return n.nodeType==3&&n.textContent.trim()})) return;   // only boxes that hold text directly
    var cs=getComputedStyle(e); if(cs.overflow=='visible'&&cs.overflowX=='visible'&&cs.textOverflow!='ellipsis') return;
    if(e.scrollWidth>e.clientWidth+1||e.scrollHeight>e.clientHeight+1) over.push('"'+e.textContent.trim().slice(0,28)+'" is clipped by its box');});
  /* ---- overflow: canvas text ---- */
  var cv=(window.__cvText||[]), blocks2=[].slice.call(document.querySelectorAll('[data-qa]')).map(function(b){var r=b.getBoundingClientRect();return {n:b.getAttribute('data-qa'),r:[r.left,r.top,r.right,r.bottom]}});
  cv.forEach(function(c,i){ var r=c.r, area=Math.max(1,(r[2]-r[0])*(r[3]-r[1])), lab='canvas "'+c.t+'"';
    var vis=[Math.max(r[0],0),Math.max(r[1],0),Math.min(r[2],F.w),Math.min(r[3],F.h)];
    if(vis[2]<=vis[0]||vis[3]<=vis[1]) return;                                   // fully off-frame scenery: not shown
    if(r[0]<-0.5||r[2]>F.w+0.5||r[1]<-0.5||r[3]>F.h+0.5) over.push(lab+' is cut by the frame edge');
    blocks2.forEach(function(b){ if(inter(r,b.r)>area*.15) over.push(lab+' is hidden under '+b.n); });
    for(var j=i+1;j<cv.length;j++){ var o=cv[j].r, a2=Math.max(1,(o[2]-o[0])*(o[3]-o[1])); if(inter(r,o)>Math.min(area,a2)*.25) over.push(lab+' collides with canvas "'+cv[j].t+'"'); }
  });
  var seen={}; over=over.filter(function(x){if(seen[x])return false;seen[x]=1;return true});
  if(over.length) errs.push('OVERFLOW: '+over.slice(0,8).join(' | ')+(over.length>8?' (+'+(over.length-8)+' more)':''));
  return {errs:errs, rects:R};
})()"""

ap = argparse.ArgumentParser()
ap.add_argument("pages", nargs="+")
ap.add_argument("--num", type=int)
ap.add_argument("--out", default="out")
ap.add_argument("--qa-only", action="store_true")
ap.add_argument("--force", action="store_true", help="drafts: save the PNG even when QA fails")
ap.add_argument("--port", type=int, default=9872)
a = ap.parse_args()
out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
proc, c = cdp.session(a.port)
bad = 0
try:
    c.call("Page.addScriptToEvaluateOnNewDocument", source=HOOK)
    c.metrics(1080, 1440, 2)
    for i, pg in enumerate(a.pages):
        p = pathlib.Path(pg).resolve()
        c.go(p.as_uri(), 1.2)
        r = c.ev(QA)
        title = c.ev("document.title")
        m = re.search(r"p(\d+)", p.stem)
        n = (a.num + i) if a.num else (int(m.group(1)) if m else i + 1)
        name = f"{n:02d}-technext-{title}.png"
        if r["errs"]:
            bad += 1
            print("FAIL", p.name, *r["errs"], sep="\n  ")
            if not a.force:
                continue
        if not a.qa_only:
            c.shot(out / name, {"x": 0, "y": 0, "width": 1080, "height": 1440})
        print("ok  ", p.name, "->", out / name)
finally:
    proc.terminate()
print("ALL CLEAN" if not bad else f"{bad} page(s) failed QA")
sys.exit(1 if bad else 0)
