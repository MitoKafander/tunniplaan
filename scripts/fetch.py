#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mikk Rosini tunniplaan: loeb EduPage'i (Kesklinn + Mustamäe) tunnid ja asendused ning
menuu.techno.ee lõunamenüü ja kirjutab need faili site/data/snap.json.
Käivitab GitHub Actions (.github/workflows/pages.yml). Ainult Pythoni standardteek.

EduPage'i server lükkab GitHubi masinate ühendused sageli tagasi. Siis võetakse linnaku tunnid
kolleegi avalikust tunniplaanisaidist (kasparsu.github.io/tahvel-tunniplaan, uueneb iga 30 min),
kus Rosin on Kesklinnas „Mikk Rosin“ ja Mustamäel „Rosin“. Varuallikas asendusi ei sisalda.
"""
import datetime as dt
import html
import json
import os
import re
import time
import urllib.request

VALJUND = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'site', 'data', 'snap.json')
LINNAKUD = {'kesklinn': ('https://kesklinn-techno.edupage.org', '-88'),
            'mustamae': ('https://mustamae-techno.edupage.org', '-77')}
RUHMAD = {'M-MES-26', 'K-SA-24', 'K-VM-24', 'K-VMT-26-1', 'K-VMT-26-2', 'K-ITS4-26MS'}
UA = {'User-Agent': 'Mozilla/5.0 (tunniplaan)'}
VARU = 'https://kasparsu.github.io/tahvel-tunniplaan/data/'
VARU_LINNAK = {'kesklinn': 'K', 'mustamae': 'M'}
MINU_NIMED = {'Rosin', 'Mikk Rosin'}


def get_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode('utf-8'))


def post(url, args, katseid=3, aeg=30):
    body = json.dumps({'__args': args, '__gsh': '00000000'}).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={**UA, 'Content-Type': 'application/json; charset=UTF-8'})
    viga = None
    for katse in range(katseid):
        try:
            with urllib.request.urlopen(req, timeout=aeg) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception as e:
            viga = e
            time.sleep(3 * (katse + 1))
    raise viga


def minutid(s):
    try:
        h, m = (s or '').split(':')
        return int(h) * 60 + int(m)
    except ValueError:
        return 10 ** 6


def plokid(andmed, opetaja):
    T = {t['id']: {r['id']: r for r in t['data_rows']} for t in andmed['tables']}
    per = {p.get('period'): p for p in T.get('periods', {}).values()}
    kaardid = []
    for c in T.get('cards', {}).values():
        L = T.get('lessons', {}).get(c.get('lessonid'))
        if not L or not c.get('period') or opetaja not in (L.get('teacherids') or []):
            continue
        p0 = int(c['period'])
        p1 = p0 + int(L.get('durationperiods') or 1) - 1
        grupid = [T['groups'][g]['name'] for g in (L.get('groupids') or []) if g in T.get('groups', {})]
        grupid = [g for g in grupid if g and g != 'Terve klass']
        klassid = ', '.join(T['classes'][x]['name'] for x in (L.get('classids') or []) if x in T.get('classes', {}))
        for i, b in enumerate(c.get('days') or ''):
            if b == '1':
                kaardid.append({
                    'day': i, 'p0': p0, 'p1': p1,
                    'start': per.get(str(p0), {}).get('starttime'), 'end': per.get(str(p1), {}).get('endtime'),
                    'subject': T.get('subjects', {}).get(L.get('subjectid'), {}).get('name', '?'),
                    'group': klassid + (f" ({', '.join(grupid)})" if grupid else ''),
                    'room': ', '.join(T['classrooms'][r]['short'].strip() for r in (c.get('classroomids') or [])
                                      if r in T.get('classrooms', {}) and T['classrooms'][r].get('short')),
                    'weeks': c.get('weeks') or ''})
    kaardid.sort(key=lambda k: (k['day'], k['p0']))
    out = []
    for k in kaardid:
        e = out[-1] if out else None
        if (e and k['p0'] == e['p1'] + 1 and minutid(k['start']) - minutid(e['end']) <= 15
                and all(e[x] == k[x] for x in ('day', 'subject', 'group', 'room', 'weeks'))):
            e['p1'], e['end'] = k['p1'], k['end']
        else:
            out.append(dict(k))
    for b in out:
        p0, p1 = b.pop('p0'), b.pop('p1')
        b['hours'] = p1 - p0 + 1
        b['lessons'] = str(p0) if p0 == p1 else f'{p0}–{p1}'
    return out


def kellad(andmed):
    """Tunniajad järjekorras: indeks + 1 = tunni number."""
    for t in andmed['tables']:
        if t['id'] == 'periods':
            rows = sorted(t['data_rows'], key=lambda r: int(r.get('period') or 0))
            return [{'start': r.get('starttime'), 'end': r.get('endtime')} for r in rows if str(r.get('period', '')).isdigit()]
    return []


def puhasta(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


def asendused(host, tana):
    leitud = []
    for i in range(-1, 14):
        d = tana + dt.timedelta(days=i)
        if d.weekday() >= 5:
            continue
        h = post(host + '/substitution/server/viewer.js?__func=getSubstViewerDayDataHtml',
                 [None, {'date': d.isoformat(), 'mode': 'classes'}]).get('r')
        if not isinstance(h, str):
            continue
        for osa in h.split('<div class="section')[1:]:
            m = re.search(r'class="header">(.*?)</div>', osa)
            pealkiri = puhasta(m.group(1)) if m else ''
            for klass, tunnid, info in re.findall(
                    r'<div class="row([^"]*)"><div class="period">(.*?)</div><div class="info">(.*?)</div>', osa):
                info = puhasta(info)
                if pealkiri in RUHMAD or 'Rosin' in info or 'Rosin' in pealkiri:
                    leitud.append({'date': d.isoformat(), 'group': pealkiri, 'periods': puhasta(tunnid),
                                   'info': info, 'cancelled': 'remove' in klass})
    return leitud


def linnak(lid, tana):
    host, opetaja = LINNAKUD[lid]
    aasta = tana.year if tana.month >= 8 else tana.year - 1
    lo, hi = (tana - dt.timedelta(days=14)).isoformat(), (tana + dt.timedelta(days=70)).isoformat()
    loend = (post(host + '/timetable/server/ttviewer.js?__func=getTTViewerData', [None, aasta], katseid=1, aeg=20)['r']
             .get('regular') or {}).get('timetables', [])
    jarjest = sorted([t for t in loend if t.get('datefrom')], key=lambda t: t['datefrom'])
    enne = [t for t in jarjest if t['datefrom'] <= lo]
    valik = [t for t in jarjest if lo < t['datefrom'] <= hi or (enne and t is enne[-1])]
    versioonid = []
    for t in valik:
        r = post(host + '/timetable/server/regulartt.js?__func=regularttGetData', [None, str(t['tt_num'])])['r']
        v = {'tt': int(t['tt_num']), 'name': t.get('text'), 'from': t.get('datefrom')}
        if 'dbiAccessorRes' not in r:
            v['hidden'] = True
        else:
            v['blocks'] = plokid(r['dbiAccessorRes'], opetaja)
            v['bells'] = kellad(r['dbiAccessorRes'])
        versioonid.append(v)
    return {'campus': lid, 'fetchedAt': now_iso(), 'versions': versioonid, 'subs': asendused(host, tana)}


def varu_linnak(lid):
    """Kolleegi saidi nädalafailid → sama kuju mis EduPage'ist (üks „versioon“ nädala kohta)."""
    kood = VARU_LINNAK[lid]
    indeks = get_json(VARU + 'index.json')
    versioonid = []
    for n in indeks.get('weeks', []):
        nadal = get_json(VARU + n['file'])
        e = dt.date.fromisoformat(nadal['monday'])
        r = e + dt.timedelta(days=6)
        kellad = nadal.get('periods', {}).get(kood) or []
        algus = {k['start']: i + 1 for i, k in enumerate(kellad)}
        lopp = {k['end']: i + 1 for i, k in enumerate(kellad)}
        tunnid = sorted([l for l in nadal['lessons'] if l.get('campus') == kood and MINU_NIMED & set(l.get('teachers') or [])],
                        key=lambda l: (l['day'], minutid(l['start'])))
        plokid_ = []
        for l in tunnid:
            b = {'day': l['day'], 'start': l['start'], 'end': l['end'], 'subject': l['subject'],
                 'group': ', '.join(l.get('classes') or []) + (f" ({', '.join(l['groups'])})" if l.get('groups') else ''),
                 'room': ', '.join(l.get('rooms') or []), 'weeks': '',
                 'p0': algus.get(l['start']), 'p1': lopp.get(l['end']),
                 'hours': max(1, round((minutid(l['end']) - minutid(l['start']) + 15) / 60))}
            if b['p0'] and b['p1']:
                b['hours'] = b['p1'] - b['p0'] + 1
            v = plokid_[-1] if plokid_ else None
            if (v and minutid(b['start']) - minutid(v['end']) <= 15 and minutid(b['start']) >= minutid(v['end'])
                    and all(v[x] == b[x] for x in ('day', 'subject', 'group', 'room'))):
                v['end'], v['hours'], v['p1'] = b['end'], v['hours'] + b['hours'], b['p1']
            else:
                plokid_.append(b)
        for b in plokid_:
            p0, p1 = b.pop('p0'), b.pop('p1')
            if p0 and p1:
                b['lessons'] = str(p0) if p0 == p1 else f'{p0}–{p1}'
        versioonid.append({'tt': 0, 'name': f"{e:%d.%m}-{r:%d.%m.%y} (varuallikas)", 'from': nadal['monday'], 'blocks': plokid_,
                           'bells': [{'start': k['start'], 'end': k['end']} for k in kellad]})
    return {'campus': lid, 'fetchedAt': indeks.get('generated') or now_iso(), 'versions': versioonid, 'subs': [],
            'fallback': True}


