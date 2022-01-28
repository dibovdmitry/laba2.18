#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import sys


def add_airplane(race, path, number, model):
    race.append(
        {
            "path": path,
            "number": number,
            "model": model
        }
    )
    return race


def display_airplanes(race):
    if race:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 20
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^20} |'.format(
                "№",
                "Пункт назначения",
                "Номер рейса",
                "Тип самолёта"
                )
        )
        print(line)
        for idx, airplane in enumerate(race, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>20} |'.format(
                    idx,
                    airplane.get('path', ''),
                    airplane.get('number', ''),
                    airplane.get('model', 0)
                )
            )
        print(line)
    else:
        print("Список работников пуст.")


def select_airplanes(race, sel):

    result = []
    for airplane in race:
        if airplane.get('path') <= sel:
            result.append(airplane)

    return result


def save_airplanes(file_name, race):
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(race, fout, ensure_ascii=False, indent=4)


def load_airplanes(file_name):
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main(command_line=None):
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "-d",
        "--data",
        action="store",
        required=False,
        help="The data file name"
    )

    parser = argparse.ArgumentParser("airplanes")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new airplane"
    )
    add.add_argument(
        "-p",
        "--path",
        action="store",
        required=True,
        help="The airplane's path"
    )
    add.add_argument(
        "-n",
        "--number",
        action="store",
        help="The airplane's number"
    )
    add.add_argument(
        "-m",
        "--model",
        action="store",
        type=int,
        required=True,
        help="The airplane's model"
    )

    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all airplanes"
    )

    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the airplanes"
    )
    select.add_argument(
        "-r",
        "--result",
        action="store",
        type=int,
        required=True,
        help="The required result"
    )

    args = parser.parse_args(command_line)

    data_file = args.data
    if not data_file:
        data_file = os.environ.get("RACES_DATA")
    if not data_file:
        print("The data file name is absent", file=sys.stderr)
        sys.exit(1)

    is_dirty = False
    if os.path.exists(data_file):
        airplanes = load_airplanes(data_file)
    else:
        airplanes = []

    if args.command == "add":
        airplanes = add_airplane(
            airplanes,
            args.path,
            args.number,
            args.model
        )
        is_dirty = True

    elif args.command == "display":
        display_airplanes(airplanes)

    elif args.command == "select":
        selected = select_airplanes(airplanes, args.period)
        display_airplanes(selected)

    if is_dirty:
        save_airplanes(data_file, airplanes)


if __name__ == "__main__":
    main()
