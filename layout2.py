from string import Template

LANG = {
    "de": {
        "lang": "de",
        "ogtitle": "Alle DB-Stationen auf einen Blick",
        "lang_links_html": '<b aria-current="true">DE</b> <a href="./en.html">EN</a>',
        "h1": "alle bahnhöfe und haltepunkte der deutschen bahn",
        "subtitle": "nebst ihrer sich für laien in einigen fällen durchaus nicht unmittelbar erschließenden bahnsteignummerierung",
        "hints_html": """<h2>Hinweise</h2>
        <p>Diese Seite ist automatisch generiert aus <a href="#attribution">Daten</a>, die die DB freundlicherweise zur Verfügung stellt. Sie stellt einen Soll-Zustand aus dem Jahre unseres Herrn 2020 dar, keinen aktuellen Ist-Zustand. Naja, Bahnsteige laufen nicht so schnell weg. Trotzdem: Um Vorsicht wird gebeten und Gewähr nicht übernommen.</p>
			<p>Zu jedem Bahnhof findet sich der Name (wie er auf den Schildern stehen <em>sollte</em>), so vorhanden eine Addresse und klein gedruckt verschiedene nur für Nerds interessante Kenndaten. Über den Link "db-infoscreen" findet eins aktuelle Ankünfte und Abfahrten, unter "bahnhof.de" offizielle Informationen der DB zum Bahnhof, unter anderem, ob Aufzüge vorhanden sind und funktionieren.</p>
			<p>Die grauen Balken mit den Gleisnummern drauf sind die gemeinsamen Bahnsteige. <strong>Achtung:</strong> Gelegentlich haben Bahnsteige mehr als zwei Gleise (z.B. zwei durchgehende Gleise und ein Kopfgleis). Das Kopfgleis landet dann in Einzelfällen hier auf der Seite in einem neuen Bahnsteig, obwohl es in echt auf demselben ist. Das ist schon in den Daten der DB so falsch eingetragen und müsste für jeden bestätigten Fall manuell korrigiert werden.</p>""",
        "searchlabel": "Suche nach Stationen",
        "searchbutton": "Suchen",
        "resetbutton": "Löschen",
        "attributionbased": "Auf Basis von DB Open Data (CC BY 4.0):",
        "and": "und",
        "github": """Der Quelltext dieser Seiten ist auf <a href="https://github.com/deingithub/stationsliste">Github</a> einsehbar.""",
        "me_html": """Diese inoffizielle Seite ohne Zusammenhang mit der DB wird Ihnen präsentiert von <span style="font-variant: small-caps;">Cass</span> Dingenskirchen, 2022. All rites reversed.</p>""",
        "ds100": "DS100-Kürzel",
        "kategorie": "Preisklasse",
        "ifopt": "IFOPT",
        "ibnr": "IBNR",
        "verkehr": "Verkehr",
        "betreiber_name": "Betreiber",
        "rni_warn_html": "<p>Station von DB RegioNetz: Keine Daten dazu, welche Bahnsteige gemeinsam sind.</p>",
        "platform": "Bahnsteig",
        "track": "Gleis",
        "high": "hoch",
        "long": "lang",
        "notrackinfo_html": "<p>Keine Informationen zu Bahnsteigen verfügbar, sorry.</p>",
        "also": "auch:",
        "linklist_hint_html": '<p>Um die Bahnhofsdetails zu sehen, einfach auf den Namen klicken. Eine Liste mit allen Details zu allen Bahnhöfen auf einmal ist auch verfügbar, aber sehr groß. Falls lange Lade- und Aufbauzeiten kein Problem sind, findet sich hier <a href="./complete.html">die vollständige Liste</a>.</p>',
        "patches": "Durchgeführte Korrekturen",
    },
    "en": {
        "lang": "en",
        "ogtitle": "DB stations at a glance",
        "lang_links_html": '<a href="./">DE</a> <b aria-current="true">EN</b>',
        "h1": "deutsche bahn's network",
        "subtitle": "including their platform numbers, frequent source of confusion and frustration to the layperson",
        "hints_html": """<h2>Hints</h2>
        <p>This page is automatically generated from <a href="#attribution">data</a> kindly provided by DB. It represents the network's intended state in the year of our Lord 2020, not today's current state. Well, platforms don't run away that fast. Nevertheless: Caution is advised and no warranties are given.</p>
			<p>For each station you can find the name (as it <em>ought</em> to be written on the actual signs), an address if available and various bits of data only interesting to nerds in fine print. Using the link "db-infoscreen" one finds current arrivals and departures, on "bahnhof.de" there is official information from DB about the station, among other things whether elevators are present and currently in operating condition.</p>
			<p>The gray bars with the track numbers on them are their shared platforms. <strong>Attention:</strong> Sometimes platforms have more than two tracks (e.g. two through tracks and one head track). On the page, the head track might in some cases end up on a new platform, although it is on the same one in reality. This is an error in the DB data and would have to be corrected manually for each confirmed case. </p>""",
        "searchlabel": "Search for stations",
        "searchbutton": "Search",
        "resetbutton": "Reset",
        "attributionbased": "Based on DB Open Data (CC BY 4.0):",
        "and": "and",
        "github": """This site's source is available on <a href="https://github.com/deingithub/stationsliste">Github</a>.""",
        "me_html": """This unofficial third-party site is brought to you by <span style="font-variant: small-caps;">Cass</span> Dingenskirchen, 2022. All rites reversed.</p>""",
        "ds100": "DS100",
        "kategorie": "Category",
        "ifopt": "IFOPT",
        "ibnr": "IBNR",
        "verkehr": "Distance",
        "betreiber_name": "Operator",
        "rni_warn_html": "<p>DB RegioNetz station: No data about which platforms are shared.</p>",
        "platform": "Platform",
        "track": "Track",
        "high": "high",
        "long": "long",
        "notrackinfo_html": "<p>No information on tracks and platforms, sorry.</p>",
        "also": "also listed as:",
        "linklist_hint_html": """<p>Too see a station's details, simply click on its name. There's also a pre-expanded list with details for all stations available, but it's rather large. If long loading and rendering times aren't an issue, the  <a href="./complete.html">complete list</a> is available here, though with German text only.</p>""",
        "patches": "Data includes these corrections",
    },
}