def varu_louna():
    d = get_json(VARU + 'lunch.json')
    out = {}
    for lid, kood in VARU_LINNAK.items():
        paevad = {}
        for p in (d.get('campuses', {}).get(kood) or {}).get('days', []):
            read = []
            for sek in p.get('sections', []):
                for i, roog in enumerate(sek.get('dishes', [])):
                    read.append({'label': sek.get('title', '') if i == 0 else '', 'name': roog.get('name')})
            paevad[p['date']] = read
        out[lid] = paevad
    return out


def louna():
    d = get_json('https://menuu.techno.ee/menu.php?format=json')
    out = {}
    for c in d.get('campuses', []):
        slug = c['campus']['slug']
        if slug not in LINNAKUD:
            continue
        paevad = {}
        for m in c.get('menus', []):
            for paev in (m.get('menu') or {}).get('days', []):
                paevad[paev['date']] = [{'label': x.get('label') or '', 'name': x.get('name')}
                                        for x in (paev.get('rows') or paev.get('lunch') or [])]
        out[slug] = paevad
    return out


def now_iso():
    return dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')


def main():
    tana = dt.date.today()
    snap = {'fetchedAt': now_iso(), 'source': 'github'}
    for lid in LINNAKUD:
        try:
            snap[lid] = linnak(lid, tana)
            print(lid, 'EduPage otse')
        except Exception as e:
            print(lid, 'EduPage ei vasta (', e, ') → varuallikas')
            snap[lid] = varu_linnak(lid)
    try:
        snap['lunch'] = louna()
    except Exception as e:
        print('lõuna otse ebaõnnestus (', e, ') → varuallikas')
        snap['lunch'] = varu_louna()
    os.makedirs(os.path.dirname(VALJUND), exist_ok=True)
    tmp = VALJUND + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(snap, f, ensure_ascii=False)
    os.replace(tmp, VALJUND)
    print(now_iso(), 'ok', VALJUND, sum(len(v.get('blocks', [])) for c in ('kesklinn', 'mustamae') for v in snap[c]['versions']), 'plokki')


if __name__ == '__main__':
    main()
