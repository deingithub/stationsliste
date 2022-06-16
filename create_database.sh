#!/usr/bin/env bash

curl "https://download-data.deutschebahn.com/static/datasets/stationsdaten/DBSuS-Uebersicht_Bahnhoefe-Stand2020-03.csv" -o sus-stationsdaten-2020-03.csv
curl "https://download-data.deutschebahn.com/static/datasets/stationsdaten_regio/DBRNI-Uebersicht_Bahnhoefe-Stand2020-04.csv" -o rni-stationsdaten-2020-04.csv

curl "https://download-data.deutschebahn.com/static/datasets/haltestellen/D_Bahnhof_2020_alle.CSV" -o sus-haltestellen-2020.csv

curl "https://download-data.deutschebahn.com/static/datasets/bahnsteig/DBSuS-Bahnsteigdaten-Stand2020-03.csv" -o sus-bahnsteigdaten-2020-03.csv
curl "https://download-data.deutschebahn.com/static/datasets/bahnsteig_regio/DBRNI-Bahnsteigdaten_erweitert-Stand2020-04.csv" -o rni-bahnsteigdaten-2020-04.csv

sqlite3 bahnhof.sqlite3 <<EOF
.mode csv
.separator ;
.import sus-stationsdaten-2020-03.csv sus_stationsdaten
.import rni-stationsdaten-2020-04.csv rni_stationsdaten

.import sus-haltestellen-2020.csv sus_haltestellen

.import sus-bahnsteigdaten-2020-03.csv sus_bahnsteigdaten
.import rni-bahnsteigdaten-2020-04.csv rni_bahnsteigdaten

CREATE VIEW platform(bfnr, platform, track_name, length, height)
AS SELECT "Bahnhofsnummer", "Bahnsteig", "Gleisnummer", "Netto-baulänge (m)", "Höhe Bahnsteigkante (cm)""" FROM sus_bahnsteigdaten
UNION SELECT "Bf-Nr", NULL, "Bahnsteig-Nr.", "NETTOLAENGE [m]", "HOEHE [cm]" FROM rni_bahnsteigdaten
/* platform(bfnr,platform,track_name,length,height) */;

CREATE VIEW stationsdaten(regionalbereich, bahnhofsnummer, name, ds100, kategorie, strasse, plz, ort, bundesland, aufgabentraeger)
AS SELECT "RB", "Bf. Nr.", "Station", "Bf DS 100Abk.", "Kat. Vst", "Straße", "PLZ", "Ort", "Bundesland", "Aufgabenträger" FROM sus_stationsdaten
UNION SELECT "Regionalbereich", "Bf. Nr.", "Station", "Bf DS 100 Abk.", "Kategorie Vst", "Straße", "PLZ", "Ort", "Bundesland", "Aufgabenträger" FROM rni_stationsdaten
/* stationsdaten(regionalbereich,bahnhofsnummer,name,ds100,kategorie,strasse,plz,ort,bundesland,aufgabentraeger) */;

EOF
