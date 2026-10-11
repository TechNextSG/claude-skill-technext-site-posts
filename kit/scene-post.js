/* Draw a hero-style scene on #scene with the site's own drawing kit (IXW.kit from assets/js/industry-world.js).
   Usage in a post page (after industry-world.js):
     SP.draw(function (g, K, H) { ... });   // g = 2D context in post px (1080x1440), K = IXW.kit, H = helpers below
   The page is marked ready (window.__spReady) after fonts load and the scene is painted; render.py waits for it. */
(function () {
  var K = window.IXW && window.IXW.kit;
  var H = {
    /* a cast member: defaults for the pill-flat model; s ~0.5 = about 245 px tall */
    who: function (o) {
      var P = Object.assign({ x: 0, y: 0, s: 0.6, ph: 1, mood: 'happy', look: 0, talk: false, feet: true, hands: [[-70, -150], [70, -150]],
        c: { skin: '#E8B48F', hair: '#2B1D16', top: '#3167CA', top2: '#2552A6', low: '#2A3550', shoe: '#2A2F45' }, outfit: 'tee', hairStyle: 'short' }, o);
      P.c = Object.assign({ skin: '#E8B48F', hair: '#2B1D16', top: '#3167CA', top2: '#2552A6', low: '#2A3550', shoe: '#2A2F45' }, o.c || {});
      return P;
    },
    person: function (g, P, t) { K.person(g, P, t == null ? 1.3 : t); },
    /* vertical gradient fill of a rect */
    grad: function (g, x, y, w, h, a, b) { var gr = g.createLinearGradient(0, y, 0, y + h); gr.addColorStop(0, a); gr.addColorStop(1, b); g.fillStyle = gr; g.fillRect(x, y, w, h); },
    /* a warm light pool on the floor */
    pool: function (g, x, y, rx, ry, a) { g.save(); g.translate(x, y); g.scale(1, ry / rx); var r = g.createRadialGradient(0, 0, 4, 0, 0, rx); r.addColorStop(0, 'rgba(255,248,220,' + (a || .55) + ')'); r.addColorStop(1, 'rgba(255,248,220,0)'); g.fillStyle = r; g.beginPath(); g.arc(0, 0, rx, 0, 7); g.fill(); g.restore(); },
    /* depth of field for a foreground prop: draw fn blurred */
    blur: function (g, px, fn) { g.save(); g.filter = 'blur(' + px + 'px)'; fn(); g.restore(); },
    /* one-point perspective floor tiles from a horizon y to the bottom, vanishing at vx */
    floorLines: function (g, y0, y1, vx, col, rows, cols) { g.save(); g.strokeStyle = col; g.lineWidth = 2; g.beginPath();
      for (var d = 1; d <= rows; d++) { var yy = y0 + Math.pow(d / rows, 1.7) * (y1 - y0); g.moveTo(-50, yy); g.lineTo(1130, yy); }
      for (var i = -cols; i <= cols; i++) { g.moveTo(vx + i * 40, y0); g.lineTo(vx + i * 40 * ((y1 - y0) / 60), y1); }
      g.stroke(); g.restore(); },
    vignette: function (g, a) { var r = g.createRadialGradient(540, 760, 300, 540, 760, 980); r.addColorStop(0, 'rgba(20,30,60,0)'); r.addColorStop(1, 'rgba(20,30,60,' + (a || .14) + ')'); g.fillStyle = r; g.fillRect(0, 0, 1080, 1440); }
  };
  window.SP = {
    H: H, K: K,
    draw: function (fn) {
      var cv = document.getElementById('scene'), g = cv.getContext('2d'), dpr = window.devicePixelRatio || 1;
      cv.width = 1080 * dpr; cv.height = 1440 * dpr; g.scale(dpr, dpr);
      (document.fonts ? document.fonts.load('800 20px "Plus Jakarta Sans"').then(function () { return document.fonts.ready; }) : Promise.resolve()).then(function () {
        try { fn(g, K, H); } catch (e) { document.title = 'SCENE ERROR: ' + e.message; console.error(e); }
        window.__spReady = true;
      });
    }
  };
})();
