# Architektura systemu

System pobierania i analizy logów składa się z dwóch skryptów w języku python, z których pierwszy ma za zadanie pobrać logi, używając parsera przeprowadzić ekstrakcję danych w nich zawartych i wykorzystując połączenie z bazą danych umieścić je w tabeli z logami. Przepływ danych przebiega przez interfejs HTTP w postaci zapytania, które pobiera dane, następnie dane są przetwarzane przez moduł logParser i zwracane do wpisania do bazy danych.

Drugi skrypt, niezależnie od uruchomienia pierwszego, przeprowadza na podstawie konfiguracji dołączonej do projektu analizę logów zawartych w bazie danych. Na podstawie odczytanej konfiguracji z pliku CSV, moduł budujący zapytania SQL o nazwie queryBuilder zwraca odpowiednie warunki zapisane w postaci stringów, które następnie wywoływane są przez połączenie z bazą danych. Otrzymane dane porównywane są ilościowo z deklarowanymi wartościami zawartymi w pliku konfiguracyjnym. Po porównaniu, wyniki są sprawdzane i jeśli spełnione zostały warunki, generowany jest poprzez interfejs obsługi plików tekstowych raport.

# Moduły

### Moduł budowania zapytań SQL:

Moduł odpowiada za generowanie zapytań SQL na podstawie dołączonej konfiguracji w pliku tekstowym. Posiada on metody odpowiadające za analizę i konwertowanie jednej linijki pliku konfiguracyjnego na szereg warunków odpowiadających zapisanej konfiguracji. Po utworzeniu zapytania, jest ono zwracane przez moduł do skryptu i uruchamiane w bazie danych

### Moduł parsowania logów:

Moduł odpowiadający za ekstrakcję danych z różnych rodzajów logów, które są wspierane przez rozwiązanie. Aby poprawnie odczytywać dane, moduł zawiera wsparcie wyrażeń regularnych (regexp), które odpowiednio dopasowane są do różnych możliwości zapisu zdarzeń w logach. Moduł pozwala na wyciągnięcie wartości takich jak: adres ip wysyłającego zapytanie, metodę HTTP, ścieżkę zapytania, kod odpowiedzi, wersje http oraz datę zdarzenia. Po ekstrakcji dane są zwracane do skryptu umieszczającego dane w bazie.

### Moduł testów: 

Aby zapewnić pewność odpowiedniego działania został przygotowany moduł testów, który sprawdza moduły parsowania logów i budowania zapytań SQL w celu wychwycenia błędów i zapewnienia punktu odniesienia po wprowadzeniu zmian w projekcie. Bazuje on na pythonowym unittest i sprawdza zarówno podstawowe jak i rozszerzone przypadki testowe.


# Interfejsy
Moduł parsowania logów zawiera interfejs wywołujący mechanizm przetwarzania w postaci funkcji, która jako argument przyjmuje jedną wartość, którą jest String zawierający dane z jednej linijki z logami a na wyjściu zwraca 6 wartości, które wstawiane są do bazy danych (adres ip wysyłającego zapytanie, metodę HTTP, ścieżkę zapytania, kod odpowiedzi, wersje http oraz datę zdarzenia)

Moduł budowania zapytań SQL wystawia jeden interfejs w postaci funkcji, która jako parametry wejściowe przyjmuje jedną linijkę pliku konfiguracyjnego oraz tablicę zawierającą nazwy kolumn pliku konfiguracyjnego CSV. Na wyjściu zwraca ona krotkę, zawierającą zapytanie SQL w postaci String i ilość obiektów zapisanych jako ilość oczekiwana w konfiguracji.
