# RESUME_HERE — tunniplaan

Seis: **12.11.2026 kell 10:46**. Mis ja kuidas töötab → [README](README.md); siin on ainult jätkamiseks vajalik.

## Ligipääs

- Leht: https://mitokafander.github.io/tunniplaan/ · repo `MitoKafander/tunniplaan` (avalik), haru `main`.
- Kohalik kaust: `Techno/tunniplaan/` (AI Projects all). `gh` on Macis sisse logitud.
- Avaldamine: push `main`-i → GitHub Action (`pages.yml`) loeb andmed ja avaldab, u 1 min.
- Käsitsi värskendus ilma muudatuseta: `gh workflow run pages.yml`.
- Kohalik eelvaade: `python3 -I scripts/fetch.py && python3 -m http.server 8765 --directory site`,
  siis `http://localhost:8765/?now=2026-11-12T08:50` (`?now=` näitab lehte teisel ajahetkel).
- Teste ei ole. Kontroll = kohalik eelvaade brauseris + `gh run list` pärast push'i.

## Kontrollitud seis

- ✅ Leht: päeva-, nädala- ja lõunavaade, hele ja tume teema, võrguta avamine (kontrollitud brauseris 11.11).
  Päris telefonis **kontrollimata**: pühkimine päeva vahetamiseks ja avakuvale paigaldamine.
- ✅ Andmed tulevad otse EduPage'ist koos asendustega, sest töö käib macOS-i masinal
  (käivitus 12.11 kell 10:16: mõlemad linnakud otse).
- 🔴 **Ajastus ei tööta.** 12.11 kell 10:46 oli `schedule`-käivitusi **0**: vana cron (`*/30`) ei käivitunud
  4 tunni jooksul kordagi, uus cron (alates 10:15, minutid :03, :13 …) pole kolme pesa jooksul käivitunud.
  Seni uueneb leht ainult push'i või käsitsi käivitusega.

## Järgmised sammud

1. **Kontrolli ajastust** (Mikk palus 12.11 hiljem üle vaadata):
   `gh api "repos/MitoKafander/tunniplaan/actions/runs?event=schedule" --jq .total_count`.
   Lehel näitab sama asja kellaaeg värskendusnupu kõrval; üle 5 tunni vana seis = „vana seis“.
2. **Kui ajastus ei käivitu või on hõre, on vaja Miku otsust.** Variandid:
   - **a) Värskendusnupp käivitab päris päringu.** Fine-grained token (ainult see repo, Actions: write),
     mille Mikk kleebib korra telefonis lehele (jääb `localStorage`-isse); nupp kutsub
     `POST /repos/MitoKafander/tunniplaan/actions/workflows/pages.yml/dispatches`, uus seis u 1 min pärast.
     Pakutud 12.11, vastust ei ole.
   - **b) Kodune alati töötav masin** (nt Home Assistant) kutsub sama API-t iga 30 min järel. Vajab sama tokenit.
   - **c) Oma Cloudflare Worker** cron'iga. Vajab uut kontot.
3. **Tahvli kirjed puuduvad otse-EduPage'i seisus.** Nt E 16:15–17:45 „3D-labor“ oli näha ainult siis,
   kui andmed tulid kolleegi saidilt (seal on Tahvel sees). Kas lisada? Otsustamata.

## Lõksud

- **EduPage'i tulemüür:** GitHubi Linuxi ja Windowsi masinatelt ühendus aegub (proov 12.11: Linux 2/3,
  ARM 0/3, Windows 0/3, macOS 3/3). Pythoni veateade „Network is unreachable“ eksitab: see on IPv6 katse,
  mis varjab IPv4 ajalõppu. Ära vii `build`-tööd tagasi `ubuntu-latest` peale.
- **GitHubi cron:** täis- ja pooltunni käivitused jäävad vahele (kolleegi sama `*/30` annab u 2 käivitust päevas).
- **Kinni jäänud käivitus:** kui push'i käivitus jääb „queued“ ja `jobs` on tühi, aitab `gh workflow run pages.yml`.
  Käivitus 43095640804 (11.11) on selline; seda ei saa tühistada ega kustutada ja see ei sega.
- **Värskendusnupp** laeb ainult viimase avaldatud seisu; EduPage'i päringut ta ei käivita (Mikk eeldas vastupidist).
- **Mustamäe nädalaversioonide `datefrom` on vale** (kopeeritud nädalad) → nädal loetakse versiooni nimest.
- **Service worker** (`site/sw.js`) on võrk-ees. Playwrighti `setOffline` teda ei mõjuta: võrguta olekut
  testi kohaliku serveri peatamisega.
- `site/index.html` on üks fail (CSS ja JS sees); `site/data/` on `.gitignore`-is, andmeid repos ei hoita.
- 60 päeva commit'ideta lülitab GitHub avaliku repo ajastuse välja (saadab enne kirja).

## Miku soovid kujunduses (ära muuda küsimata)

- Päeva tunnipesad peavad näitama ka vabu tunde (nt 1.–6. tühi, kui tund algab 7. tunniga).
- Tunnikaardil neli kindlat rida: aeg ja ruum · „1–2. tund · 2 ak/h“ · aine · rühm ja linnak.
  Üksused ei tohi poole pealt murduda.
- Lõunavaade peab alles jääma.
