#!/usr/bin/env python3
"""Arma la versión instalable (PWA) desde app.html. Uso: python3 build.py [carpeta_con_canciones_json]"""
import json, sys, os, glob, hashlib, datetime
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, "app.html"), encoding="utf-8").read()
src = src.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
title_end = src.index("</title>") + len("</title>")
body = src[title_end:]
if len(sys.argv) > 1:
    seeds = []
    for f in sorted(glob.glob(os.path.join(sys.argv[1], "*.json"))):
        d = json.load(open(f, encoding="utf-8")); d = d.get("data", d)
        d.setdefault("id", os.path.basename(f)[:-5]); seeds.append(d)
    open(os.path.join(here, "seed.js"), "w", encoding="utf-8").write(
        "/* Canciones iniciales (copiadas desde Claude). Solo se usan la primera vez que se abre la app. */\nwindow.MAPA_SEED = " + json.dumps(seeds, ensure_ascii=False) + ";\n")
version = hashlib.sha1((body + open(os.path.join(here, "seed.js"), encoding="utf-8").read()).encode()).hexdigest()[:10]
html = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Mapa de batería</title>
<meta name="description" content="Mapa de batería: dinámicas, fills, golpes y cortes de cada canción.">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Mapa batería">
<meta name="theme-color" content="#F6F2F0" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#100E17" media="(prefers-color-scheme: dark)">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icons/icon-180.png?v=2">
<link rel="icon" type="image/png" href="icons/icon-192.png">
<script src="seed.js"></script>
</head>
<body>
{body.strip()}
<script>
/* funciona sin internet: guarda la app en el teléfono */
if ("serviceWorker" in navigator) addEventListener("load", () => navigator.serviceWorker.register("sw.js").catch(() => {{}}));
</script>
</body>
</html>
'''
open(os.path.join(here, "index.html"), "w", encoding="utf-8").write(html)
sw = open(os.path.join(here, "sw.template.js"), encoding="utf-8").read().replace("__VERSION__", version)
open(os.path.join(here, "sw.js"), "w", encoding="utf-8").write(sw)
print("versión", version)
