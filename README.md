# Tunniplaan

Mikk Rosini tunniplaan Techno Kesklinna ja Mustamäe linnakus koos asenduste ja lõunamenüüga.

- Leht: https://mitokafander.github.io/tunniplaan/
- Andmed: EduPage'i avalik API (`kesklinn-techno`, `mustamae-techno`) ja `menuu.techno.ee`.
- GitHub Action (`.github/workflows/pages.yml`) käivitab `scripts/fetch.py` iga 30 minuti järel
  koolipäevadel, kirjutab `site/data/snap.json` ja avaldab `site/` GitHub Pagesis.
  Andmeid repos ei hoita.
- EduPage lükkab GitHubi masinate ühendused sageli tagasi. Siis võtab `fetch.py` tunnid kolleegi
  avalikust tunniplaanisaidist (`kasparsu.github.io/tahvel-tunniplaan`); asendusi sealt ei tule.
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
