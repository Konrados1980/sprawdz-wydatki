# Odpowiedzi AI z archiwum aplikacji

Pytania zadane w aplikacji „Sprawdź, na co wydajesz” w Claude, 21.10.2026. Dane FIKCYJNE: 156 operacji z okresu 2026-07-01 – 2026-09-30.

Odpowiedzi są przepisane z archiwum bez zmian. Pod każdą jest:
- **Sprawdzenie aplikacji:** automatyczny test, czy każda kwota z odpowiedzi występuje w danych.
- **Sprawdzenie z kluczem:** ręczna kontrola (zrobiona razem z Claude), czy kwoty są użyte we właściwym miejscu. Automat sprawdza tylko, czy liczba gdzieś istnieje. Gdyby AI przypisało 499,25 PLN do złej kategorii, automat by tego nie zauważył.

## Podsumowanie

| | |
|---|---|
| Pytań | 4 (2 z zadania + 2 własne) |
| Kwot w odpowiedziach | 52 |
| Kwot spoza danych (automat) | 0 |
| Błędów merytorycznych (ręczne sprawdzenie z kluczem) | 0 |

**Co AI zrobiło dobrze:**
- **Przy „Skąd wzrost wydatków?”** wskazało główną przyczynę (jedzenie na mieście), ale też wymieniło kategorie, które spadły, w tym transport. To dokładnie ten wniosek, który znalazłem sam, klikając w wykres.
- **Samo zauważyło zwrot elektroniki** (399,00 PLN) i wyjaśniło, że nie wpływa na wydatki netto.
- **Nie zgadywało przy niejasnej operacji.** Przy pytaniu o transport wspomniało o „TRN 0347/KX*88213 WAW PL” za 37,00 PLN i uczciwie napisało, że nie wie, czy to transport.
- **Pilnowało zasady, że przelewy na oszczędności i gotówka to nie wydatki.**
- **Przy pytaniu o czynsz** nie tylko odpowiedziało „nie”, ale sprawdziło też powiązane rachunki (media, internet).

---

## 1. Na co poszło najwięcej?

*Pytanie z zadania · 21.10.2026, 13:47*

Najwięcej poszło na mieszkanie: 6900,00 PLN w całym okresie (2300,00 PLN miesięcznie, bez zmian).

Kolejne kategorie:
- Spożywcze: 4190,49 PLN
- Jedzenie na mieście: 1483,03 PLN
- Media: 520,99 PLN
- Transport: 499,25 PLN

Razem wydatki netto w okresie to 14957,44 PLN. Do wydatków nie wliczam przelewów własnych na oszczędności ani wypłat gotówki.

Jeśli pytasz o kategorię, która rośnie, to jest to Jedzenie na mieście: 239,50 PLN w lipcu, a 730,80 PLN we wrześniu (zmiana +491,30 PLN). Spożywcze spadły w tym czasie o 22,33 PLN, a Transport o 169,25 PLN.

> **Sprawdzenie aplikacji:** 12 kwot, wszystkie występują w danych.
> **Sprawdzenie z kluczem:** wszystkie sumy kategorii i suma 14 957,44 PLN zgodne z `dane/FIKCYJNE_klucz_sumy_miesieczne.csv`. Kolejność kategorii poprawna.

## 2. Skąd wzrost wydatków?

*Pytanie z zadania · 21.10.2026, 13:48*

Wydatki netto wzrosły z 4782,12 PLN (lipiec) do 5280,16 PLN (wrzesień), czyli o +498,04 PLN.

Główna przyczyna:
- Jedzenie na mieście: +491,30 PLN (z 239,50 PLN do 730,80 PLN). Liczba transakcji wzrosła z 6 do 15.

Inne kategorie, które wzrosły:
- Rozrywka: +115,66 PLN
- Drogeria: +64,55 PLN
- Zdrowie: +52,79 PLN
- Media: +2,32 PLN

Kategorie, które spadły:
- Transport: -169,25 PLN
- Spożywcze: -22,33 PLN
- Do wyjaśnienia: -37,00 PLN

