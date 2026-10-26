"""Build the website (repo root) from the sources in src/.  Usage: python3 tools/build.py CACHE_VERSION

The artifact pages are HTML fragments (Claude wraps them in a document when it
publishes). For hosting anywhere else they need a real <head> with a charset,
a mobile viewport, icons, the app manifest and the offline service worker.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = ROOT
GAME = os.path.join(ROOT, 'src', 'game.html')
CLASSIC = os.path.join(ROOT, 'src', 'classic.html')
VERSION = sys.argv[1] if len(sys.argv) > 1 else '3'


def head(title, prefix, manifest):
    return '\n'.join([
        '<!doctype html>',
        '<html lang="en">',
        '<head>',
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
        '<meta name="theme-color" content="#17133d">',
        '<meta name="description" content="A typing game: blast the Potato Pirate with marshmallows from Earth to Mars.">',
        f'<link rel="icon" type="image/png" href="{prefix}icons/icon-192.png">',
        f'<link rel="apple-touch-icon" href="{prefix}icons/icon-192.png">',
        f'<link rel="manifest" href="{prefix}manifest.webmanifest">' if manifest else '',
        f'<title>{title}</title>',
        '<style>[hidden]{display:none!important}</style>',
        '',
    ])


def strip_title(html):
    i = html.index('<title>'); j = html.index('</title>', i) + len('</title>')
    return html[:i] + html[j:].lstrip('\n')


SW_REGISTER = """
<script>
/* Offline support and "Install app": only when served from a web address, not a local file. */
if ('serviceWorker' in navigator && location.protocol !== 'file:') {
  window.addEventListener('load', function () { navigator.serviceWorker.register('%ssw.js').catch(function () {}); });
}
</script>
"""

os.makedirs(os.path.join(SITE, 'classic'), exist_ok=True)

game = open(GAME, encoding='utf-8').read()
open(os.path.join(SITE, 'index.html'), 'w', encoding='utf-8').write(
    head('Potato Pirate', '', True) + strip_title(game).rstrip() + '\n' + (SW_REGISTER % '') + '</html>\n')

classic = open(CLASSIC, encoding='utf-8').read()
open(os.path.join(SITE, 'classic', 'index.html'), 'w', encoding='utf-8').write(
    head('Potato Pirate (classic)', '../', False) + strip_title(classic).rstrip() + '\n' + (SW_REGISTER % '../') + '</html>\n')

manifest = {
    'name': 'Potato Pirate',
    'short_name': 'Potato Pirate',
    'description': 'A typing game: blast the Potato Pirate with marshmallows from Earth to Mars.',
    'start_url': './',
    'scope': './',
    'display': 'standalone',
    'background_color': '#17133d',
    'theme_color': '#17133d',
    'icons': [
        {'src': 'icons/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
        {'src': 'icons/icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
        {'src': 'icons/icon-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'},
    ],
}
open(os.path.join(SITE, 'manifest.webmanifest'), 'w', encoding='utf-8').write(json.dumps(manifest, indent=2) + '\n')

sw = """/* Potato Pirate offline support.
   Pages: network first, so updates show up right away; the saved copy is used when offline.
   Fonts: saved after the first visit so the game looks the same offline. */
const CACHE = 'potato-pirate-v%s';
const CORE = ['./', './index.html', './manifest.webmanifest', './icons/icon-192.png', './icons/icon-512.png', './classic/'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin === location.origin) {
    e.respondWith(fetch(req)
      .then(res => { if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); } return res; })
      .catch(() => caches.match(req, {ignoreSearch: true}).then(r => r || caches.match('./index.html'))));
    return;
  }
  if (url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
    e.respondWith(caches.match(req).then(r => r || fetch(req).then(res => {
      const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); return res;
    })));
  }
});
""" % VERSION
open(os.path.join(SITE, 'sw.js'), 'w', encoding='utf-8').write(sw)
print('built site, cache version', VERSION)
