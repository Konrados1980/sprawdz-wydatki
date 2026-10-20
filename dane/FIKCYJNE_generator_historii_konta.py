#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIKCYJNE DANE - symulacja historii rachunku w PLN (lipiec-wrzesień 2026).
Format inspirowany eksportem CSV z mBanku, BEZ gwarancji zgodności z jego
aktualnym eksportem. Wszystkie operacje, firmy i numery są zmyślone.

Uruchomienie:  python FIKCYJNE_generator_historii_konta.py [katalog_wyjściowy]
Domyślnie pliki trafiają do katalogu, w którym leży skrypt.
Skrypt generuje pliki, a potem wczytuje je ponownie z dysku i sprawdza
salda, liczby wierszy, format i klucz. Przy błędzie kończy się kodem 1.
"""
import csv
import io
import random
import re
import sys
from calendar import monthrange
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

SEED = 20261115
START_BALANCE = 420_000          # 4200,00 PLN w groszach
ACCOUNT = "0" * 26
BANK_CATEGORY = "Bez kategorii"
ENC = "cp1250"
MONTHS = [(2026, 7), (2026, 8), (2026, 9)]
HEADER = ["#Data operacji", "#Opis operacji", "#Rachunek", "#Kategoria",
          "#Kwota", "#Saldo po operacji", ""]   # pusty element = końcowy średnik
KEY_HEADER = ["Nr wiersza w pliku łącznym", "ID", "Data operacji", "Opis operacji",
              "Kwota", "Rodzaj", "Kategoria", "Powiązana operacja"]
SUMS_HEADER = ["Miesiąc", "Grupa", "Kategoria", "Kwota"]
EAT = "Jedzenie na mieście"
SPEND_KINDS = {"zakup", "rachunek", "subskrypcja", "zwrot"}
ALL_KINDS = SPEND_KINDS | {"wpływ", "transfer własny", "wypłata gotówki"}

OUT_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
P = "FIKCYJNE_"


def month_file(y, m):
    return OUT_DIR / f"{P}historia_konta_{y}-{m:02d}.csv"


COMBINED = OUT_DIR / f"{P}historia_konta_2026-07_do_2026-09.csv"
KEY_FILE = OUT_DIR / f"{P}klucz_operacji.csv"
SUMS_FILE = OUT_DIR / f"{P}klucz_sumy_miesieczne.csv"

AMOUNT_RE = re.compile(r"^(-?)(\d+),(\d{2}) PLN$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def fmt(gr: int) -> str:
    sign = "-" if gr < 0 else ""
    zl, g = divmod(abs(gr), 100)
    return f"{sign}{zl},{g:02d} PLN"


def parse(s: str) -> int:
    m = AMOUNT_RE.match(s)
    if not m:
        raise AssertionError(f"Zły format kwoty: {s!r}")
    v = int(m.group(2)) * 100 + int(m.group(3))
    return -v if m.group(1) else v


# --------------------------------------------------------------------------
# GENEROWANIE
# --------------------------------------------------------------------------
FILLER = [  # (opis, rodzaj, kategoria, min_gr, max_gr, waga)
    ("BIEDRONKA 3021 WARSZAWA", "zakup", "Spożywcze", 1_500, 16_000, 8),
    ("LIDL WARSZAWA UL. FIKCYJNA", "zakup", "Spożywcze", 2_000, 18_000, 7),
    ("ŻABKA Z4417 WARSZAWA", "zakup", "Spożywcze", 500, 4_000, 6),
    ("CARREFOUR EXPRESS WARSZAWA", "zakup", "Spożywcze", 1_200, 9_000, 3),
    ("ROSSMANN 112 WARSZAWA", "zakup", "Drogeria", 1_500, 9_000, 2),
    ("APTEKA POD FIKCYJNYM ORŁEM", "zakup", "Zdrowie", 1_000, 8_000, 1),
    ("STACJA PALIW FIKC 044 WARSZAWA", "zakup", "Transport", 8_000, 22_000, 1),
    ("EMPIK WARSZAWA CENTRUM", "zakup", "Rozrywka", 2_000, 9_000, 1),
]
EAT_PLACES = ["PYSZNE.PL FIKC ZAMÓWIENIE", "UBER EATS WARSZAWA", "BAR MLECZNY FIKCYJNY",
              "PIZZERIA NAPOLI FIKC WARSZAWA", "SUSHI FIKCYJNE WARSZAWA",
              "KEBAB U FIKCYJNEGO WARSZAWA", "BISTRO FIKC MOKOTÓW"]


def build_month(y, m, idx, rng):
    last = monthrange(y, m)[1]
    ops = []

    def add(day, desc, amount, kind, cat, link=None):
        op = {"date": date(y, m, day), "desc": desc, "amount": amount,
              "kind": kind, "cat": cat, "link": link}
        ops.append(op)
        return op

    def rd(a, b):
        return rng.randint(a, min(b, last))

    # Pensja, rachunki, subskrypcje, transport
    add(10, f"PRZELEW PRZYCHODZĄCY FIKCYJNA FIRMA SP. Z O.O. WYNAGRODZENIE {m - 1:02d}/{y}",
        850_000, "wpływ", "Wynagrodzenie")
    add(5, "PRZELEW ZEWNĘTRZNY CZYNSZ NAJMU - FIKCYJNY WYNAJMUJĄCY", -230_000, "rachunek", "Mieszkanie")
    add(15, "PRZELEW ZEWNĘTRZNY FIKCYJNA ENERGIA SA FAKTURA", -rng.randint(14_000, 19_000), "rachunek", "Media")
    add(12, "PRZELEW ZEWNĘTRZNY FIKCYJNY OPERATOR INTERNET", -6_999, "rachunek", "Internet i telefon")
    add(20, "PRZELEW ZEWNĘTRZNY FIKCYJNA SIEĆ KOMÓRKOWA ABONAMENT", -4_500, "rachunek", "Internet i telefon")
    add(3, "NETFLIX.COM SUBSKRYPCJA", -4_900, "subskrypcja", "Subskrypcje")
    add(8, "SPOTIFY P1234FIKC", -2_399, "subskrypcja", "Subskrypcje")
    add(22, "GOOGLE ONE CHMURA 100 GB", -999, "subskrypcja", "Subskrypcje")
    add(1, "ZTM WARSZAWA BILET 30-DNIOWY", -11_000, "zakup", "Transport")

    # Transfery własne
    add(11, "PRZELEW WŁASNY NA RACHUNEK OSZCZĘDNOŚCIOWY", -150_000, "transfer własny", "Transfer własny")
    if idx == 2:
        add(26, "PRZELEW WŁASNY Z RACHUNKU OSZCZĘDNOŚCIOWEGO", 60_000, "transfer własny", "Transfer własny")

    # Wypłaty gotówki
    add(rd(1, 9), "WYPŁATA Z BANKOMATU EURONET WARSZAWA", -20_000, "wypłata gotówki", "Gotówka")
    add(rd(16, 28), "WYPŁATA Z BANKOMATU PKO WARSZAWA", -rng.choice([10_000, 20_000, 30_000]),
        "wypłata gotówki", "Gotówka")

    # Zakup + powiązany zwrot (w sierpniu opis ze średnikiem -> pole w cudzysłowie)
    refund_cases = [
        ("ZALANDO SE ZAMÓWIENIE 10458821", "Odzież", -24_998, 24_998),
        ("ALLEGRO.PL; ZAMÓWIENIE 5521-FIKC", "Zakupy online", -15_990, 7_995),  # zwrot częściowy
        ("MEDIA EXPERT WARSZAWA", "Elektronika", -39_900, 39_900),
    ]
    desc, cat, buy, ret = refund_cases[idx]
    pday = rng.randint(3, 16)
    purchase = add(pday, desc, buy, "zakup", cat)
    add(pday + rng.randint(4, 9), f"ZWROT {desc}", ret, "zwrot", cat, link=purchase)

    # Niejasny opis (lipiec)
    if idx == 0:
        add(rd(13, 25), "TRN 0347/KX*88213 WAW PL", -3_700, "zakup", "Niejasne - do wyjaśnienia")

    # Dwie osobne, identyczne płatności (wrzesień)
    if idx == 2:
        for _ in range(2):
            add(14, "KAWIARNIA ZIARNO FIKC WARSZAWA", -1_450, "zakup", EAT)

    # Jedzenie na mieście - rośnie z miesiąca na miesiąc (liczba i kwoty)
    n_eat = [6, 9, 13][idx]
    mult = [100, 118, 135][idx]
    for _ in range(n_eat):
        add(rd(1, 31), rng.choice(EAT_PLACES), -(rng.randint(2_500, 6_500) * mult // 100), "zakup", EAT)

    # Wypełnienie do 45-60 operacji
    target = rng.randint(45, 60)
    weights = [f[5] for f in FILLER]
    while len(ops) < target:
        d, k, c, lo, hi, _w = rng.choices(FILLER, weights=weights)[0]
        add(rd(1, 31), d, -rng.randint(lo, hi), k, c)
    if not 45 <= len(ops) <= 60:
        raise AssertionError(f"{y}-{m:02d}: {len(ops)} operacji poza zakresem 45-60")

    ops.sort(key=lambda o: o["date"])   # stabilne sortowanie chronologiczne
    return ops


def summarize(records, balances):
    """records: dict(month, amount, kind, cat); balances: {month: (start, end)}."""
    rows = []
    for mon in sorted(balances):
        rec = [r for r in records if r["month"] == mon]
        inc, spend = defaultdict(int), defaultdict(int)
        refunds = transfers = cash = 0
        for r in rec:
            k, a = r["kind"], r["amount"]
            if k == "wpływ":
                inc[r["cat"]] += a
            elif k in SPEND_KINDS:          # zwroty pomniejszają wydatki w kategorii zakupu
                spend[r["cat"]] += -a
                if k == "zwrot":
                    refunds += a
            elif k == "transfer własny":
                transfers += a
            elif k == "wypłata gotówki":
                cash += -a
            else:
                raise AssertionError(f"Nieznany rodzaj: {k}")
        for c in sorted(inc):
            rows.append((mon, "Wpływy", c, inc[c]))
        rows.append((mon, "Wpływy", "RAZEM", sum(inc.values())))
        for c in sorted(spend, key=lambda c: (-spend[c], c)):
            rows.append((mon, "Wydatki netto po zwrotach", c, spend[c]))
        rows.append((mon, "Wydatki netto po zwrotach", "RAZEM", sum(spend.values())))
        rows.append((mon, "Informacyjnie", "Zwroty odjęte od wydatków", refunds))
        rows.append((mon, "Transfery własne (saldo)", "RAZEM", transfers))
        rows.append((mon, "Wypłaty gotówki", "RAZEM", cash))
        s, e = balances[mon]
        rows += [(mon, "Kontrola", "Saldo początkowe", s),
                 (mon, "Kontrola", "Saldo końcowe", e),
                 (mon, "Kontrola", "Zmiana salda", e - s)]
    return rows


def writer(f):
    return csv.writer(f, delimiter=";", lineterminator="\r\n", quoting=csv.QUOTE_MINIMAL)


def generate():
    rng = random.Random(SEED)
    months, seq, bal = [], 0, START_BALANCE
    balances = {}
    for idx, (y, m) in enumerate(MONTHS):
        ops = build_month(y, m, idx, rng)
        start = bal
        for op in ops:
            seq += 1
            op["id"] = f"OP-{seq:04d}"
            bal += op["amount"]
            op["balance"] = bal
            if bal < 0:
                raise AssertionError(f"Ujemne saldo {fmt(bal)} w dniu {op['date']}")
        balances[f"{y}-{m:02d}"] = (start, bal)
        months.append(((y, m), ops))

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    def bank_row(op):
        return [op["date"].isoformat(), op["desc"], ACCOUNT, BANK_CATEGORY,
                fmt(op["amount"]), fmt(op["balance"]), ""]

    for (y, m), ops in months:
        with open(month_file(y, m), "w", encoding=ENC, newline="") as f:
            w = writer(f)
            w.writerow(HEADER)
            w.writerows(bank_row(o) for o in reversed(ops))      # od najnowszej

    all_new_first = [o for _, ops in reversed(months) for o in reversed(ops)]
    with open(COMBINED, "w", encoding=ENC, newline="") as f:
        w = writer(f)
        w.writerow(HEADER)
        w.writerows(bank_row(o) for o in all_new_first)

    with open(KEY_FILE, "w", encoding=ENC, newline="") as f:
        w = writer(f)
        w.writerow(KEY_HEADER)
        for i, o in enumerate(all_new_first, 1):
            w.writerow([i, o["id"], o["date"].isoformat(), o["desc"], fmt(o["amount"]),
                        o["kind"], o["cat"], o["link"]["id"] if o["link"] else ""])

    records = [{"month": o["date"].isoformat()[:7], "amount": o["amount"],
                "kind": o["kind"], "cat": o["cat"]} for o in all_new_first]
    with open(SUMS_FILE, "w", encoding=ENC, newline="") as f:
        w = writer(f)
        w.writerow(SUMS_HEADER)
        w.writerows([mon, g, c, fmt(v)] for mon, g, c, v in summarize(records, balances))


# --------------------------------------------------------------------------
# WERYFIKACJA (tylko na podstawie plików wczytanych z dysku)
# --------------------------------------------------------------------------
def read_csv(path):
    raw = path.read_bytes()
    assert raw.count(b"\n") == raw.count(b"\r\n"), f"{path.name}: nie wszystkie końce linii to CRLF"
    text = raw.decode(ENC)  # błąd, jeśli plik nie jest w Windows-1250
    return text, list(csv.reader(io.StringIO(text, newline=""), delimiter=";"))


def check_bank_file(path, start_balance, month=None):
    text, rows = read_csv(path)
    assert rows[0] == HEADER, f"{path.name}: zły nagłówek {rows[0]}"
    data, prev = rows[1:], None
    for n, r in enumerate(data, 2):
        assert len(r) == 7 and r[6] == "", f"{path.name} w.{n}: zła liczba pól"
        assert DATE_RE.match(r[0]), f"{path.name} w.{n}: data {r[0]}"
        date.fromisoformat(r[0])
        assert r[2] == ACCOUNT and r[3] == BANK_CATEGORY, f"{path.name} w.{n}: rachunek/kategoria"
        if month:
            assert r[0].startswith(month), f"{path.name} w.{n}: data spoza miesiąca"
        assert prev is None or r[0] <= prev, f"{path.name} w.{n}: kolejność nie od najnowszej"
        prev = r[0]
    bal = start_balance
    for r in reversed(data):                       # od najstarszej
        bal += parse(r[4])
        assert bal == parse(r[5]), f"{path.name}: saldo {r[5]} ≠ {fmt(bal)} ({r[0]} {r[1]})"
    return text, data, bal


def verify():
    rep = []
    bal, monthly, balances = START_BALANCE, [], {}
    for (y, m) in MONTHS:
        mon = f"{y}-{m:02d}"
        _, data, end = check_bank_file(month_file(y, m), bal, mon)
        assert 45 <= len(data) <= 60, f"{mon}: {len(data)} wierszy"
        balances[mon] = (bal, end)
        rep.append(f"{mon}: {len(data)} operacji, saldo {fmt(bal)} -> {fmt(end)} ✓")
        monthly.append(data)
        bal = end

    text, comb, comb_end = check_bank_file(COMBINED, START_BALANCE)
    assert len(comb) == sum(map(len, monthly)), "liczba wierszy w pliku łącznym"
    assert comb == [r for d in reversed(monthly) for r in d], "plik łączny ≠ pliki miesięczne"
    assert comb_end == bal, "saldo końcowe pliku łącznego"
    rep.append(f"Plik łączny: {len(comb)} wierszy, saldo końcowe {fmt(comb_end)} ✓")

    _, krows = read_csv(KEY_FILE)
    assert krows[0] == KEY_HEADER
    kd = krows[1:]
    assert len(kd) == len(comb), "liczba wierszy klucza"
    by_id = {}
    for i, (k, c) in enumerate(zip(kd, comb), 1):
        assert int(k[0]) == i and (k[2], k[3], k[4]) == (c[0], c[1], c[4]), f"klucz w.{i} ≠ plik łączny"
        assert k[5] in ALL_KINDS and k[6], f"klucz w.{i}: rodzaj/kategoria"
        by_id[k[1]] = k
    assert len(by_id) == len(kd), "zduplikowane ID w kluczu"
    rep.append(f"Klucz: {len(kd)} wierszy zgodnych 1:1 z plikiem łącznym ✓")

    refunds = [k for k in kd if k[5] == "zwrot"]
    assert len(refunds) == 3
    for k in refunds:
        p = by_id[k[7]]
        assert p[5] == "zakup" and p[6] == k[6] and p[2] <= k[2] and 0 < parse(k[4]) <= -parse(p[4])
    rep.append(f"Zwroty: {len(refunds)}, każdy powiązany z wcześniejszym zakupem ✓")

    semi = [c for c in comb if ";" in c[1]]
    assert semi and all(f'"{c[1]}"' in text for c in semi)
    rep.append(f"Opis ze średnikiem w cudzysłowie: {len(semi)} wiersze ✓")

    dups = [k for k, v in Counter((c[0], c[1], c[4]) for c in comb).items() if v >= 2]
    assert ("2026-09-14", "KAWIARNIA ZIARNO FIKC WARSZAWA", "-14,50 PLN") in dups
    assert any(c[1] == "TRN 0347/KX*88213 WAW PL" for c in comb)
    rep.append("Dwie identyczne płatności i niejasny opis obecne ✓")

    eat = defaultdict(int)
    for k in kd:
        if k[6] == EAT:
            eat[k[2][:7]] -= parse(k[4])
    seq = [eat[mo] for mo in sorted(balances)]
    assert seq[0] < seq[1] < seq[2], f"jedzenie na mieście nie rośnie: {seq}"
    rep.append("Jedzenie na mieście: " + " < ".join(fmt(v) for v in seq) + " ✓")

    _, srows = read_csv(SUMS_FILE)
    assert srows[0] == SUMS_HEADER
    file_sums = [(r[0], r[1], r[2], parse(r[3])) for r in srows[1:]]
    recs = [{"month": k[2][:7], "amount": parse(k[4]), "kind": k[5], "cat": k[6]} for k in kd]
    assert file_sums == summarize(recs, balances), "sumy miesięczne ≠ przeliczenie z klucza"
    look = {(mo, g, c): v for mo, g, c, v in file_sums}
    for mo, (s, e) in balances.items():
        lhs = (look[(mo, "Wpływy", "RAZEM")] - look[(mo, "Wydatki netto po zwrotach", "RAZEM")]
               + look[(mo, "Transfery własne (saldo)", "RAZEM")] - look[(mo, "Wypłaty gotówki", "RAZEM")])
        assert lhs == e - s == look[(mo, "Kontrola", "Zmiana salda")], f"{mo}: sumy nie uzgadniają salda"
    rep.append("Sumy miesięczne: wpływy − wydatki ± transfery − gotówka = zmiana salda ✓")
    return rep


if __name__ == "__main__":
    generate()
    try:
        report = verify()
    except AssertionError as e:
        print("BŁĄD WERYFIKACJI:", e)
        sys.exit(1)
    print("FIKCYJNE DANE - weryfikacja zakończona pomyślnie")
    print("\n".join(report))
