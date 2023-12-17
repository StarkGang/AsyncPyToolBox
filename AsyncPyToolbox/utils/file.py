# Copyright (C) 2023-present by TelegramExtended@Github, < https://github.com/TelegramExtended >.
#
# This file is part of < https://github.com/TelegramExtended/AsyncPyToolBox > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TelegramExtended/AsyncPyToolBox/blob/main/LICENSE >
#
# All rights reserved.

from . import *
import os
import mimetypes

# Check if PIL is installed
is_pil_installed = check_if_package_exists("PIL")
if is_pil_installed:
    from PIL import Image


class FileHelpers:
    """FileHelpers class to help you with files.
    Parameters:
        file (str): Path of the file.
    Raises:
        OSError: If the file doesn't exist in my storage."""
    def __init__(self, file) -> None:
        self.__file__ = file
        if not os.path.exists(self.__file__):
            raise OSError("File Doesn't exist in my storage.")

    def _get_metadata(self, is_audio=True) -> tuple:
        """Get metadata of a file.
        Parameters:
            is_audio (bool, optional): Whether the file is audio or not. Defaults to True."""
        dur, title = 0, None
        if is_audio:
            try:
                with open(self.__file__, 'rb') as file:
                    file.seek(-128, 2)
                    tag = file.read(128).decode('utf-8')
                    title = tag[3:32].strip('\x00')
            except Exception:
                pass
        else:
            dur = self.get_meta_data_video()[0] or 0
        return dur, title

    def _resize_if_req(self, image_size_allowed=1280) -> None:
        """Resize an image if it's size is greater than the allowed size.
        Parameters:
            image_size_allowed (int, optional): Maximum size of the image. Defaults to 1280."""
        if is_pil_installed:
            im = Image.open(self.__file__)
            if max(im.size) > image_size_allowed:
                im.thumbnail((image_size_allowed, image_size_allowed))
                im.save(self.__file__)
        pass

    def get_meta_data_video(self) -> tuple:
        """Get metadata of a video file.
        Returns:
            tuple: (duration, width, height)"""
        try:
            with open(self.__file__, 'rb') as file:
                data = file.read(200)
                dur = data.find(b'\x96\x9e') + 6 if b'\x96\x9e' in data else 0
                width = data.find(b'\x00\x00\x00\x01\x67') + 9 if b'\x00\x00\x00\x01\x67' in data else 0
                height = data.find(b'\x00\x00\x00\x01\x68') + 9 if b'\x00\x00\x00\x01\x68' in data else 0
            return dur, width, height
        except Exception:
            return 0, 0, 0

    def get_by_reading(self) -> str:
        """Get mime type of a file by reading it.
        Returns:
            str: Mime type of the file."""
        try:
            with open(self.__file__, 'rb') as file:
                data = file.read(200)
                mime_type = data.find(b'ftyp') + 8
                return data[mime_type:mime_type + 8].decode('utf-8')
        except Exception:
            return None

    def guess_mime_type_from_mimetypes(self) -> str:
        """Guess mime type of a file from mimetypes.
        Returns:
            str: Mime type of the file."""
        return mimetypes.guess_type(self.__file__)[0]

    def guess_mime_type(self) -> str:
        """Guess mime type of a file.
        Returns:
            str: Mime type of the file."""
        return self.get_by_reading() or self.guess_mime_type_from_mimetypes()

    def _is_media(self, media_type) -> bool:
        """Check if a file is a media file.
        Parameters: 
            media_type (str): Media type to check.
        Returns:
            bool: Whether the file is a media file or not."""
        mt = self.guess_mime_type()
        return mt and mt.startswith(media_type)

    @property
    def is_audio(self) -> bool:
        """Check if a file is an audio file.
        Returns:
            bool: Whether the file is an audio file or not.
        """
        return self._is_media("audio/")

    @property
    def is_audio_note(self) -> bool:
        """Check if a file is an audio note.
        Returns:
            bool: Whether the file is an audio note or not.
        """
        return self.is_audio and self.guess_mime_type().endswith((".ogg"))

    @property
    def is_video(self) -> bool:
        """Check if a file is a video file.
        Returns:
            bool: Whether the file is a video file or not.
        """
        return self._is_media("video/")

    @property
    def is_photo(self) -> bool:
        """Check if a file is a photo file.
        Returns:
            bool: Whether the file is a photo file or not.
        """
        return self._is_media("image/")

    @property
    def get_ext(self) -> str:
        """Get extension of a file.
        Returns:
            str: Extension of the file."""
        return os.path.splitext(self.__file__)[1][1:]

    @property
    def is_animated_sticker(self)  -> bool:
        """Check if a file is an animated sticker.
        Returns:
            bool: Whether the file is an animated sticker or not.
        """
        return self.get_ext == "tgs" and not any([self.is_audio, self.is_video, self.is_photo, self.is_sticker])

    @property
    def is_sticker(self) -> bool:
        """Check if a file is a sticker.
        Returns:
            bool: Whether the file is a sticker or not.
        """
        return self.get_ext == "webp" and not any([self.is_audio, self.is_video, self.is_photo])

    @property
    def is_document(self) -> bool:
        """Check if a file is a document.
        Returns:
            bool: Whether the file is a document or not.
        """
        return not any([self.is_audio, self.is_video, self.is_photo, self.is_sticker, self.is_animated_sticker])



def scandir(dir, ext=None, subfolders=[], files=[]) -> list:
    """Scans a directory for files and returns a list of files found.
    Parameters:
        dir (str): The directory to scan.
        ext (list, optional): A list of extensions to filter by. Defaults to None.
        subfolders (list, optional): A list of subfolders to scan. Defaults to [].
        files (list, optional): A list of files to append to. Defaults to []."""
    for f in os.scandir(dir):
        if f.is_dir():
            scandir(f.path, ext, subfolders, files)
        if f.is_file():
            if ext and os.path.splitext(f.name)[1].lower() in ext:
                files.append(f.path)
            else:
                files.append(f.path)
    return files


