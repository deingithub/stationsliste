from helpers import station_id
import json

PATCHES = {}

with open("patches.json") as f:
    PATCHES = {int(k): v for k, v in json.load(f).items()}


def patched(station):
    if not station_id(station) in PATCHES:
        return station

    station.update(PATCHES[station_id(station)])

    if "_delete" in station:
        for deletion in station["_delete"]:
            station[deletion[0]] = [
                item
                for item in station[deletion[0]]
                if not eval("lambda i:" + deletion[1])(item)
            ]

        del station["_delete"]

    if "_modify" in station:
        for modification in station["_modify"]:
            station[modification[0]] = [
                eval("lambda i:" + modification[2])(item)
                if eval("lambda i:" + modification[1])(item)
                else item
                for item in station[modification[0]]
            ]

        del station["_modify"]

    if "_add" in station:
        for addition in station["_add"]:
            station[addition[0]].append(addition[1])

        del station["_add"]

    return station
