# Tunniplaan

Mikk Rosini tunniplaan Techno Kesklinna ja Mustamäe linnakus koos asenduste ja lõunamenüüga.

- Leht: https://mitokafander.github.io/tunniplaan/
- Andmed: EduPage'i avalik API (`kesklinn-techno`, `mustamae-techno`) ja `menuu.techno.ee`.
- GitHub Action (`.github/workflows/pages.yml`) käivitab `scripts/fetch.py`, kirjutab
  `site/data/snap.json` ja avaldab `site/` GitHub Pagesis. Andmeid repos ei hoita.
- **Ajastus:** GitHub jätab täis- ja pooltunni cron-käivitusi sageli vahele. Seepärast käivitub töö
  koolipäeviti iga 10 min järel (minutid :03, :13 …) ja job `check` jätab vahele, kui avaldatud
  andmed on nooremad kui 25 min. Muul ajal iga 2 tunni järel.
- **EduPage'i tulemüür:** enamik GitHubi Linuxi ja Windowsi masinaid ei pääse EduPage'i (ühendus
  aegub), macOS-i masinad pääsevad (proov 12.11.2026: macOS 3/3, Linux 2/3, ARM 0/3, Windows 0/3).
  Seepärast `runs-on: macos-latest`. Kui ka sealt ei saa, võtab `fetch.py` tunnid kolleegi
  tunniplaanisaidist (`kasparsu.github.io/tahvel-tunniplaan`); asendusi sealt ei tule.
- Lehe värskendusnupp laeb ainult viimase avaldatud seisu, EduPage'i päringut ta käivitada ei saa.
- Rosini õpetaja-id: Kesklinn `-88`, Mustamäe `-77` (Mustamäel on nimi ainult „Rosin“).
- EduPage'i nädalaversioonide `datefrom` on vahel vale (kopeeritud nädal); leht võtab nädala
  versiooni nimest (`09.11-15.11.26`).

## Leht (`site/index.html`)

- Üleval kaart „Järgmisena / Praegu“ (ruum, aeg, mis tuleb pärast); puudutus viib selle päeva juurde.
- Vaated: **Päev** (telefonis vaikimisi; päeva tunnipesad + selle linnaku lõuna), **Nädal**
  (arvutis vaikimisi; read on päevade vahel joondatud), **Lõuna** (mõlema linnaku menüü).
- Päevaribal on nädala viis päeva linnakute täppidega; nooled ja pühkimine vahetavad päeva või nädalat.
- Vabad tunnid on hallid pesad tunni numbri ja kellaajaga; tunniplokk on nii kõrge, mitu tundi ta katab.
- `sw.js` hoiab lehe ja viimase seisu võrguta kasutamiseks (võrk ees, vahemälu varuks).
- Eelvaade teisel ajahetkel: `?now=2026-11-12T08:50`.