LAYOUT_TOP = Template(
    """
<!doctype html>
<html lang="$lang">
<head>
    <meta charset="utf-8">
    <meta property="og:title" content="$ogtitle">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://dingenskirchen.org/bf">
    <title>need a hbf 🥺</title>
    <script src="./surreal.js"></script>
    <style>
    body { background-color: #eee; }
    main { max-width: 70ch; margin: 0 auto; font-family: 'TeX Gyre Heros', 'Futura', 'Arial', sans-serif;; }
    section h2, main > ul li > a { font-size: 1.5rem; font-weight: bold; display: block; background-color: #302a57; padding: .5rem 1rem .5rem .5rem; margin-bottom: 0; }
    section h2 a, main > ul li > a { color: white; text-decoration: none; }
    address { margin-bottom: 0.75rem; }
    .platform { background-color: #aaa; padding: .5rem; margin: 0.5rem 0; border: 1px solid gray; }
    .platform p em { background: #302a57; color: white; height: 2rem; min-width: 2rem; vertical-align: middle; text-align: right; display: inline-block; padding: 0 .3ch; box-sizing: border-box; font-style: normal; font-weight: bold; line-height: 1.25; font-size: 1.5rem; }
    .platform h3 { font-size: 3rem; float: right; line-height: 1; margin: 0; color: #666; }
    .button-row a { padding: .5rem; display: inline-block; background-color: #efb435; color: #302a57; font-weight: bold; text-decoration: none; margin-bottom: 0.3rem; }
    .button-row a:hover, .button-row a:focus { box-shadow: 3px 3px #302a57; }
    .hide { display: none; }
    .sm { font-size: .8rem; }
    .invis, section em span { width: 1px; height: 1px; top: -900rem; position: absolute; display: block; }
    label { display: block; }
    input { flex-grow: 1; min-width: 10ch; font-size: 1.2rem; padding: 0.5rem 0; }
    button { font-size: 1.2rem; }
    main > ul li { margin: 1rem 0; }
    main > ul { list-style: none; padding-left: 0; }
    main > ul li section h2 { margin-top: 0; }
    li.loading::before {
	display: block;
	width: calc( 70ch / 1.5 );
	content: "⏳";
	background: rgba(100,100,100,0.5);
	height: calc( 3rem + 3px );
	position: absolute;
	text-align: center;
	font-size: 1.5rem;
	line-height: 2;
	max-width: calc( 100vw - 2rem );
}
    @media screen and (max-width: 80ch) {
        body > main { max-width: unset; margin: 0 0.5rem;}
        body { overflow-x: hidden;}
    }
    </style>
</head>
<body>
    <main>
        <nav style="text-align: right;" aria-labelledby="#lang">
            <h2 id="#lang" style="display: inline; font-size: 1rem; font-weight: normal; font-style: italic;">Language:</h2>
            $lang_links_html
        </nav>
        <h1 style="margin-bottom: 0;">$h1</h1>
        <p style="font-size:1.2rem; margin-top: 0;">$subtitle</p>
        $hints_html"""
)

