"""Prepare a work folder for site-inspired posts.

    python setup.py <work dir> [--site ~/ClaudeWork/tn-social-ref]

Copies into <work>/assets/: the site's css/ and img/ (Odoo icons, reference), js/industry-world.js (the hero drawing kit,
IXW.kit), and the post kit (brand.css, scene.css, scene-post.js, site-post.css, sp/ logos + nexi/). Makes v3/ qa/ out/.
Refresh the site worktree first: git -C <site> fetch -q origin && git -C <site> checkout -q --detach origin/master
"""
import argparse, pathlib, shutil

HERE = pathlib.Path(__file__).resolve().parent
KIT = HERE.parent / "kit"
ap = argparse.ArgumentParser()
ap.add_argument("work")
ap.add_argument("--site", default=str(pathlib.Path.home() / "ClaudeWork" / "tn-social-ref"))
a = ap.parse_args()
work, site = pathlib.Path(a.work), pathlib.Path(a.site)
dst = work / "assets"
for sub in ("css", "img"):
    shutil.copytree(site / "assets" / sub, dst / sub, dirs_exist_ok=True)
(dst / "js").mkdir(parents=True, exist_ok=True)
shutil.copy2(site / "assets" / "js" / "industry-world.js", dst / "js" / "industry-world.js")
for f in ("brand.css", "scene.css", "scene-post.js", "site-post.css"):
    shutil.copy2(KIT / f, dst / f)
shutil.copytree(KIT / "assets", dst / "sp", dirs_exist_ok=True)
for d in ("v3", "qa", "out"):
    (work / d).mkdir(parents=True, exist_ok=True)
print("ready:", work)
