# Copyright (C) 2023-present by TelegramExtended@Github, < https://github.com/TelegramExtended >.
#
# This file is part of < https://github.com/TelegramExtended/TelegramExtended > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TelegramExtended/TelegramExtended/blob/main/LICENSE >
#
# All rights reserved.

class SafeMode(Exception):
    """Raised when unsafe command is detected in safe mode."""
    pass