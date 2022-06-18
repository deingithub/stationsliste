#!/usr/bin/env python3

import sqlite3
import argparse
import locale
import itertools

import extract2
import layout2
from helpers import station_id


def render_station(station, lang):
    address_html = ""
    if station["strasse"]:
        address_html = f'<address>{station["strasse"]}, {station["plz"]} {station["ort"]} ({station["bundesland"]})</address>'

    subs_html = ""
    for i, sub in enumerate(station["subs"]):
        subs_html += '<p class="sm">'

        if len(station["subs"]) > 1 or station["subs"][0]["name"] != station["name"]:
            subs_html += f'<b>{sub["name"]}:</b> '

        subs_html += " | ".join(
            [
                f"<b>{lang[key]}</b> {sub[key]}"
                for key in ("ds100", "ibnr", "ifopt", "verkehr", "betreiber_name")
                if sub[key]
            ]
        )

        if sub["lat"] and sub["lon"] and i > 0:
            subs_html += f' | <a href="https://www.openstreetmap.org/#map=17/{sub["lat"]}/{sub["lon"]}">OpenStreetMap</a>'

        subs_html += "</p>"

    links_html = (
        '<p class="button-row">'
        f'<a href="https://dbf.finalrewind.org/{station["name"]}">db-infoscreen</a>'
        f' <a href="https://www.bahnhof.de/service/search/bahnhof-de/520608?query={station["name"]}">bahnhof.de</a>'
    )

    if station["subs"][0]["lat"] and station["subs"][0]["lon"]:
        links_html += f' <a href="https://www.openstreetmap.org/#map=17/{sub["lat"]}/{sub["lon"]}">OpenStreetMap</a>'

    links_html += "</p>"

    platforms_html = ""
    if station["platforms"]:
        if station["platforms"][0]["quelle"] == "rni":
            platforms_html += lang["rni_warn_html"]
        for platform, rows in itertools.groupby(
            sorted(station["platforms"], key=lambda row: row["bahnsteig"]),
            key=lambda row: row["bahnsteig"],
        ):
            platforms_html += f'<div class="platform"><h3><span class="invis">{lang["platform"]}</span> {platform}</h3>'
            for row in rows:
                platforms_html += (
                    f'<p><em><span>{lang["track"]} </span>{row["gleis"]}</em> '
                    f'{row["hoehe"]}cm {lang["high"]}, {row["laenge"]}m {lang["long"]} </p>'
                )
            platforms_html += "</div>"

    if not platforms_html:
        platforms_html = lang["notrackinfo_html"]

    cite_html = ""
    if station.get("_cite"):
        cite_html += f'<h3 class="sm">{lang["patches"]}</h3><ul class="sm">'
        for cite in station["_cite"]:
            cite_html += f"<li>{cite}</li>"
        cite_html += "</ul>"

    return f"""<section data-name="{station["name"]}">
        <h2 id="{station_id(station)}" lang="de"><a href="#{station_id(station)}">{station["name"]}</a></h2>
        {address_html}
        {links_html}
        {subs_html}
        {platforms_html}
        {cite_html}
        </section>"""


def render_station_for_list(station, lang):
    sub_html = ""
    if sub_names := [
        sub["name"] for sub in station["subs"] if not sub["name"] == station["name"]
    ]:
        sub_html = f'<i>{lang["also"]} {", ".join(sub_names)}</i>'

    return f"""<li id="{station_id(station)}">
    <a lang="de" href="./details/{lang["lang"]}/{station_id(station)}.html">{station["name"]}</a>
    {sub_html}</li>"""


def generate(db, stations):
    for lang in (layout2.LANG["de"], layout2.LANG["en"]):
        with open(f'web/{lang["lang"]}.html', "w", encoding="utf-8") as f:
            f.write(
                layout2.LAYOUT_TOP.substitute(**lang)
                + layout2.LAYOUT_LINKLIST_PREFIX.substitute(**lang)
            )
            for station in stations:
                f.write(render_station_for_list(station, lang))
            f.write(
                layout2.LAYOUT_LINKLIST_SUFFIX
                + layout2.LAYOUT_BOTTOM.substitute(**lang)
            )
        for station in stations:
            with open(
                f'web/details/{lang["lang"]}/{station_id(station)}.html',
                "w",
                encoding="utf-8",
            ) as f:
                f.write(render_station(station, lang))

    with open("web/complete.html", "w", encoding="utf-8") as f:
        f.write(layout2.LAYOUT_TOP.substitute(**layout2.LANG["de"]))
        for station in stations:
            f.write(render_station(station, layout2.LANG["de"]))
        f.write(layout2.LAYOUT_BOTTOM.substitute(**layout2.LANG["de"]))


if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, "de_DE")
    p = argparse.ArgumentParser()
    p.add_argument("database", help="database path")
    args = p.parse_args()

    db = sqlite3.connect(args.database)
    db.row_factory = sqlite3.Row

    generate(
        db,
        sorted(
            extract2.extract_stations(db), key=lambda bf: locale.strxfrm(bf["name"])
        ),
    )
