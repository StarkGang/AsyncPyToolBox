# Copyright (C) 2023-present by TelegramExtended@Github, < https://github.com/TelegramExtended >.
#
# This file is part of < https://github.com/TelegramExtended/AsyncPyToolBox > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TelegramExtended/AsyncPyToolBox/blob/main/LICENSE >
#
# All rights reserved.

import re
from . import *
import random
import string

ip_middle_octet = r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5]))"
ip_last_octet = r"(?:\.(?:0|[1-9]\d?|1\d\d|2[0-4]\d|25[0-5]))"
regex = re.compile(
    r"^"
    # protocol identifier
    r"(?:(?:https?|ftp)://)"
    # user:pass authentication
    r"(?:[-a-z\u00a1-\uffff0-9._~%!$&'()*+,;=:]+"
    r"(?::[-a-z0-9._~%!$&'()*+,;=:]*)?@)?"
    r"(?:"
    r"(?P<private_ip>"
    # IP address exclusion
    # private & local networks
    r"(?:(?:10|127)" + ip_middle_octet + r"{2}" + ip_last_octet + r")|"
    r"(?:(?:169\.254|192\.168)" + ip_middle_octet + ip_last_octet + r")|"
    r"(?:172\.(?:1[6-9]|2\d|3[0-1])" + ip_middle_octet + ip_last_octet + r"))"
    r"|"
    # private & local hosts
    r"(?P<private_host>" r"(?:localhost))" r"|"
    # IP address dotted notation octets
    # excludes loopback network 0.0.0.0
    # excludes reserved space >= 224.0.0.0
    # excludes network & broadcast addresses
    # (first & last IP address of each class)
    r"(?P<public_ip>"
    r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
    r"" + ip_middle_octet + r"{2}"
    r"" + ip_last_octet + r")"
    r"|"
    # IPv6 RegEx from https://stackoverflow.com/a/17871737
    r"\[("
    # 1:2:3:4:5:6:7:8
    r"([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|"
    # 1::                              1:2:3:4:5:6:7::
    r"([0-9a-fA-F]{1,4}:){1,7}:|"
    # 1::8             1:2:3:4:5:6::8  1:2:3:4:5:6::8
    r"([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|"
    # 1::7:8           1:2:3:4:5::7:8  1:2:3:4:5::8
    r"([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|"
    # 1::6:7:8         1:2:3:4::6:7:8  1:2:3:4::8
    r"([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|"
    # 1::5:6:7:8       1:2:3::5:6:7:8  1:2:3::8
    r"([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|"
    # 1::4:5:6:7:8     1:2::4:5:6:7:8  1:2::8
    r"([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|"
    # 1::3:4:5:6:7:8   1::3:4:5:6:7:8  1::8
    r"[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|"
    # ::2:3:4:5:6:7:8  ::2:3:4:5:6:7:8 ::8       ::
    r":((:[0-9a-fA-F]{1,4}){1,7}|:)|"
    # fe80::7:8%eth0   fe80::7:8%1
    # (link-local IPv6 addresses with zone index)
    r"fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|"
    r"::(ffff(:0{1,4}){0,1}:){0,1}"
    r"((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}"
    # ::255.255.255.255   ::ffff:255.255.255.255  ::ffff:0:255.255.255.255
    # (IPv4-mapped IPv6 addresses and IPv4-translated addresses)
    r"(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|"
    r"([0-9a-fA-F]{1,4}:){1,4}:"
    r"((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}"
    # 2001:db8:3:4::192.0.2.33  64:ff9b::192.0.2.33
    # (IPv4-Embedded IPv6 Address)
    r"(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])" r")\]|"
    # host name
    r"(?:(?:(?:xn--)|[a-z\u00a1-\uffff\U00010000-\U0010ffff0-9]-?)*"
    r"[a-z\u00a1-\uffff\U00010000-\U0010ffff0-9]+)"
    # domain name
    r"(?:\.(?:(?:xn--)|[a-z\u00a1-\uffff\U00010000-\U0010ffff0-9]-?)*"
    r"[a-z\u00a1-\uffff\U00010000-\U0010ffff0-9]+)*"
    # TLD identifier
    r"(?:\.(?:(?:xn--[a-z\u00a1-\uffff\U00010000-\U0010ffff0-9]{2,})|"
    r"[a-z\u00a1-\uffff\U00010000-\U0010ffff]{2,}))"
    r")"
    # port number
    r"(?::\d{2,5})?"
    # resource path
    r"(?:/[-a-z\u00a1-\uffff\U00010000-\U0010ffff0-9._~%!$&'()*+,;=:@/]*)?"
    # query string
    r"(?:\?\S*)?"
    # fragment
    r"(?:#\S*)?" r"$",
    re.UNICODE | re.IGNORECASE,
)

