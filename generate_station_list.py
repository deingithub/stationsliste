#!/usr/bin/env python3

import sqlite3
import argparse
import locale

LANGS = {
    "de": {
        "platform": "Bahnsteig",
        "track": "Gleis",
        "high": "hoch",
        "long": "lang",
        "notrackinfo_html": "<p>Keine Informationen zu Bahnsteigen verfügbar, sorry.</p>",
        "ds100": "DS100-Kürzel",
        "category": "Preisklasse",
        "stationid": "Bahnhofsnummer",
        "operator": "Betreiber",
        "h1": "alle bahnhöfe und haltepunkte der deutschen bahn",
        "subtitle": "nebst ihrer sich für laien in einigen fällen durchaus nicht unmittelbar erschließenden bahnsteignummerierung",
        "hints": "Hinweise",
        "hints_html": """<h2>Hinweise</h2>
        <p>Diese Seite ist automatisch generiert aus <a href="#attribution">Daten</a>, die die DB freundlicherweise zur Verfügung stellt. Sie stellt einen Soll-Zustand aus dem Jahre unseres Herrn 2020 dar, keinen aktuellen Ist-Zustand. Naja, Bahnsteige laufen nicht so schnell weg. Trotzdem: Um Vorsicht wird gebeten und Gewähr nicht übernommen.</p>
			<p>Zu jedem Bahnhof findet sich der Name (wie er auf den Schildern stehen <em>sollte</em>), so vorhanden eine Addresse und klein gedruckt verschiedene nur für Nerds interessante Kenndaten. Über den Link "db-infoscreen" findet eins aktuelle Ankünfte und Abfahrten, unter "bahnhof.de" offizielle Informationen der DB zum Bahnhof, unter anderem, ob Aufzüge vorhanden sind und funktionieren.</p>
			<p>Die grauen Balken mit den Gleisnummern drauf sind die gemeinsamen Bahnsteige. Achtung: Gelegentlich haben Bahnsteige <em>drei</em> Gleise (zwei durchgehende und ein Kopfgleis). Das Kopfgleis landet dann hier auf der Seite in einem neuen Bahnsteig, obwohl es in echt auf demselben ist. Das ist schon in den Daten der DB so falsch eingetragen und müsste für jeden bestätigten Fall manuell korrigiert werden.</p>""",
        "searchlabel": "Suche nach Stationsnamen (Nur ein Wort möglich)",
        "searchbutton": "Suchen",
        "resetbutton": "Zurücksetzen",
        "attribution_html": """<p id="attribution">Auf Basis von DB Open Data (CC BY 4.0): <a href="https://data.deutschebahn.com/dataset/data-haltestellen.html">Haltestellendaten SuS 01/2020</a>, <a href="https://data.deutschebahn.com/dataset/data-stationsdaten.html">Stationsdaten SuS 03/2020</a>, <a href="https://data.deutschebahn.com/dataset/data-stationsdaten-regio.html">Haltestellendaten RNI 04/2020</a>, <a href="https://data.deutschebahn.com/dataset/data-bahnsteig.html">Bahnsteigdaten SuS 03/2020</a> und <a href="https://data.deutschebahn.com/dataset/data-bahnsteig-regio.html">Bahnsteigdaten RNI 04/2020</a>. Diese inoffizielle Seite ohne Zusammenhang mit der DB wird Ihnen präsentiert von <span style="font-variant: small-caps;">Cass</span> Dingenskirchen, 2022. All rites reversed.</p>""",
    },
    "en": {
        "platform": "Platform",
        "track": "Track",
        "high": "high",
        "long": "long",
        "notrackinfo_html": "<p>No information on tracks and platforms, sorry.</p>",
        "ds100": "DS100",
        "category": "Category",
        "stationid": "Station Number",
        "operator": "Operator",
        "h1": "deutsche bahn's network",
        "subtitle": "including their platform numbers, frequent source of confusion and frustration to the layperson",
        "hints_html": """<h2>Hints</h2>
        <p>This page is automatically generated from <a href="#attribution">data</a> kindly provided by DB. It represents the network's intended state in the year of our Lord 2020, not today's current state. Well, platforms don't run away that fast. Nevertheless: Caution is advised and no warranties are given.</p>
			<p>For each station you can find the name (as it <em>ought</em> to be written on the actual signs), an address if available and various bits of data only interesting to nerds in fine print. Using the link "db-infoscreen" one finds current arrivals and departures, on "bahnhof.de" there is official information from DB about the station, among other things whether elevators are present and currently in operating condition.</p>
			<p>The gray bars with the track numbers on them are their shared platforms. Attention: Sometimes platforms have <em>three</em> tracks (two through tracks and one head track). On the page, the head track then ends up in a new platform, although it is on the same one in reality. This is an error in the DB data and would have to be corrected manually for each confirmed case. </p>""",
        "searchlabel": "Search for stations (one word only)",
        "searchbutton": "Search",
        "resetbutton": "Reset",
        "attribution_html": """<p id="attribution">Based on DB Open Data (CC BY 4.0): <a href="https://data.deutschebahn.com/dataset/data-haltestellen.html">Haltestellendaten SuS 01/2020</a>, <a href="https://data.deutschebahn.com/dataset/data-stationsdaten.html">Stationsdaten SuS 03/2020</a>, <a href="https://data.deutschebahn.com/dataset/data-stationsdaten-regio.html">Haltestellendaten RNI 04/2020</a>, <a href="https://data.deutschebahn.com/dataset/data-bahnsteig.html">Bahnsteigdaten SuS 03/2020</a> and <a href="https://data.deutschebahn.com/dataset/data-bahnsteig-regio.html">Bahnsteigdaten RNI 04/2020</a>. This unofficial third-party site is brought to you by <span style="font-variant: small-caps;">Cass</span> Dingenskirchen, 2022. All rites reversed.</p>""",
    },
}


