# Copyright (C) 2023-present by TelegramExtended@Github, < https://github.com/TelegramExtended >.
#
# This file is part of < https://github.com/TelegramExtended/AsyncPyToolBox > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TelegramExtended/AsyncPyToolBox/blob/main/LICENSE >
#
# All rights reserved.


from . import *
import json


@run_in_exc
def file_to_json(file_path: str) -> dict:
    """Convert a file to JSON.
    Parameters:
        file_path (str): Path of the file."""
    with open(file_path, "r") as file:
        return json.load(file)
    
@run_in_exc
def write_to_json(file_path: str, data: dict):
    """Write data to a JSON file.
    Parameters:
        file_path (str): Path of the file.
        data (dict): Data to write."""
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def get_readable_time(seconds: int) -> str:
    """Get readable time from seconds.
    Parameters:
        seconds (int): Time in seconds."""
    suffixes = ["s", "m", "h", "days"]
    times = [seconds // 60, seconds % 60]
    for i in range(2, 4): times.insert(0, times.pop(0) // 24) if i == 3 else times.insert(0, times.pop(0))
    return ':'.join([f"{val}{suffix}" for val, suffix in zip(times, suffixes) if val]) if len(times) > 1 else f"{times[0]}, "

def humanbytes(size):
    """Convert bytes to human readable format.
    Parameters:
        size (int): Size in bytes."""
    if size:
        power = 2**10
        raised_to_pow = 0
        dict_power_n = {0: "", 1: "KB", 2: "MB", 3: "GB", 4: "TB"}
        while size > power:
            size /= power
            raised_to_pow += 1
        return f"{str(round(size, 2))} {dict_power_n[raised_to_pow]}"
    return "0B"


def time_formatter(milliseconds: int) -> str:
    """Convert time to a readable format.
    Parameters:
        milliseconds (int): Time in milliseconds."""
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return (
            (f"{str(days)} Day(s), " if days else "")
            + (f"{str(hours)} Hour(s), " if hours else "")
            + (f"{str(minutes)} Minute(s), " if minutes else "")
            + (f"{str(seconds)} Second(s), " if seconds else "")
            + (f"{str(milliseconds)} Millisecond(s), " if milliseconds else "")
        )[:-2]


