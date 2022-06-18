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

.import sus-haltestellen-2020.csv haltestellen

.import sus-bahnsteigdaten-2020-03.csv sus_bahnsteigdaten
.import rni-bahnsteigdaten-2020-04.csv rni_bahnsteigdaten

/*
	bahnsteigdaten(bahnhofsnummer, bahnsteig, gleis, laenge, hoehe)
	RegioNetz-Datensatz hat einfach keine Bahnsteigangaben, deswegen dichten wir jedem Gleis seinen eigenen dazu.
*/
CREATE VIEW bahnsteigdaten(quelle, bahnhofsnummer, bahnsteig, gleis, laenge, hoehe)
AS SELECT "sus", "Bahnhofsnummer", "Bahnsteig", "Gleisnummer", "Netto-baulänge (m)", "Höhe Bahnsteigkante (cm)""" FROM sus_bahnsteigdaten
UNION SELECT "rni", "Bf-Nr", rowid, "Bahnsteig-Nr.", "NETTOLAENGE [m]", "HOEHE [cm]" FROM rni_bahnsteigdaten;

/*
	stationsdaten(regionalbereich,bahnhofsnummer,name,ds100,kategorie,strasse,plz,ort,bundesland,aufgabentraeger)
	
	Die gemeinsamen Spalten von sus_stationsdaten und rni_stationsdaten.
*/

CREATE VIEW stationsdaten(quelle, regionalbereich, bahnhofsnummer, name, ds100, kategorie, strasse, plz, ort, bundesland, aufgabentraeger)
AS SELECT "sus", "RB", "Bf. Nr.", "Station", "Bf DS 100Abk.", "Kat. Vst", "Straße", "PLZ", "Ort", "Bundesland", "Aufgabenträger" FROM sus_stationsdaten
UNION SELECT "rni", "Regionalbereich", "Bf. Nr.", "Station", "Bf DS 100 Abk.", "Kategorie Vst", "Straße", "PLZ", "Ort", "Bundesland", "Aufgabenträger" FROM rni_stationsdaten;

CREATE VIEW bfnr_nichtinstationsdaten AS SELECT bahnhofsnummer from stationsdaten except select Betreiber_Nr from haltestellen;


EOF
