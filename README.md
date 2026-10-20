# Sprawdź, na co wydajesz pieniądze

Projekt z mentoringu „Po prostu koduj” (Paul Crow), cel na październik–listopad 2026.

> **Zadanie:** Zbuduj z AI aplikację, która wczyta wydatki z CSV i pokaże je na wykresie. Potem zapytaj: „Na co poszło najwięcej?” albo „Skąd wzrost wydatków?”. Zacznij od fikcyjnych danych. Na koniec pokaż jeden wykres i sprawdź jego sumę w transakcjach.
> Termin: 15 listopada 2026.

**Aplikacja online:** https://konrados1980.github.io/sprawdz-wydatki/

Kliknij „Wczytaj przykładowe dane (fikcyjne)”, a potem kliknij dowolny kawałek słupka, żeby sprawdzić jego sumę w transakcjach.

⚠️ **Wszystkie dane w tym repozytorium są fikcyjne.** Format jest inspirowany eksportem CSV z mBanku, bez gwarancji zgodności z jego aktualnym eksportem. Aplikacja działa w całości w przeglądarce, wczytany plik nie jest nigdzie wysyłany.

## Jak powstawała aplikacja

Aplikację budowałem krok po kroku z Claude. Każdy krok to osobna strona w folderze [`kroki/`](kroki/) i osobny zapis w historii repozytorium.

| Krok | Strona | Co robi | Czego się nauczyłem |
|---|---|---|---|
| 0 | [`dane/`](dane/) | Fikcyjna historia konta za lipiec–wrzesień 2026 i klucz z poprawnymi odpowiedziami | Testuj na danych, przy których znasz poprawny wynik |
| 1 | [Wczytanie CSV](https://konrados1980.github.io/sprawdz-wydatki/kroki/krok1_wczytanie_csv.html) | Odczytuje plik i sprawdza ciągłość sald | Kodowanie (Windows-1250 vs UTF-8), średnik w opisie, liczenie w groszach |
| 2 | [Kategorie](https://konrados1980.github.io/sprawdz-wydatki/kroki/krok2_kategorie.html) | Rozpoznaje kategorię po opisie | Rodzaj (czy to wydatek?) ≠ kategoria (na co?). Reguły porównują litery, nie znaczenie. Nie zgadujemy, oznaczamy „do wyjaśnienia” |
| 3 | [Wykres](https://konrados1980.github.io/sprawdz-wydatki/kroki/krok3_wykres.html) | Wydatki miesiąc po miesiącu ze sprawdzaniem sumy | Sumę wykresu liczymy drugi raz, niezależnie, z listy transakcji |
| 4 | [Aplikacja](https://konrados1980.github.io/sprawdz-wydatki/) | Wszystko razem plus pytania do AI | Aplikacja liczy, AI tłumaczy. Każda kwota w odpowiedzi AI jest sprawdzana z danymi |

### Pułapki ukryte w danych

- **Przelewy własne i wypłaty z bankomatu** to nie wydatki, tylko przesunięcie pieniędzy. Pokazane osobno.
- **Zwroty** pomniejszają zakup w jego kategorii, a nie są liczone jako przychód.
- **Dwie identyczne płatności** (14.09, kawiarnia, 14,50 PLN) to dwie prawdziwe płatności, nie duplikat.
- **Opis ze średnikiem** (`ALLEGRO.PL; ZAMÓWIENIE…`) musi być w cudzysłowie, inaczej kolumny się przesuwają.
- **Niejasny opis** (`TRN 0347/KX*88213 WAW PL`, 37,00 PLN) trafia do „Do wyjaśnienia”.

## Wnioski z analizy

Wydatki netto: **4 782,12** (lipiec) → **4 895,16** (sierpień) → **5 280,16 PLN** (wrzesień), czyli +498,04 PLN.

- **Najwięcej:** Mieszkanie (2 300,00 PLN miesięcznie), potem Spożywcze.
- **Skąd wzrost:** głównie Jedzenie na mieście, z 239,50 do 730,80 PLN (+491,30 PLN). Częściej (6 → 15 transakcji) i drożej (średnio ok. 40 → 49–57 PLN).
- **Ale nie tylko:** Transport spadł o 169,25 PLN (tankowanie tylko w lipcu), a Rozrywka, Drogeria i Zdrowie urosły razem o ok. 233 PLN. Te zmiany prawie się zniosły, dlatego jedna kategoria „wyjaśnia” prawie cały wzrost.

## Pytania do AI

Część „Zapytaj AI” działa, gdy aplikacja jest otwarta w Claude, bo pytania idą przez konto Claude osoby, która ją otwiera. Na GitHub Pages ta część jest wyłączona, ale przycisk „Kopiuj dane” kopiuje gotowe polecenie z danymi, które można wkleić do dowolnego czatu z AI.

## Dane i generator

- `dane/FIKCYJNE_historia_konta_*.csv`: wyciągi miesięczne i łączny (średnik, Windows-1250, CRLF, od najnowszej operacji).
- `dane/FIKCYJNE_klucz_operacji.csv`: rodzaj i kategoria każdej operacji.
- `dane/FIKCYJNE_klucz_sumy_miesieczne.csv`: poprawne sumy miesięczne do sprawdzania aplikacji.
- `dane/FIKCYJNE_generator_historii_konta.py`: skrypt, który tworzy powyższe pliki i sam je sprawdza.

```bash
python dane/FIKCYJNE_generator_historii_konta.py dane
```

Generator ma stały seed, więc za każdym razem tworzy te same dane.
