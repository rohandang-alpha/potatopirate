# Potato Pirate

A typing game made for Neal. The Potato Pirate is racing to Mars to steal the Candy Vault, and the only way to stop him is to type: marshmallow cannons, jellybean blasters, candy canes and a lot of silliness.

**Play:** https://rohandang-alpha.github.io/potatopirate/ (once GitHub Pages is turned on)

- 25 missions in three acts: the home row, the busiest letters, then the rest of the alphabet, capitals and punctuation.
- Finale: a knock-knock-joke vault on Mars, then Candy Runs for ongoing practice.
- Several captains (players) per computer, each with their own stars and progress.
- The first version of the game is at `classic/`.

## Saving

Progress saves automatically in the browser, after every mission. Each browser on each computer keeps its own saves. To move progress to another computer or browser, open **For grown-ups → Copy save code** on the old one and **Load a save code** on the new one. Clearing browsing data, or playing in a private window, erases saves on that browser.

## Install it like an app

On the game page in Edge, open the **…** menu → **Apps** → **Install this site as an app**. In Chrome, click the install icon in the address bar. You get a Start-menu and taskbar icon, the game opens in its own window, and it works offline after the first visit.

## Files

| File | What it is |
|---|---|
| `index.html` | The whole game: one self-contained page |
| `classic/index.html` | The original version |
| `manifest.webmanifest`, `icons/` | App name and icons for installing |
| `sw.js` | Offline support |

No build step and no server code. Any static host works (GitHub Pages, Netlify, Cloudflare Pages), and `index.html` also runs if you just double-click it.

## Updating the game

`src/game.html` is the game as Claude publishes it (an HTML fragment). After changing it, run `python3 tools/build.py N` with a new number N; that rebuilds `index.html` and `classic/index.html` and bumps the offline cache so installed copies pick up the change. `src/classic.html` is the original version, kept as it was.
