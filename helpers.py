station_id = lambda station: station["bfnr"] or min(
    [s["ibnr"] for s in station["subs"]]
)

deutsch_2_float = lambda x: float(x.strip().replace(",", "."))
