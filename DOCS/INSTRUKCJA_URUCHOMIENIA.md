# Uruchomienie skryptów:

Do uruchomienia skryptów potrzebny jest interpreter python z zainstalowanymi modułami:
>1. sqlite3
>2. csv
>3. datetime
>4. time
>5. sys
>6. re

Przykładowym interpreterem może być np. Conda, która została wykorzystana do testowania stworzonego oprogramowania.

Skrypty mogą być uruchamiane niezależnie od siebie.

# Pobieranie logów:

Aby uruchomić mechanizm pobierania logów należy uruchomić skrypt main.py, który bazuje na pliku konfiguracyjnym configuration.txt

Konfiguracja skryptu zawarta jest w pliku configuration.txt i ma jasno zdefiniowaną składnie, która pozwala na deklaracje odpowiednich serwerów, z których logi mogą być pobierane i częstotliwości samego pobierania.

Składnia pliku to para wartości <server url> <czas w sekundach>, gdzie każda para musi być umieszczona w nowej linii a wartości oddzielone są spacją.

np.

> http://localhost:3000/api 10
>
> http://localhost:3010/api 5

Tak skonfigurowany skrypt, uruchomi dwa zapytania, po jednym na każdy z adresów, co 10 sekund w przypadku pierwszego adresu i co 5 sekund w przypadku drugiego.


# Analiza logów:

Skrypt analizujący logi z pliku analyzer.py bazuje na swoim pliku konfiguracyjnym w postaci csv o nazwie analyzeConfiguration.csv.

Plik konfiguracyjny ma 11 kolumn, z których pierwsza odpowiada za mechanizm wyrażeń warunkowych if/else, a dwie ostatnie za oznaczenie wzorca pozytywnego/negatywnego i próg ilości wyników których oczekujemy. W pliku można w jednej kolumnie podać kilka wartości danego parametru oddzielając je średnikiem, np w przypadku adresu IP: 

>1.2.3.4;1.3.4.5
<hr />
W przypadku podania dwóch wartości, oznaczenie wzorca pozytywnego i negatywnego będzie odpowiednio skutkowało zapytaniem z warunkami:


>ip_addr = 1.2.3.4 OR ip_addr = 1.3.4.5 

>(NOT ip_addr = 1.2.3.4 AND NOT ip_addr = 1.3.4.5)
<hr />
Aby zaznaczyć konkretny przedział czasu należy podać początkową datę w formacie:

>10/May/2013:10:35:32+0200

Oprócz podania daty, wymagane jest podanie przedziału czasowego. Przedział czasowy możemy podać w postaci granulacji w pliku csv. Dopuszczalne wartości przedziału czasowego to: s (sekunda), m (minuta), h (godzina), d (dzień), w (tydzień).

Przykładowo, w przypadku podania daty powyżej i przedziału czasowego ‘d’, w pliku tekstowym powinniśmy mieć

>10/May/2013:10:35:32+0200,d

Tak zadeklarowane dane spowodują przedział czasowy w zapytaniu w postaci:

>date BETWEEN '10/May/2013:10:35:32+0200' AND '11/May/2013:10:35:32+0200'

Wzorce pozytywne i negatywne nie odnoszą się do dat, zawsze będziemy szukali logów z podanego odstępu czasu, niezależnie od wzorca. Możliwe jest podanie kilku wartości daty i uzyskanie kilku przedziałów czasowych o tej samej granulacji np:

>10/May/2013:10:35:32+0200;10/May/2013:10:37:32+0200,m
<hr />
Budowanie zapytań if/else opiera się o wartości w pierwszej kolumnie pliku konfiguracyjnego. 

>1. if,1.2.3.6,-,-,-,-,-,10/May/2013:10:35:32+0200,m,1,600
>2. -,-,-,-,/,404,-,10/May/2013:10:35:32+0200,m,1,5
>3. else,-,-,-,/,402,-,10/May/2013:10:35:32+0200,m,1,5
>4. -,-,-,-,/,302,-,10/May/2013:10:35:32+0200,m,1,5

Tak skonstruowana konfiguracja, sprawdzi ilość wyników zapytania w lini nr 1. Jeśli przekroczy ona 600 obiektów, do pętli w skrypcie zostanie wykorzystana linia nr 3.
Linia numer 2 zostanie użyta zamiast linii nr 3 jeśli ilość wyników nie przekroczy 600 obiektów. Linia numer 4 w tej konfiguracji będzie użyta niezależnie od wyniku linii numer 1.
W przypadku wyniku ‘true’ w linii nr 1, możliwe jest przekazanie do pętli wielu linii z konfiguracji, np:




>1. if,1.2.3.6,-,-,-,-,-,10/May/2013:10:35:32+0200,m,1,600
>2. -,-,-,-,/,404,-,10/May/2013:10:35:32+0200,m,1,5
>3. -,-,-,-,/,302,-,10/May/2013:10:35:32+0200,m,1,5
>4. else,-,-,-,/,402,-,10/May/2013:10:35:32+0200,m,1,5
<hr />
Instrukcje if/else mogą być zagnieżdżane w sobie, w przypadku pozytywnego warunku. Konfiguracja w linii else, zawsze musi być jedno linijkowa. np:

>1. if,1.2.3.4;1.3.4.5,-,-,-,-,-,10/May/2013:10:35:32+0200;10/May/2013:10:37:32+0200,m,0,3
>2. if,1.2.3.6,-,-,-,-,-,10/May/2013:10:35:32+0200,m,1,600
>3. -,-,-,-,/,404,-,10/May/2013:10:35:32+0200,m,1,5
>4. else,-,-,-,/,402,-,10/May/2013:10:35:32+0200,m,1,5
>5. -,-,-,-,/,302,-,10/May/2013:10:35:32+0200,m,1,5
>6. else,-,-,-,/,304,-,10/May/2013:10:35:32+0200,m,1,5

Jeśli zapytanie w linii pierwszej uzyska pozytywny wynik, sprawdzone będzie zapytanie w linii nr 2. Jeśli ono uzyska negatywny wynik, do pętli zapytań zostanie wzięte zapytanie z linii nr 4 a zapytanie z linii nr 3 zostanie pominięte. Zapytanie z linii nr 5 wzięte będzie do pętli niezależnie od wyniku zapytania z linii nr 2.
<hr />
Zapytania z konfiguracji, standardowo wykonywane są co 30 sekund. Aby zmienić czas wykonywania zapytań, należy podać wartość typu integer jako parametr wywołania skryptu. Przykładowe wywołanie:

> python analyzer.py 5

W takiej konfiguracji, skrypt co 5 sekund wywoła zapytania do bazy danych.

# Raporty

Raporty z danej konfiguracji, zapisywane są do pliku generatedReports.txt. Wpisy zawierają dokładne zapytanie do bazy danych, datę, ilość wyników i ilość oczekiwanych wyników. Wpis generowany jest wyłącznie w przypadku przekroczenia progu wyników oczekiwanych, podawanych w pliku konfiguracyjnym w ostatniej kolumnie, np:

>-,-,-,-,/,404,-,10/May/2013:10:35:32+0200,m,1,5

Jeżeli w bazie zostanie znalezione 5 obiektów z logami z kodem odpowiedzi 404 i scieżką dostępu ‘/’ w danym przedziale czasowym, do pliku tekstowego dołączony zostanie raport z tego zdarzenia. W przeciwnym wypadku raport nie jest generowany.
