# Copyright (C) 2023-present by TelegramExtended@Github, < https://github.com/TelegramExtended >.
#
# This file is part of < https://github.com/TelegramExtended/AsyncPyToolBox > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TelegramExtended/AsyncPyToolBox/blob/main/LICENSE >
#
# All rights reserved.

import asyncio
import multiprocessing
from functools import wraps
from concurrent.futures.thread import ThreadPoolExecutor


executor = ThreadPoolExecutor(max_workers=multiprocessing.cpu_count() * 5)

def check_if_package_exists(package: str):
    """Check if a package exists."""
    try:
        __import__(package)
    except ImportError:
        return False
    else:
        return True

def run_in_exc(func_):
    """Run a blocking function in a thread pool executor and return an awaitable."""
    @wraps(func_)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(executor, lambda: func_(*args, **kwargs))
    return wrapper