def bahnhoefe():
    stationsdaten = {}
    for row in db.execute("SELECT * FROM stationsdaten;"):
        stationsdaten[row["bahnhofsnummer"]] = {
            k: row[k]
            for k in (
                "name",
                "ds100",
                "kategorie",
                "bahnhofsnummer",
                "strasse",
                "plz",
                "ort",
                "bundesland",
            )
        }

    for row in db.execute("SELECT * FROM sus_haltestellen;"):
        if row["Betreiber_Nr"] in stationsdaten:
            stationsdaten[row["Betreiber_Nr"]] |= {
                k_dict: row[k_row]
                for k_row, k_dict in (
                    ("EVA_NR", "ibnr"),
                    ("IFOPT", "ifopt"),
                    ("LAENGE", "lon"),
                    ("BREITE", "lat"),
                    ("Betreiber_Name", "betreibername"),
                )
            }
            if len(stationsdaten[row["Betreiber_Nr"]]["name"]) < len(row["NAME"]):
                stationsdaten[row["Betreiber_Nr"]]["name"] = row["NAME"]
        else:
            for bfnr, station in stationsdaten.items():
                if station["ds100"] == row["DS100"] or station["ds100"] in row[
                    "DS100"
                ].split(","):
                    stationsdaten[bfnr] |= {
                        k_dict: row[k_row]
                        for k_row, k_dict in (
                            ("EVA_NR", "ibnr"),
                            ("IFOPT", "ifopt"),
                            ("LAENGE", "lon"),
                            ("BREITE", "lat"),
                            ("Betreiber_Name", "betreibername"),
                        )
                    }
                    if len(stationsdaten[bfnr]["name"]) < len(row["NAME"]):
                        stationsdaten[bfnr]["name"] = row["NAME"]
                    break
            else:
                station = {
                    k_dict: row[k_row]
                    for k_row, k_dict in (
                        ("EVA_NR", "ibnr"),
                        ("DS100", "ds100"),
                        ("NAME", "name"),
                        ("IFOPT", "ifopt"),
                        ("LAENGE", "lon"),
                        ("BREITE", "lat"),
                        ("Betreiber_Name", "betreibername"),
                        ("Betreiber_Nr", "bahnhofsnummer"),
                    )
                }
                stationsdaten[-id(station)] = station

    return stationsdaten


def bahnhof_render(bf, lang):
    platforms_html = ""
    if platforms := db.execute(
        "SELECT DISTINCT platform FROM platform WHERE bfnr = ? ORDER BY platform",
        (bf.get("bahnhofsnummer"),),
    ):
        for platform in platforms:
            tracks = db.execute(
                "SELECT * FROM platform WHERE bfnr = ? AND platform = ?",
                (bf["bahnhofsnummer"], platform["platform"]),
            )
            platforms_html += f'<div class="platform"><h3 class="invis">{lang["platform"]} {platform["platform"]}</h3>'
            for track in tracks:
                platforms_html += f"<p><em><span>{lang['track']}  </span>{track['track_name']}</em> {track['height']}cm {lang['high']}, {track['length']}m {lang['long']} </p>"
            platforms_html += "</div>"

    if not platforms_html:
        platforms_html = lang["notrackinfo_html"]

    address_html = ""
    if "strasse" in bf.keys():
        address_html = f"<address>{bf['strasse']}, {bf['plz']} {bf['ort']}  ({bf['bundesland']})</address>"

    facts = {
        lang["ds100"]: bf["ds100"],
        lang["category"]: bf.get("kategorie"),
        lang["stationid"]: bf.get("bahnhofsnummer"),
        "IBNR": bf.get("ibnr"),
        "IFOPT": bf.get("ifopt"),
        lang["operator"]: bf.get("betreibername"),
    }
    facts_html = (
        "<p class='sm'>"
        + " | ".join([f"<b>{k}</b> {v}" for k, v in facts.items() if v])
        + "</p>"
    )
    return f"""<section data-name="{bf["name"]}">
	<h2 id="{bf["ds100"]}"><a href="#{bf["ds100"]}">{bf["name"]}</a></h2>
	{address_html}
	{facts_html}
	<a href="https://dbf.finalrewind.org/{bf["ds100"]}">db-infoscreen</a> <a href="https://www.bahnhof.de/service/search/bahnhof-de/520608?query={bf["name"]}">bahnhof.de</a>
	{platforms_html}
	</section>"""


