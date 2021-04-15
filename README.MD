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