#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import sys
from dotenv import load_dotenv


def get_airplane(race, path, number, model):
    race.append(
        {
            'path': path,
            'number': number,
            'model': model,
        }
    )
    return race


def display_airplanes(race):
    if race:
        line = '+-{}-+-{}-+-{}-+'.format(
            '-' * 30,
            '-' * 4,
            '-' * 20
        )
        print(line)
        print(
            '| {:^30} | {:^4} | {:^20} |'.format(
                "Пункт назначения",
                "Номер рейса",
                "Тип самолёта"
            )
        )
        print(line)

        for airplane in race:
            print(
                '| {:<30} | {:>4} | {:<20} |'.format(
                    airplane.get('path', ''),
                    airplane.get('number', ''),
                    airplane.get('model', '')
                )
            )
        print(line)

    else:
        print("Таких рейсов нет")


def select_airplanes(race, sel):

    result = []
    for airplane in race:
        if airplane.get('path') <= sel:
            result.append(airplane)

    return result


def save_airplanes(file_name, race):
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(race, f, ensure_ascii=False, indent=4)


def load_airplanes(file_name):
    with open(file_name, "r", encoding="utf-8") as fl:
        return json.load(fl)


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
        help="Add a new way"
    )
    add.add_argument(
        "-p",
        "--path",
        action="store",
        required=True,
        help="The race's name"
    )
    add.add_argument(
        "-n",
        "--number",
        action="store",
        type=int,
        help="The race's number"
    )
    add.add_argument(
        "-m",
        "--model",
        action="store",
        required=True,
        help="The race's model"
    )

    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all races"
    )

    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the race"
    )
    select.add_argument(
        "-s",
        "--sel",
        action="store",
        required=True,
        help="The required period"
    )

    args = parser.parse_args(command_line)

    data_file = args.data

    if not data_file:
        load_dotenv()
        data_file = os.getenv("RACES")
    if not data_file:
        print("The data file name is absent", file=sys.stderr)
        sys.exit(1)

    is_dirty = False
    if os.path.exists(data_file):
        airplanes = load_airplanes(data_file)
    else:
        airplanes = []

    if args.command == "add":
        airplanes = get_airplane(
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


if __name__ == '__main__':
    main()
