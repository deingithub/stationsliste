import itertools
import re
from helpers import deutsch_2_float
from patch3 import patched


def extract_stations(db):
    "Merge the three data sources for station data into one big python list"

    stations = []

    # stations with entries in both xxx_stationsdaten and haltestellen
    for row in db.execute(
        """SELECT haltestellen.Betreiber_Nr as bfnr, stationsdaten.name, stationsdaten.regionalbereich,
        stationsdaten.kategorie, stationsdaten.strasse, stationsdaten.plz, stationsdaten.ort, stationsdaten.bundesland,
        stationsdaten.aufgabentraeger, group_concat(haltestellen.DS100, "|") as ds100s,
        group_concat(haltestellen.NAME, "|") as names, group_concat(haltestellen.EVA_NR, "|") as ibnrs,
        group_concat(haltestellen.IFOPT, "|") as ifopts, group_concat(haltestellen.Verkehr, "|") as verkehrs,
        group_concat(haltestellen.LAENGE, "|") as lons, group_concat(haltestellen.BREITE, "|") as lats,
        group_concat(haltestellen.Betreiber_Name, "|") as betreiber_names
        FROM haltestellen
        JOIN stationsdaten ON stationsdaten.bahnhofsnummer = bfnr
        WHERE Betreiber_Nr != "" AND Betreiber_Nr != 0
        GROUP BY Betreiber_Nr;"""
    ):
        ds100s, names, ibnrs, ifopts, verkehrs, lons, lats, betreiber_names = (
            row["ds100s"].split("|"),
            row["names"].split("|"),
            row["ibnrs"].split("|"),
            row["ifopts"].split("|"),
            row["verkehrs"].split("|"),
            row["lons"].split("|"),
            row["lats"].split("|"),
            row["betreiber_names"].split("|"),
        )
        stations.append(
            {
                "bfnr": int(row["bfnr"]),
                "name": row["name"],
                "regionalbereich": row["regionalbereich"],
                "kategorie": row["kategorie"],
                "strasse": row["strasse"],
                "plz": row["plz"],
                "ort": row["ort"],
                "bundesland": row["bundesland"],
                "aufgabentraeger": row["aufgabentraeger"],
                "subs": [
                    {
                        "ds100": ds100s[i].strip(),
                        "name": names[i].strip(),
                        "ibnr": int(ibnrs[i]),
                        "ifopt": ifopts[i].strip(),
                        "verkehr": verkehrs[i].strip(),
                        "lat": deutsch_2_float(lats[i]),
                        "lon": deutsch_2_float(lons[i]),
                        "betreiber_name": betreiber_names[i].strip(),
                    }
                    for i in range(len(names))
                ],
            }
        )

    # stations with an entry in haltestellen but not xxx_stationsdaten (usually third-party stops)
    for row in db.execute(
        """SELECT DS100, EVA_NR, NAME, IFOPT, Verkehr, Laenge, Breite, Betreiber_Name
        FROM haltestellen
        WHERE Betreiber_Nr = "" OR Betreiber_Nr = 0;"""
    ):
        name = row["NAME"].strip()
        stations.append(
            {
                "bfnr": None,
                "name": name,
                "regionalbereich": None,
                "kategorie": None,
                "strasse": None,
                "plz": None,
                "ort": None,
                "bundesland": None,
                "aufgabentraeger": None,
                "subs": [
                    {
                        "ds100": row["DS100"].strip(),
                        "name": name,
                        "ibnr": int(row["EVA_NR"]),
                        "ifopt": row["IFOPT"],
                        "verkehr": row["Verkehr"],
                        "lat": deutsch_2_float(row["Breite"]),
                        "lon": deutsch_2_float(row["Laenge"]),
                        "betreiber_name": row["Betreiber_Name"],
                    }
                ],
            }
        )

    # stations with an entry in xxx_stationsdaten but not haltestellen (db what are you doing)
    for row in db.execute(
        """SELECT * FROM stationsdaten
        JOIN bfnr_nichtinstationsdaten ON bfnr_nichtinstationsdaten.bahnhofsnummer = stationsdaten.bahnhofsnummer
        ORDER BY name;"""
    ):
        name = row["name"].strip()
        stations.append(
            {
                "name": name,
                "bfnr": int(row["bahnhofsnummer"]),
                "regionalbereich": row["regionalbereich"],
                "kategorie": row["kategorie"],
                "strasse": row["strasse"],
                "plz": row["plz"],
                "ort": row["ort"],
                "bundesland": row["bundesland"],
                "aufgabentraeger": row["aufgabentraeger"],
                "subs": [
                    {
                        "ds100": row["ds100"].strip(),
                        "name": name,
                        "ibnr": None,
                        "ifopt": None,
                        "verkehr": None,
                        "lat": None,
                        "lon": None,
                        "betreiber_name": None,
                    }
                ],
            }
        )

    # we now have a list, but it has a few duplicates because some stations are listed both in xxx_stationsdaten
    # and haltestellen but don't have a dataset station number (Betreiber_Nr/bahnhofsnummer). in the first query
    # we excluded those even if we could match them up otherwise to avoid even worse duplication issues, now we
    # can reunite those datasets!

    # first, we'll reunite based on the stations having the same name (casefolded and only letters counted)
    cleaned_stations_1 = []
    sort_by_name = lambda station: re.sub("[^a-z]", "", station["name"].casefold())
    for _, items in itertools.groupby(
        sorted(stations, key=sort_by_name), key=sort_by_name
    ):
        items = list(items)
        if len(items) == 1:
            cleaned_stations_1.append(items[0])
        elif len(items) == 2:
            cleaned_stations_1.append(
                {k: v or items[1][k] for k, v in items[0].items()}
            )
            if not cleaned_stations_1[-1]["subs"][0]["ibnr"]:
                cleaned_stations_1[-1]["subs"] = items[1]["subs"]
        else:
            raise Exception(
                "wow they managed to have a three-way broken dataset, implement this"
            )

    # and finally, we'll reunite the last remaining (i hope, at least) duplicates by matching the DS100 abbreviations
    cleaned_stations_2 = []
    sort_by_ds100 = lambda station: station["subs"][0]["ds100"]
    for _, items in itertools.groupby(
        sorted(cleaned_stations_1, key=sort_by_ds100), key=sort_by_ds100
    ):
        items = list(items)
        if len(items) == 1:
            cleaned_stations_2.append(items[0])
        elif len(items) == 2:
            cleaned_stations_2.append(
                {k: v or items[1][k] for k, v in items[0].items()}
            )
            if not cleaned_stations_2[-1]["subs"][0]["ibnr"]:
                cleaned_stations_2[-1]["subs"] = items[1]["subs"]
        else:
            raise Exception(
                "wow they managed to have a three-way broken dataset, implement this"
            )

    for station in cleaned_stations_2:
        station["platforms"] = [
            dict(row)
            for row in db.execute(
                "SELECT * FROM bahnsteigdaten WHERE bahnhofsnummer = ? ORDER BY bahnsteig, gleis",
                (station["bfnr"],),
            ).fetchall()
        ]
        station = patched(station)

    return cleaned_stations_2
