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
from io import StringIO


async def ping_server(host: str, port: int, timeout: int = 5):
    """Ping a server."""
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=timeout)
        writer.close()
        await writer.wait_closed()
        return True
    except Exception:
        return False

async def exec_terminal(command: str):
    """Execute a terminal command."""
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
        errors = traceback.format_exception(etype=exc_type, value=exc_obj, tb=exc_tb)
        success = False
        output += errors[-1]
    return success, output, return_code

async def execute_code(code: str, safe_mode: bool = False):
    """Execute Python code."""
    if safe_mode:
        restricted_commands = ["open", "os.", "sys.", "subprocess."]
        for cmd in restricted_commands:
            if cmd in code:
                raise SafeMode("Unsafe command detected in safe mode")
    compiled_code = compile(code, filename="<string>", mode="exec")
    namespace = {}
    exec(compiled_code, namespace)
    return namespace

async def evaluate_code(code: str, safe_mode: bool = False):
    """Evaluate Python code."""
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