Mieszkanie, Internet i telefon oraz Subskrypcje nie zmieniły się.

Po miesiącach: z lipca na sierpień razem +113,04 PLN (najwięcej Jedzenie na mieście +273,23 PLN, przy spadku Spożywczych o -271,55 PLN). Z sierpnia na wrzesień razem +385,00 PLN (Spożywcze +249,22 PLN i Jedzenie na mieście +218,07 PLN).

Uwaga: zakup elektroniki za 399,00 PLN we wrześniu został zwrócony, więc nie wpływa na wydatki netto.

> **Sprawdzenie aplikacji:** 20 kwot, wszystkie występują w danych.
> **Sprawdzenie z kluczem:** wszystkie zmiany kategorii zgodne z kluczem. Liczba transakcji jedzenia na mieście (6 w lipcu, 15 we wrześniu) zgodna. Zakup w Media Expert 16.09 i zwrot 23.09, oba po 399,00 PLN, zgodne.

## 3. Ile wydałem na transport w ostatnich miesiącach?

*Własne pytanie · 21.10.2026, 13:47*

Na transport w okresie 2026-07 – 2026-09 wydałeś łącznie 499,25 PLN. Z miesiąca na miesiąc wyglądało to tak:

- lipiec 2026: 279,25 PLN (2 transakcje, w tym bilet ZTM 30-dniowy za 110,00 PLN oraz tankowanie na stacji paliw za 169,25 PLN)
- sierpień 2026: 110,00 PLN (1 transakcja, bilet ZTM)
- wrzesień 2026: 110,00 PLN (1 transakcja, bilet ZTM)

Zmiana między lipcem a wrześniem to -169,25 PLN. Wynika z tego, że po lipcowym tankowaniu nie było już wydatków na paliwo, został tylko bilet miesięczny.

Warto dodać, że operacja z 2026-07-23 (TRN 0347/KX*88213 WAW PL, 37,00 PLN) nie ma rozpoznanej kategorii i jest w pozycji "Do wyjaśnienia". Nie wiem, czy to był transport, więc nie wliczam jej do powyższej kwoty.

> **Sprawdzenie aplikacji:** 8 kwot, wszystkie występują w danych.
> **Sprawdzenie z kluczem:** zgodne. Transakcje: ZTM 01.07, 01.08, 01.09 po 110,00 PLN, stacja paliw 06.07 za 169,25 PLN.

## 4. Czy opłata za mieszkanie podrożała ostatnio?

*Własne pytanie · 21.10.2026, 13:49*

Nie, opłata za mieszkanie nie podrożała. W całym okresie jest taka sama:

- lipiec 2026: 2300,00 PLN
- sierpień 2026: 2300,00 PLN
- wrzesień 2026: 2300,00 PLN

Zmiana między lipcem a wrześniem wynosi 0,00 PLN. To jedna transakcja miesięcznie, przelew czynszu najmu, wykonywany około 5. dnia miesiąca.

Jeśli pytasz o koszty związane z mieszkaniem, to kategoria Media (rachunek za energię) wahała się: 164,64 PLN w lipcu, 189,39 PLN w sierpniu i 166,96 PLN we wrześniu. Zmiana lipiec→wrzesień to +2,32 PLN, czyli niewielka. Sierpień był chwilowo wyższy (+24,75 PLN względem lipca), ale we wrześniu rachunek spadł (-22,43 PLN).

Internet i telefon też bez zmian: 114,99 PLN miesięcznie.

Wzrost wydatków w ostatnich miesiącach wynika głównie z innych kategorii, przede wszystkim z jedzenia na mieście (+491,30 PLN lipiec→wrzesień).

> **Sprawdzenie aplikacji:** 12 kwot, wszystkie występują w danych.
> **Sprawdzenie z kluczem:** zgodne. Czynsz 05.07, 05.08, 05.09 po 2300,00 PLN. Rachunki za energię zgodne co do grosza.
