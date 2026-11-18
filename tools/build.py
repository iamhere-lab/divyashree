#!/usr/bin/env python3
"""Refresh the inlined CSS and config in index.html. Run after editing
assets/css/styles.css or assets/js/config.js:  python3 tools/build.py"""
import os, re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
css = open("assets/css/styles.css").read()
css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
css = re.sub(r"\s+", " ", css)
css = re.sub(r"\s*([{};])\s*", r"\1", css).replace(";}", "}").strip()
css = css.replace("../fonts/", "assets/fonts/").replace("../img/", "assets/img/")
cfg = re.sub(r"^\s*//.*$", "", open("assets/js/config.js").read(), flags=re.M).strip()
html = open("index.html").read()
def put(name, body):
    global html
    pat = re.compile(r"(<!-- inline:%s[^>]*-->).*?(<!-- /inline:%s -->)" % (name, name), re.S)
    assert pat.search(html), name
    html = pat.sub(lambda m: m.group(1) + body + m.group(2), html)
put("css", "<style>" + css + "</style>")
put("config", "<script>" + cfg + "</script>")
open("index.html", "w").write(html)
print("index.html: %d KB (css %d KB inlined)" % (len(html) // 1024, len(css) // 1024))