HEADER = """<!doctype html>
			<html lang="de-DE"><head>
			<meta charset="utf-8">
			<meta property="og:title" content="DB-Stationen auf einen Blick">
			<meta name="viewport" content="width=device-width, initial-scale=1.0">
			<meta property="og:type" content="website">
			<meta property="og:url" content="https://dingenskirchen.org/bf">
			<title>need a hbf 🥺</title>
			<script src="./surreal.js"></script>
			<style>
			body { background-color: #eee; }
			main { max-width: 70ch; margin: 0 auto; font-family: 'TeX Gyre Heros', 'Futura', 'Arial', sans-serif;; }
			section h2 { background-color: #302a57; padding: .5rem 1rem .5rem .5rem; margin-bottom: 0; }
			section h2 a { color: white; text-decoration: none; }
			.platform { background-color: #aaa; padding: .5rem; margin: 0.5rem 0; border: 1px solid gray; }
			.platform p em { background: #302a57; color: white; height: 2rem; min-width: 2rem; vertical-align: middle; text-align: right; display: inline-block;
			padding: 0 .3ch; box-sizing: border-box; font-style: normal; font-weight: bold; line-height: 1.25; font-size: 1.5rem; }
			section > a { padding: .5rem; display: inline-block; background-color: #efb435; color: #302a57; font-weight: bold; text-decoration: none; }
			section > a:hover, section > a:focus { box-shadow: 3px 3px #302a57; }
			section.hide { display: none; }
			.sm { font-size: .8rem; }
			.invis, section em span { width: 1px; height: 1px; top: -900rem; position: absolute; display: block; }
			label { display: block; }
			input { width: 35ch; font-size: 1.2rem; padding: 0.5rem 0; }
			button { width: 10ch; font-size: 1.2rem; }
			</style></head>
			<body><main>
			<nav style="text-align: right;" aria-labelledby="#lang"><h2 id="#lang" style="display: inline; font-size: 1rem; font-weight: normal; font-style: italic;">Language:</h2> <b aria-current="true">DE</b> <a href="./en.html">EN</a></nav>"""


def generate():
    with open("web/index.html", "w", encoding="utf-8") as f_de, open(
        "web/en.html", "w", encoding="utf-8"
    ) as f_en:
        f_de.write(HEADER)
        f_en.write(
            HEADER.replace(
                "DB-Stationen auf einen Blick", "DB stations at a glance"
            ).replace(
                '<b aria-current="true">DE</b> <a href="./en.html">EN</a>',
                '<a href="./">DE</a> <b aria-current="true">EN</b>',
            )
        )

        for (lang, file) in ((LANGS["de"], f_de), (LANGS["en"], f_en)):
            file.write(
                f"""<h1 style="margin-bottom: 0;">{lang["h1"]}</h1>
			<p style="font-size:1.2rem; margin-top: 0;">{lang["subtitle"]}</p>
			{lang["hints_html"]}        
			<form role=search>
			    <label for="search-input">{lang["searchlabel"]}</label>
                <div style="display:flex">
			    <input type="search" id="search-input"/>
			    <button>
			        {lang["searchbutton"]}
			        <script>
			            me().on("click", ev => {{
			                halt(ev);
			                any("section").classAdd("hide");
			                any(`section[data-name *= ${{ me("#search-input").value }} i]`).classRemove("hide");
		                }})
			        </script>
			    </button>
			    
			    <button>
			        {lang["resetbutton"]}
			        <script>me().on("click", ev => {{ halt(ev); any("section").classRemove("hide"); }})</script>
			    </button>	    
			    </div>
		    	</form>"""
            )
            for bf in sorted(
                bahnhoefe().values(), key=lambda bf: locale.strxfrm(bf["name"])
            ):
                file.write(bahnhof_render(bf, lang))

            file.write(lang["attribution_html"])
            file.write("</main></body></html>")


if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, "de_DE")
    p = argparse.ArgumentParser()
    p.add_argument("database", help="database path")
    args = p.parse_args()

    db = sqlite3.connect(args.database)
    db.row_factory = sqlite3.Row
    generate()
