# Analiza logów i raportowanie zdarzeń

## Wprowadzenie

Projekt składa się z trzech głównych części: pozyskiwania logów z zewnętrznego serwera, analizy tych logów oraz przygotowania raportu w formie pliku tekstowego. Ma za zadanie wychwytywać podejrzane zdarzenia i ostrzec w ten sposób użytkownika przed zagrożeniami dla systemu. 

## Zakres projektu

Dostęp do zewnętrznego serwera możliwy jest za pomocą http. Następnie logi są pobierane w formie pliku tekstowego. Zarówno częstotliwość pobierania jak i adres url serwera można wybrać i dostosować do swoich potrzeb. 

Analiza logów, która jest złożonym problemem została skonfigurowana tak, aby użytkownik mógł sam ustawić parametry wykrywania zdarzeń. W pliku tekstowym można ustawić konfigurację, między innymi za pomocą warunków if-else, wzorców pozytywnych i negatywnych. Można wybrać adres url serwera, metodę, ścieżkę, kod odpowiedzi, wersję http, datę z granulacją i liczbę wystąpień. Konfiguracja pozwala na wskazywanie kilku wartości dla danej zmiennej oraz umożliwia pominięcie niektórych z nich. Wspierane jest wiele formatów logów takich jak:
>- apache
>- nginx
>- iis
>- http
>- NSCA access logs
>- elb

Jeżeli zostały wykryte logi w liczbie przewyższającej podaną w konfiguracji, które spełniają jej warunki, do pliku tekstowego generowany jest raport. Zawiera on liczbę obiektów, które spełniały warunki podane w konfiguracji i zapytanie, którym zostały one odfiltrowane.

## Wykorzystane technologie

Przy wyborze języka oprogramowania analizowaliśmy głównie dwie opcję Javę oraz Pythona. Finalnie został wybrany Python ze względu na jego przystępną składnię, wydajność oraz możliwość uruchomienia w postaci skryptu, bez konieczności generowania gotowych do instalacji paczek.

## Opis metodyki prowadzonych prac

Prace przeprowadzone zostały w metodyce Waterfall. Wybrana została ona, gdyż już na samym początku było wiadomo jakie są wymagania co do oczekiwanego produktu oraz co ma on zawierać. Od początku znany był również termin. Projekt był zaplanowany, podzielony na etapy realizacji i na końcu przetestowany, aby sprawdzić, czy nie pojawiły się błędy. Ze względu na krótki czas realizacji, niewielki zespół i jasno określone wymagania waterfall okazał się odpowiednim wyborem.

## Rezultaty testów

Zostały przeprowadzone testy jednostkowe sprawdzające logikę systemu. Przetestowany został parser logów, który zwraca dane w formacie umożliwiającym ich analizę. Kolejne testy sprawdzały poprawność tworzonych i wysyłanych zapytań SQL. Dodatkowo przeprowadzone zostały testy manualne, które potwierdziły działanie systemu i zgodność z wymaganiami projektu.

## Podsumowanie

Udało się przygotować produkt, który w poprawny sposób analizuje wiele dostępnych formatów logów. Produkt jest konfigurowalny przez użytkownika, można dostosować go do własnych potrzeb. Rodzaj raportu jest narzucony z góry, jednak zapewnia czytelność i możliwość zastosowania własnego filtru bądź skryptu na pliku zawierającym logi, co pozwala łatwe dalsze rozwijanie produktu. Wygenerowany plik pozwala na śledzenie z określonym odstępem czasu liczby obiektów, które potencjalnie mogą stanowić zagrożenie.

Ze względu na ograniczone ramy czasowe nie udało się przygotować dostępu do serwera za pomocą innych protokołów niż http takich jak ssh czy ftp, co również spowodowało brak zastosowania mechanizmu autoryzacji pobrania logów.