pattern = re.compile(regex)

@run_in_exc
def is_url(value: str, public: bool =False) -> bool:
    """Check if value is URL."""
    result = pattern.match(value)
    if not public:
        return result
    return result and not any(
        (result.groupdict().get(key) for key in ("private_ip", "private_host"))
    )


@run_in_exc
def is_valid_email(value: str) -> bool:
    """Check if value is valid email."""
    return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", value))

@run_in_exc
def validate_phone_any_country(phone: str) -> bool:
    """Validate phone number."""
    return bool(re.search(r"^\+?[0-9]{6,14}$", phone))


@run_in_exc
def random_hash(length=8) -> str:
    """Generate a random hash."""
    return "".join(random.choice("0123456789abcdef") for _ in range(length))

@run_in_exc
def generate_random_password(length, lowercase=True, uppercase=True, digits=True, special_chars=True):
    """Generate a random password."""
    chars = string.ascii_lowercase * lowercase + string.ascii_uppercase * uppercase + string.digits * digits + string.punctuation * special_chars
    return ''.join(random.choice(chars) for _ in range(length))

bs4_installed = check_if_package_exists("bs4")
markdown_installed = check_if_package_exists("markdown")

if bs4_installed and markdown_installed:
    import markdown
    from bs4 import BeautifulSoup

@run_in_exc
def md_to_text(raw_text: str) -> str:
    """Convert markdown to text."""
    if bs4_installed and markdown_installed:
        html = markdown.markdown(raw_text)
        soup = BeautifulSoup(html, features="html.parser")
        return soup.get_text()
    text = re.sub(r'<[^>]*>', '', raw_text)
    text = re.sub(r'&nbsp;|&amp;|&lt;|&gt;|&quot;|&#39;', '', text)
    return html_entity_decode(text)

@run_in_exc
def html_entity_decode(text: str):
    """Decode HTML entities in the text."""
    entities = {'&nbsp;': ' ', '&amp;': '&', '&lt;': '<', '&gt;': '>', '&quot;': '"', '&#39;': "'", '&lt;': '<', '&gt;': '>'}
    for entity, char in entities.items():
        text = text.replace(entity, char)
    return text

@run_in_exc        
def clean_html(text: str) -> str:
    """"Clean HTML tags from text."""
    return re.sub(r"<[^>]*>", "", text)

platforms = {
        "Macintosh": ["68K", "PPC"],
        "Windows": [
            "Win3.11",
            "WinNT3.51",
            "WinNT4.0",
            "Windows NT 5.0",
            "Windows NT 5.1",
            "Windows NT 5.2",
            "Windows NT 6.0",
            "Windows NT 6.1",
            "Windows NT 6.2",
            "Win95",
            "Win98",
            "Win 9x 4.90",
            "WindowsCE",
        ],
        "X11": ["Linux i686", "Linux x86_64"],
    }

@run_in_exc
def gen_random_useragent():
    platform = random.choice(["Macintosh", "Windows", "X11"])
    gen_os = random.choice(platforms[platform])    
    browser = random.choice(["chrome", "firefox", "ie"])
    if browser == "chrome":
        return f"Mozilla/5.0 ({gen_os}) AppleWebKit/{random.randint(500, 599)}.0 (KHTML, live Gecko) Chrome/{random.randint(0, 24)}.0.{random.randint(0, 999)} Safari/{random.randint(500, 599)}"
    elif browser == "firefox":
        return f"Mozilla/5.0 ({gen_os}; rv:{random.choice(range(1, 16))}.0) Gecko/{random.randint(20000101, 20121231)} Firefox/{random.choice(range(1, 16))}.0"
    elif browser == "ie":
        version = f"{random.randint(1, 10)}.0"
        engine = f"{random.randint(1, 5)}.0"
        token = f"{random.choice(['.NET CLR', 'SV1', 'Tablet PC', 'Win64; IA64', 'Win64; x64', 'WOW64'])}; " if random.choice([True, False]) else ""
        return f"Mozilla/5.0 (compatible; MSIE {version}; {gen_os}; {token}Trident/{engine})"
