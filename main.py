import configparser
import json
import os
import pathlib
import sys
import getopt
from typing import Any, Optional

import appdirs
import yeelight
from pathlib import Path

APPNAME = "better_yeecli"
CONFIG_FILENAME = "settings.ini"


def main(argv):
    bulb: Optional[yeelight.Bulb] = None
    try:
        opts, args = getopt.getopt(argv, "hsb:t", ["search", "bulb=", "toggle", "set-default="])
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            printHelp()
            sys.exit(0)
        elif opt in ("-b", "--bulb"):
            bulbs = searchBulbs()
            bulb = getBulbByNameOrId(arg, bulbs)
            print(bulb)
        elif opt in ("--set-default"):
            setDefaultBulb()
            sys.exit(0)
        elif opt in ("-s", "--search"):
            bulbs = searchBulbs()
            pretty_bulbs = list(map(lambda bu: str(bu), bulbs))
            print("Available bulbs:")
            print("\n".join(pretty_bulbs))
            sys.exit(0)

    if bulb is None:
        # TODO: grab default bulb from config file
        pass

    for opt, arg in opts:
        if opt in ("-t", "--toggle"):
            bulb.toggle()


def setDefaultBulb():
    print("not_implemented :)")


def getBulbByNameOrId(nameOrId: str, bulbs: list[dict[str, any]]):
    bId = resolveBulbName(nameOrId)
    b = list(filter(lambda bu: bu["id"] == bId, bulbs))
    if len(b) > 0:
        (ip, port) = (b[0]["ip"], b[0]["port"])
        return yeelight.Bulb(ip, port)
    else: return None


def resolveBulbName(nameOrId: str):
    config = readConfig()
    if "aliases" in config:
        if nameOrId in config["aliases"]:
            return config["aliases"][nameOrId]
    # if we get here, assume the given nameOrId is an id
    return nameOrId


def readConfig(makeIfNotExists = True):
    config = configparser.ConfigParser()
    config_path = appdirs.user_config_dir(APPNAME)
    config_dir = pathlib.Path(config_path)
    config_file = config_dir.joinpath(CONFIG_FILENAME)
    if makeIfNotExists:
        config_dir.mkdir(parents=True, exist_ok=True)
        # trick to create empty file if not exists, but leave content intact if it does
        open(config_file, "a+").close()
    config.read(config_file)
    return config


def searchBulbs() -> list[dict[str, Any]]:
    # response = eval(yeelight.discover_bulbs())
    response = eval(
        "[{'ip': '192.168.68.113', 'port': 55443, 'capabilities': {'id': '0x00000000101761e3', 'model': 'mono4', 'fw_ver': '7', 'support': 'get_prop set_default set_power toggle set_bright set_scene cron_add cron_get cron_del start_cf stop_cf set_name set_adjust adjust_bright', 'power': 'off', 'bright': '100', 'color_mode': '2', 'ct': '4000', 'rgb': '0', 'hue': '0', 'sat': '0', 'name': ''}}, {'ip': '192.168.68.114', 'port': 55443, 'capabilities': {'id': '0x000000000e9f69c8', 'model': 'colora', 'fw_ver': '6', 'support': 'get_prop set_default set_power toggle set_bright set_scene cron_add cron_get cron_del start_cf stop_cf set_ct_abx adjust_ct set_name set_adjust adjust_bright adjust_color set_rgb set_hsv set_music', 'power': 'off', 'bright': '1', 'color_mode': '2', 'ct': '1700', 'rgb': '16711680', 'hue': '359', 'sat': '100', 'name': ''}}]")
    bulbs = [json_obj for json_obj in response]
    return [{"id": bulb["capabilities"]["id"],
             "model": bulb["capabilities"]["model"],
             "ip": bulb["ip"],
             "port": bulb["port"]
             } for bulb in bulbs]


def printHelp():
    print(f"usage: {sys.argv[0]} [OPTIONS]")


if __name__ == '__main__':
    main(sys.argv[1:])
