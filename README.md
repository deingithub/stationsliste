# DB Bahnhöfe&Haltestellen Liste

[Das Endergebnis](https://dingenskirchen.org/bf).

Aufbereitet aus einem… interessanten CSV-Format, bzw. fünf, denn die Informationen sind über fünf Dateien verteilt, alle mit unterschiedlichem Format.

Das Skript `create_database.sh` lädt die momentan aktuellsten Daten (Anfang 2020, auch über zwei Jahre nach dem Anfang von 2020) herunter und importiert sie in `bahnhof.sqlite3`.
Das Skript `generate2.py <db_path>` konvertiert die Daten aus der sqlite-Datei in den `web/` Ordner als HTML auf Englisch und Deutsch, die Ordnerstruktur muss zuerst mit `mkdir -p web/details/{en,de}` vorbereitet werden.

## Lizenzen

Die dieser Seite zugrundeliegenden Datensätze [Haltestellendaten SuS 01/2020](https://data.deutschebahn.com/dataset/data-haltestellen.html),
[Stationsdaten SuS 03/2020](https://data.deutschebahn.com/dataset/data-stationsdaten.html),
[Haltestellendaten RNI 04/2020](https://data.deutschebahn.com/dataset/data-stationsdaten-regio.html),
[Bahnsteigdaten SuS 03/2020](https://data.deutschebahn.com/dataset/data-bahnsteig.html) und
[Bahnsteigdaten RNI 04/2020](https://data.deutschebahn.com/dataset/data-bahnsteig-regio.html)
gehören der Deutschen Bahn und wurden allesamt von ihr freundlicherweise unter der Lizenz [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/) frei zur Verfügung gestellt.

Das Webinterface nutzt [surreal](https://github.com/gnat/surreal) für die interaktive Suche. Dieses ist hier mitgeliefert und unter der MIT-Lizenz verfügbar.

