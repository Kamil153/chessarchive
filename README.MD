# Chess Archive
## Autorzy
- Damian Cyper
- Kamil Polak
## Opis
Projekt jest aplikacją webową, która obsługuje bazę danych dla archiwum partii szachowych. Będzie zawierała takie informacje jak: nicki obu grających stron, kolor którą grała każda ze stron, tempo gry, wszystkie posunięcia w partii, ranking obu graczy, datę rozegrania partii. Dodatkowo do każdej z partii możliwe będzie dodanie własnej notatki (uwag na temat gry). Dane zgromadzone w bazie będzie można przeszukiwać wpisując nick jednego z graczy lub wykorzystując dostępne filtry wyszukiwania: określony przedział czasu, przedział rankingu obu graczy, wpisanie konkretnego tempa gry lub podanie pierwszego ruchu. Oprócz tego będzie możliwość sortowania zgromadzonych danych m.in po dacie, rankingu. Projekt zakłada możliwość utworzenia konta przez użytkownika. Każdy użytkownik może założyć swoje prywatne archiwum, do którego inni użytkownicy nie mają dostępu.
## Technologie
- PostgreSQL - system bazy danych
- Django - web framework
- Django ORM - system mapowania obiektowo-relacyjnego

## Instrukcja uruchomienia w Dockerze

1. Pobrać repozytorium na dysk
```shell
git clone https://github.com/Kamil153/chessarchive.git && cd chessarchive
```
2. Stworzyć w głównym katalogu plik .env z danymi potrzebnymi do połączenia z bazą danych według poniższego wzoru
```shell
touch .env
```
```
DB_NAME=nazwabazy
DB_USER=uzytkownik
DB_PASSWORD=haslo
DB_HOST=example.com
DB_PORT=5432
```
3. Zbudować obraz
```shell
docker build --tag chessarchive .
```
4. Zastosować do bazy danych migracje
```shell
docker run --env-file ./.env -p 8000:8000 chessarchive python manage.py migrate
```
5. Uruchomić serwer
```shell
docker run --env-file ./.env -p 8000:8000 chessarchive
```

## Schemat bazy danych

![schematBazy](schematBazy.png)

## Opis tabel

1. Użytkownicy_aplikacji - tabela wszystkich użytkowników korzystających z aplikacji webowej
2. Tempa_gry - tabela wszystkich możliwych temp gry. Jeżeli podanego przez użytkownika tempa gry w danej partii nie ma w tabeli to jest ona dodawana automatycznie do bazy.
3. Partie - tabela wszystkich partii w systemie. Zbiera partie wszystkich użytkowników w jedną tabelę.
4. Szczegóły_gracza - tabela zbierająca informacje na temat gracza aktualne w danej partii.
5. Ruchy - tabela informująca o ruchach w partii.
6. Gracze - tabela zbierająca informacje o wprowadzonych graczach partii. Tabela zbiera w jedną tabelę wszystkich graczy wprowadzonych przez wszystkich użytkowników systemu
7. Znajomi - tabela zawierająca informacje na temat listy znajomych każdego użytkownika
8. Zaproszenia - tabela gromadząca wszystkie oczekujące zaproszenie do dołączenia do grona znajomych (oczekują tam wszystkie zaproszenia które nie zostały ani zaakceptowane ani odrzucone)


## Przegląd aplikacji

1. Użytkownik niezalogowany ma jedynie możliwość zalogowania się lub założenia konta. Pokazany widok można znaleźć w kodzie tutaj:
https://github.com/Kamil153/chessarchive/blob/0fc1606e74d173583c63559b3cf16d01bc774cca/archive/templates/home.html#L21

   ![not_logged](screens/not_logged.png)

2. Użytkownik może zalogować się. Ta funkcjonalność (oraz pozostałe funkcjonalności dotyczące rejestracji, resetowania hasła) została zaimplementowana tutaj: https://github.com/Kamil153/chessarchive/tree/master/templates/registration

   ![log_in](screens/log_in.png)

3. Może również założyć nowe konto

   ![sign_up](screens/sign_up.png)

4. Ma również możliwość resetowania hasła

   ![reset](screens/reset.png)

5. Po zalogowaniu użytkownik widzi stronę domową (administrator ma dodatkowe pole "Settings", którego nie widzi każdy inny użytkownik bez uprawnień).
   Widok html implementujacy stronę domową można znaleźć tutaj: https://github.com/Kamil153/chessarchive/blob/master/archive/templates/home.html
   Obsługa tego i innych widoków została zaimplementowana w pliku views.py (https://github.com/Kamil153/chessarchive/blob/master/archive/views.py)

   ![home](screens/home.png)

6. Użytkownik może edytować informacje takie jak adres email oraz nazwa użytkownika. Może również zmienić hasło (zostanie przeniesiony na widok nr 4)
   https://github.com/Kamil153/chessarchive/blob/master/archive/templates/profile.html
   https://github.com/Kamil153/chessarchive/blob/0fc1606e74d173583c63559b3cf16d01bc774cca/archive/views.py#L25
   
   ![edit](screens/edit.png)

7. Każdy zalogowany użytkownik ma opcję dodania nowej partii do swojej bazy
   https://github.com/Kamil153/chessarchive/blob/master/archive/templates/add_game.html
   https://github.com/Kamil153/chessarchive/blob/0fc1606e74d173583c63559b3cf16d01bc774cca/archive/views.py#L86
   ![add_view](screens/add_view.png)

8. Może również zobaczyć całe swoje archiwum
   https://github.com/Kamil153/chessarchive/blob/master/archive/templates/list.html
   https://github.com/Kamil153/chessarchive/blob/0fc1606e74d173583c63559b3cf16d01bc774cca/archive/views.py#L35
   ![archive_view](screens/archive_view.png)

9. Ma też dostęp do dokładniejszych informacji każdej z partii
   https://github.com/Kamil153/chessarchive/blob/master/archive/templates/details.html
   https://github.com/Kamil153/chessarchive/blob/0fc1606e74d173583c63559b3cf16d01bc774cca/archive/views.py#L149
   ![details](screens/details.png)

10. Funkcjonalność bazy danych w programie pgAdmin4
   ![baza1](screens/baza1.png)
   ![baza2](screens/baza2.png)
   ![baza3](screens/baza3.png)
   ![baza4](screens/baza4.png)
   ![baza5](screens/baza5.png)
   ![baza6](screens/baza6.png)
   ![baza7](screens/baza7.png)
   ![baza8](screens/baza8.png)
   ![baza9](screens/baza9.png)