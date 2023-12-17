# Copyright (C) 2023-present by TelegramExtended@Github, < https://github.com/TelegramExtended >.
#
# This file is part of < https://github.com/TelegramExtended/AsyncPyToolBox > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TelegramExtended/AsyncPyToolBox/blob/main/LICENSE >
#
# All rights reserved.

import sys
import shlex
import asyncio
import traceback
from ..errors import SafeMode
from . import *
from io import StringIO


async def ping_server(host: str, port: int, timeout: int = 5) -> tuple[bool, str]:
    """Ping a server.
    Parameters:
        host (str): Host to ping.
        port (int): Port to ping.
        timeout (int, optional): Timeout in seconds. Defaults to 5.
    Returns:
        tuple: (success, output)"""
    try:
        reader, writer = await asyncio.open_connection(host, port)
        writer.close()
        await writer.wait_closed()
        return True, "Ping successful!"
    except Exception:
        return False, traceback.format_exc()

async def exec_terminal(command: str) -> tuple[bool, str, int]:
    """Execute a terminal command.
    Parameters:
        command (str): Command to execute.
    Returns:
        tuple: (success, output, return_code)"""
    success = True
    return_code = 0
    command = shlex.split(command)
    output = ""
    try:
        process = await asyncio.create_subprocess_exec(
            *command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        return_code = process.returncode
        stdout, stderr = await process.communicate()
        output += stdout.decode("utf-8").strip()
        if stderr:
            output += "\n" + stderr.decode("utf-8").strip()
        success = True
    except Exception:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        errors = traceback.format_exception(exc_type, value=exc_obj, tb=exc_tb)
        success = False
        output += errors[-1]
    return success, output, return_code

async def execute_code(code: str, safe_mode: bool = False) -> dict:
    """Execute Python code.
    Parameters:
        code (str): Python code to execute.
        safe_mode (bool, optional): Whether to enable safe mode or not. Defaults to False.
    Returns:
        dict: Namespace of the executed code."""
    if safe_mode:
        restricted_commands = ["open", "os.", "sys.", "subprocess."]
        for cmd in restricted_commands:
            if cmd in code:
                raise SafeMode("Unsafe command detected in safe mode")
    compiled_code = compile(code, filename="<string>", mode="exec")
    namespace = {}
    exec(compiled_code, namespace)
    return namespace

async def evaluate_code(code: str, safe_mode: bool = False) -> tuple[str, str, str, dict]:
    """Evaluate Python code.
    Parameters:
        code (str): Python code to evaluate.
        safe_mode (bool, optional): Whether to enable safe mode or not. Defaults to False.
    Returns:
        tuple: (exception, stdout, stderr, namespace)"""
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        namespace = await execute_code(code, safe_mode=safe_mode)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    return exc, stdout, stderr, namespace

is_psutil_installed = check_if_package_exists("psutil")
if is_psutil_installed:
    from platform import system as pt_system, release as pt_release, version as pt_version, machine as pt_machine, processor as pt_processor
    from psutil import virtual_memory as psl_virtual_memory, cpu_freq as psl_cpu_freq, disk_usage as psl_disk_usage, disk_io_counters as psl_disk_io_counters, Process as psl_Process
    from socket import gethostname as skt_gethostname, gethostbyname as skt_gethostbyname
    from contextlib import suppress
    import os
    import re
    import uuid
    from .convertors import humanbytes

@run_in_exc
def get_system_info(value=False) -> tuple:
    if not is_psutil_installed:
        raise ModuleNotFoundError("This function requires psutil to be installed. Install it by running pip install psutil")
    """
    Get Info
        fetches information about your system
        hides MAC and IP until explicitly referenced
        incompatible with termux due to problem with ethtool.h file .so objects
    Parameters:
        value (bool, optional): Whether to fetch IP and MAC or not. Defaults to False.
    Returns:
        tuple: (platform, platform_release, platform_version, architecture, hostname, ip_address, mac_address, processor, ram, cpu_len, cpu_freq, disk)
    Raises:
        ModuleNotFoundError: If psutil is not installed.
    """
    splatform = pt_system()
    platform_release = pt_release()
    platform_version = pt_version()
    architecture = pt_machine()
    hostname = skt_gethostname()
    ip_address = "Unable to fetch"
    mac_address = "Unable to fetch"
    with suppress(Exception):
        ip_address = skt_gethostbyname(skt_gethostname())
    with suppress(Exception):
        mac_address = ":".join(re.findall("..", "%012x" % uuid.getnode()))
    processor = pt_processor()
    ram = humanbytes(round(psl_virtual_memory().total))
    cpu_freq = psl_cpu_freq().current
    if cpu_freq >= 1000:
        cpu_freq = f"{round(cpu_freq / 1000, 2)}GHz"
    else:
        cpu_freq = f"{round(cpu_freq, 2)}MHz"
    du = psl_disk_usage(os.getcwd())
    psl_disk_io_counters()
    disk = (
        f"{humanbytes(du.used)}/{humanbytes(du.total)}"
        f"({du.percent}%)"
    )
    cpu_len = len(psl_Process().cpu_affinity())
    return (
        splatform,
        platform_release,
        platform_version,
        architecture,
        hostname,
        ip_address if value else None,
        mac_address if value else None,
        processor,
        ram,
        cpu_len,
        cpu_freq,
        disk,
    )
