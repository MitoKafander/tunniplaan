# Tunniplaan

Mikk Rosini tunniplaan Techno Kesklinna ja Mustamäe linnakus koos asenduste ja lõunamenüüga.

- Leht: https://mitokafander.github.io/tunniplaan/
- Andmed: EduPage'i avalik API (`kesklinn-techno`, `mustamae-techno`) ja `menuu.techno.ee`.
- GitHub Action (`.github/workflows/pages.yml`) käivitab `scripts/fetch.py` iga 30 minuti järel
  koolipäevadel, kirjutab `site/data/snap.json` ja avaldab `site/` GitHub Pagesis.
  Andmeid repos ei hoita.
- Rosini õpetaja-id: Kesklinn `-88`, Mustamäe `-77` (Mustamäel on nimi ainult „Rosin“).
- EduPage'i nädalaversioonide `datefrom` on vahel vale (kopeeritud nädal); leht võtab nädala
  versiooni nimest (`09.11-15.11.26`).