LAYOUT_LINKLIST_PREFIX = Template(
    """
    $linklist_hint_html
    <script>
        // poor person's htmx
        onloadAdd(_ => any("li>a").on("click", async ev => {
            halt(ev);
            parent = me(ev.target.parentNode);
            parent.classAdd("loading");
            resp = await fetch(me(ev).pathname);
            parent.innerHTML = await resp.text();
            if (window.location.hash == "#" + parent.id) {
                parent.scrollIntoView();
            } else {
                history.pushState({}, '', "#" + parent.id);
            }
            parent.classRemove("loading");
        }));
        onloadAdd(_ => {
            if (window.location.hash) {
                me(
                    "a",
                    start=document.getElementById(
                        window.location.hash.substring(1)
                    )
                ).trigger("click");
            }
        });
    </script>
    <form role=search>
            <label for="search-input">$searchlabel</label>
            <div style="display:flex">
                <input type="search" id="search-input"/>
                
                <button>
                    $searchbutton
                    <script>
                        me().on("click", ev => {
                            halt(ev);
                                any("main > ul li").classAdd("hide").run(el => {
                                    if (el.textContent.toLowerCase().includes(me("#search-input").value.toLowerCase())) {
                                        me(el).classRemove("hide");
                                    }
                                });
                        });
                    </script>
                </button>

                <button id="reset-button">
                    $resetbutton
                    <script>
                        me().on("click", ev => {
                            halt(ev);
                            any("main > section, main > ul li").classRemove("hide");
                            me("#search-input").value = "";
                        });
                    </script>
                </button>	    
            </div>
        </form><ul>"""
)
LAYOUT_LINKLIST_SUFFIX = "</ul>"

LAYOUT_BOTTOM = Template(
    """<p id="attribution">$attributionbased <a href="https://data.deutschebahn.com/dataset/data-haltestellen.html">Haltestellendaten SuS 01/2020</a>, <a href="https://data.deutschebahn.com/dataset/data-stationsdaten.html">Stationsdaten SuS 03/2020</a>, <a href="https://data.deutschebahn.com/dataset/data-stationsdaten-regio.html">Haltestellendaten RNI 04/2020</a>, <a href="https://data.deutschebahn.com/dataset/data-bahnsteig.html">Bahnsteigdaten SuS 03/2020</a> $and <a href="https://data.deutschebahn.com/dataset/data-bahnsteig-regio.html">Bahnsteigdaten RNI 04/2020</a>. $github $me_html</main></body></html>"""
)
