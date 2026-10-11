# Minimal real-time headless Chrome over the DevTools protocol (no --virtual-time-budget: it starves rAF).
import base64, json, os, pathlib, subprocess, time, urllib.request
import websocket

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROFILES = pathlib.Path.home() / "ClaudeWork" / "qa" / "site-posts-profiles"


class CDP:
    def __init__(self, url):
        self.ws = websocket.create_connection(url, max_size=None, timeout=90, suppress_origin=True)
        self.i = 0

    def call(self, method, **params):
        self.i += 1
        self.ws.send(json.dumps({"id": self.i, "method": method, "params": params}))
        while True:
            m = json.loads(self.ws.recv())
            if m.get("id") == self.i:
                if "error" in m:
                    raise RuntimeError(m["error"])
                return m.get("result", {})

    def ev(self, js):
        r = self.call("Runtime.evaluate", expression=js, returnByValue=True, awaitPromise=True)
        if r.get("exceptionDetails"):
            raise RuntimeError(r["exceptionDetails"].get("exception", {}).get("description", str(r["exceptionDetails"])))
        return r.get("result", {}).get("value")

    def metrics(self, w, h, dpr=1):
        self.call("Emulation.setDeviceMetricsOverride", width=w, height=h, deviceScaleFactor=dpr, mobile=False)

    def go(self, url, settle=2.5):
        self.call("Page.navigate", url=url)
        for _ in range(200):
            time.sleep(.1)
            try:
                if self.ev("document.readyState") == "complete":
                    break
            except Exception:
                pass
        time.sleep(settle)

    def shot(self, path, clip=None):
        p = {"format": "png", "captureBeyondViewport": False}
        if clip:
            p["clip"] = dict(clip, scale=1)
        d = self.call("Page.captureScreenshot", **p)["data"]
        pathlib.Path(path).write_bytes(base64.b64decode(d))


def session(port=9871):
    prof = PROFILES / f"p{port}"
    proc = subprocess.Popen([CHROME, "--headless=new", f"--remote-debugging-port={port}", f"--user-data-dir={prof}",
                             "--hide-scrollbars", "--no-first-run", "--force-color-profile=srgb",
                             f"--remote-allow-origins=http://127.0.0.1:{port}", "about:blank"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ws = None
    for _ in range(150):
        try:
            ws = [t for t in json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json")) if t["type"] == "page"][0]["webSocketDebuggerUrl"]
            break
        except Exception:
            time.sleep(.15)
    c = CDP(ws)
    c.call("Page.enable"); c.call("Runtime.enable")
    # the live site sends HeadlessChrome to /denied; a normal desktop UA works locally and live
    c.call("Network.enable")
    c.call("Network.setUserAgentOverride", userAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36")
    return proc, c
