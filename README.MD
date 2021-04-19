# Chess Archive
## Autorzy
- Damian Cyper
- Kamil Polak
## Opis
Projekt jest aplikacją webową, która obsługuje bazę danych dla archiwum partii
szachowych. Będzie zawierała takie informacje jak: nicki obu grających stron, kolor
którą grała każda ze stron, tempo gry, kilka pierwszych posunięć, ranking obu
graczy, datę rozegrania partii, link do analizy komputerowej na jednej ze stron
poświęconych szachom takich jak chess.com lub lichess.org. Dodatkowo do
każdej z partii możliwe będzie dodanie własnej notatki (uwag na temat gry). Dane
zgromadzone w bazie będzie można przeszukiwać wpisując nick jednego z
graczy lub wykorzystując dostępne filtry wyszukiwania: określony przedział czasu,
przedział rankingu obu graczy, wpisanie konkretnego tempa gry lub podanie
pierwszego ruchu. Oprócz tego będzie możliwość sortowania zgromadzonych
danych m.in po dacie, rankingu.
Projekt zakłada możliwość utworzenia konta przez użytkownika. Każdy
użytkownik może założyć swoje prywatne archiwum, do którego inni użytkownicy
nie mają dostępu.
## Technologie
- PostgreSQL - system bazy danych
- Django - web framework
- Django ORM - system mapowania obiektowo-relacyjnego

## Schemat bazy danych

![schematBazy](C:\Users\Damian Cyper\PycharmProjects\chessarchive\schematBazy.png)

## Opis tabel

1. Użytkownicy aplikacji - tabela wszystkich użytkowników korzystających z aplikacji webowej
2. Tempa gry - tabela wszystkich możliwych temp gry. Jeżeli podanego przez użytkownika tempa gry w danej partii nie ma w tabeli to jest ona dodawana automatycznie do bazy.
3. Partie - tabela wszystkich partii w systemie. Zbiera partie wszystkich użytkowników w jedną tabelę.
4. Szczegóły gracza - tabela zbierająca informacje na temat gracza aktualne w danej partii.
5. Ruchy w partii - tabela informująca o ruchach w partii.
6. Gracze - tabela zbierająca informacje o wprowadzonych graczach partii. Tabela zbiera w jedną tabelę wszystkich graczy wprowadzonych przez wszystkich użytkowników systemu
7. Gracze_nick - tabela będąca rozszerzeniem tabeli Gracze. Przechowuje dodatkową informację na temat nicku gracza.
8. Gracze_imie - tabela będąca rozszerzeniem tabeli Gracze. Przechowuje dodatkową informację na temat imienia i nazwiska gracza danej partii. Jeżeli użytkownik poda nick danego gracza to nie może podać imienia i nazwiska (i vice versa)