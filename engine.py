#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GLOBAL PAYMENT SETTLEMENT ENGINE v5.0
Build 2026.05.26 | Multi-Protocol Financial Terminal
[ SIMULATION / DEMONSTRATION TOOL ONLY ]
"""

import time
import random
import os
import sys
import hashlib
import datetime
import string
import json

# =====================================================================
# [ VERSION ]
# =====================================================================
VERSION = "5.0.0"
BUILD = "2026.05.26"

# =====================================================================
# [ CONFIGURATION DIRECTORY ]
# =====================================================================
try:
    CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
except NameError:
    CONFIG_PATH = os.path.join(os.getcwd(), "config.json")


# =====================================================================
# [ DEFAULT CONFIGURATION ]
# =====================================================================
_DEFAULT_RESULT_CONFIG = {
    "protocol_transaction": "SUCCESS",
    "interbank": "FAILED",
    "ip_to_ip": "SUCCESS",
    "s2s": "SUCCESS",
    "gpi": "SUCCESS",
    "mt103": "SUCCESS",
    "rtgs": "SUCCESS",
}

_DEFAULT_RESULT_MESSAGE = {
    "protocol_transaction": "",
    "interbank": "Validator quorum unreachable \u2014 TX voided",
    "ip_to_ip": "",
    "s2s": "",
    "gpi": "",
    "mt103": "",
    "rtgs": "",
}

_DEFAULT_TIMING = {
    "boot_progress": 8,
    "auth_connect": 1.5,
    "auth_verify": 1.5,
    "auth_2fa": 1.2,
    "auth_session_key": 3,
    "net_hop_duration": 1.0,
    "net_ecdhe": 1.5,
    "net_forward_secrecy": 1.0,
    "net_alliance": 1.2,
    "net_tunnel_progress": 4,
    "scan_probe_duration": 4,
    "scan_batch_duration": 80,
    "decrypt_layer_duration": 4,
    "routing_validate": 2.0,
    "routing_aml": 1.5,
    "routing_correspondent": 6,
    "bridge_ping": 1.5,
    "bridge_escrow_progress": 2.5,
    "bridge_sync_progress": 5,
    "settlement_duration": 30,
}

_DEFAULT_MODULE_TOKENS = {
    "protocol_transaction": {
        "83GIM": {
            "name": "DARKOATH",
            "cardholder": "LAWRENCE CLAYTON",
            "bank_provider": "BANK OF MONTREAL",
            "iso_country": "CANADA",
            "iso_a2": "CA",
            "iso_a3": "CAN",
            "iso_num": "124",
            "allowed_card_last4": "6498",
        },
        "W82KB": {
            "name": "MZKR SGAR",
            "cardholder": "MICHAEL SAGAR",
            "bank_provider": "UBS GROUP AG",
            "iso_country": "SWITZERLAND",
            "iso_a2": "CH",
            "iso_a3": "CHE",
            "iso_num": "756",
            "allowed_card_last4": None,
        },
    },
    "interbank": {
        "ADMIN": {
            "name": "SYSTEM ADMIN",
            "username": "admin",
            "password_hash": hashlib.sha256("admin".encode()).hexdigest(),
        },
    },
    "ip_to_ip": {
        "7X9KL": {
            "name": "NEXUS PRIME",
            "operator": "JAMES WHITFIELD",
            "clearance": "LEVEL-5",
            "region": "EMEA",
        },
        "R4T2P": {
            "name": "VECTOR NODE",
            "operator": "SARAH CHEN",
            "clearance": "LEVEL-4",
            "region": "APAC",
        },
    },
    "s2s": {
        "API01": {
            "name": "MERCURY ENGINE",
            "merchant": "GLOBAL PAYMENTS INC",
            "api_version": "v3.2.1",
            "environment": "PRODUCTION",
        },
        "API02": {
            "name": "ATLAS CORE",
            "merchant": "STRIPE INTERNATIONAL",
            "api_version": "v4.0.0",
            "environment": "PRODUCTION",
        },
    },
    "gpi": {
        "GPI01": {
            "name": "SWIFT GPI TRACKER",
            "institution": "DEUTSCHE BANK AG",
            "bic": "DEUTDEFF",
            "gpi_member_id": "GPIDB2024",
        },
        "GPI02": {
            "name": "GPI RELAY NODE",
            "institution": "HSBC HOLDINGS",
            "bic": "HSBCGB2L",
            "gpi_member_id": "GPIHSBC24",
        },
    },
    "mt103": {
        "MT101": {
            "name": "SWIFT ALLIANCE LITE2",
            "institution": "JPMORGAN CHASE",
            "bic": "CHASUS33",
            "branch": "NEW YORK HQ",
        },
        "MT102": {
            "name": "SWIFT FIN GATEWAY",
            "institution": "BNP PARIBAS",
            "bic": "BNPAFRPP",
            "branch": "PARIS MAIN",
        },
    },
    "rtgs": {
        "RTG01": {
            "name": "FEDWIRE FUNDS",
            "system": "FEDERAL RESERVE",
            "routing": "021000021",
            "node": "PRIMARY-NYC",
        },
        "RTG02": {
            "name": "TARGET2 LINK",
            "system": "EUROPEAN CENTRAL BANK",
            "routing": "MARKDEFF",
            "node": "FRANKFURT-MAIN",
        },
    },
}

_DEFAULT_BIN_DATABASE = {
    "4": "VISA",
    "40": "VISA CLASSIC",
    "41": "VISA CLASSIC",
    "42": "VISA CLASSIC",
    "43": "VISA CLASSIC",
    "44": "VISA GOLD",
    "45": "VISA PLATINUM",
    "46": "VISA BUSINESS",
    "47": "VISA SIGNATURE",
    "48": "VISA INFINITE",
    "49": "VISA CORPORATE",
    "51": "MASTERCARD STANDARD",
    "52": "MASTERCARD STANDARD",
    "53": "MASTERCARD WORLD",
    "54": "MASTERCARD WORLD ELITE",
    "55": "MASTERCARD CORPORATE",
    "22": "MASTERCARD (2-SERIES)",
    "23": "MASTERCARD (2-SERIES)",
    "24": "MASTERCARD (2-SERIES)",
    "25": "MASTERCARD (2-SERIES)",
    "26": "MASTERCARD (2-SERIES)",
    "27": "MASTERCARD (2-SERIES)",
    "34": "AMERICAN EXPRESS",
    "37": "AMERICAN EXPRESS",
    "60": "DISCOVER",
    "65": "DISCOVER",
    "35": "JCB",
    "62": "UNIONPAY",
    "36": "DINERS CLUB",
    "38": "DINERS CLUB",
}

_DEFAULT_LOADING_MESSAGES = {
    "protocol_transaction": [
        "Initializing protocol handshake layer",
        "Establishing issuer authentication channel",
        "Validating cryptographic session keys",
        "Synchronizing with card network gateway",
        "Performing EMV chip verification sequence",
        "Generating digital signature envelope",
    ],
    "interbank": [
        "Connecting to SWIFT Alliance network",
        "Synchronizing interbank ledger nodes",
        "Verifying correspondent bank routes",
        "Authenticating with central clearing house",
        "Validating nostro/vostro account balances",
        "Establishing multi-hop settlement path",
    ],
    "ip_to_ip": [
        "Initializing peer-to-peer tunnel interface",
        "Performing mutual TLS certificate exchange",
        "Establishing encrypted data channel",
        "Calibrating low-latency routing protocol",
        "Verifying endpoint identity signatures",
        "Synchronizing bilateral netting engine",
    ],
    "s2s": [
        "Authenticating REST API credentials",
        "Establishing OAuth 2.0 bearer session",
        "Validating merchant webhook endpoints",
        "Initializing idempotency key registry",
        "Synchronizing server-side ledger state",
        "Preparing JSON settlement payload",
    ],
    "gpi": [
        "Connecting to SWIFT GPI Tracker service",
        "Registering unique end-to-end transaction reference",
        "Validating GPI member institution credentials",
        "Synchronizing with gpi.swift.com directory",
        "Establishing UETR tracking pipeline",
        "Confirming SLA compliance parameters",
    ],
    "mt103": [
        "Connecting to SWIFT FIN Y-Copy service",
        "Validating MT103 message syntax (ISO 15022)",
        "Performing BIC code directory lookup",
        "Establishing FIN session with receiver",
        "Generating message authentication code",
        "Submitting to SWIFT network queue",
    ],
    "rtgs": [
        "Connecting to central bank RTGS node",
        "Validating participant bank credentials",
        "Checking real-time liquidity positions",
        "Reserving funds in settlement account",
        "Entering payment into gross settlement queue",
        "Initiating irrevocable fund transfer",
    ],
}

_DEFAULT_LOADING_DURATION = {
    "protocol_transaction": 2.0,
    "interbank": 2.5,
    "ip_to_ip": 2.0,
    "s2s": 2.0,
    "gpi": 2.5,
    "mt103": 2.5,
    "rtgs": 2.5,
}


# =====================================================================
# [ CONFIG LOAD / SAVE ]
# =====================================================================
def load_config():
    """Load configuration from config.json. Falls back to defaults if missing."""
    global MODULE_TOKENS, RESULT_CONFIG, RESULT_MESSAGE, TIMING, BIN_DATABASE
    global LOADING_MESSAGES, LOADING_DURATION

    config = None
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except (json.JSONDecodeError, IOError):
            config = None

    if config:
        MODULE_TOKENS = config.get("MODULE_TOKENS", _DEFAULT_MODULE_TOKENS)
        RESULT_CONFIG = config.get("RESULT_CONFIG", _DEFAULT_RESULT_CONFIG)
        RESULT_MESSAGE = config.get("RESULT_MESSAGE", _DEFAULT_RESULT_MESSAGE)
        TIMING = config.get("TIMING", _DEFAULT_TIMING)
        BIN_DATABASE = config.get("BIN_DATABASE", _DEFAULT_BIN_DATABASE)
        LOADING_MESSAGES = config.get("LOADING_MESSAGES", _DEFAULT_LOADING_MESSAGES)
        LOADING_DURATION = config.get("LOADING_DURATION", _DEFAULT_LOADING_DURATION)
    else:
        MODULE_TOKENS = _DEFAULT_MODULE_TOKENS
        RESULT_CONFIG = _DEFAULT_RESULT_CONFIG
        RESULT_MESSAGE = _DEFAULT_RESULT_MESSAGE
        TIMING = _DEFAULT_TIMING
        BIN_DATABASE = _DEFAULT_BIN_DATABASE
        LOADING_MESSAGES = _DEFAULT_LOADING_MESSAGES
        LOADING_DURATION = _DEFAULT_LOADING_DURATION
        save_config()


def save_config():
    """Save current configuration to config.json."""
    config = {
        "MODULE_TOKENS": MODULE_TOKENS,
        "RESULT_CONFIG": RESULT_CONFIG,
        "RESULT_MESSAGE": RESULT_MESSAGE,
        "TIMING": TIMING,
        "BIN_DATABASE": BIN_DATABASE,
        "LOADING_MESSAGES": LOADING_MESSAGES,
        "LOADING_DURATION": LOADING_DURATION,
    }
    try:
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        os.chmod(CONFIG_PATH, 0o600)
    except IOError as e:
        print(f"[WARNING] Failed to save config: {e}", file=sys.stderr)


# Load configuration at module level
load_config()


# =====================================================================
# [ BIN DATABASE — VISA / MASTERCARD AUTO-DETECTION ]
# =====================================================================
# BIN_DATABASE is now loaded from config above

def detect_card_brand(card_number):
    """Auto-detect card brand from BIN (first 6 digits)."""
    if not card_number or len(card_number) < 2:
        return "UNKNOWN", "UNKNOWN"
    # Check 2-digit prefix first (more specific)
    prefix2 = card_number[:2]
    if prefix2 in BIN_DATABASE:
        brand = BIN_DATABASE[prefix2]
        network = "VISA" if brand.startswith("VISA") else \
                  "MASTERCARD" if brand.startswith("MASTERCARD") else \
                  brand.split()[0]
        return network, brand
    # Check 1-digit prefix
    prefix1 = card_number[:1]
    if prefix1 in BIN_DATABASE:
        brand = BIN_DATABASE[prefix1]
        network = brand.split()[0]
        return network, brand
    return "UNKNOWN", "UNKNOWN"


# =====================================================================
# [ GLOBAL BANK REGISTRY ]
# =====================================================================
BANK_REGISTRY = [
    ("UBS", "UBSWCHZH80A", "CH"), ("CHASE", "CHASUS33XXX", "US"),
    ("CITI", "CITIUS33XXX", "US"), ("BARCLAYS", "BARCGB22XXX", "GB"),
    ("BOC", "BKCHCNBJ110", "CN"), ("DBS", "DBSSSGSGXXX", "SG"),
    ("MUFG", "BOTKJPJTXXX", "JP"), ("SANTANDER", "BSCHESMMXXX", "ES"),
    ("ING", "INGBNL2AXXX", "NL"), ("SCB", "SCBLSGSGXXX", "SG"),
    ("DEUTSCHE", "DEUTDEFFXXX", "DE"), ("HSBC", "HSBCGB2LXXX", "GB"),
    ("WELLS FARGO", "WFBIUS6SXXX", "US"), ("JPMORGAN", "CHASUS33XXX", "US"),
    ("BNP PARIBAS", "BNPAFRPPXXX", "FR"), ("CREDIT SUISSE", "CRESCHZZXXX", "CH"),
    ("GOLDMAN SACHS", "GOLDUS33XXX", "US"), ("COMMERZBANK", "COBADEFFXXX", "DE"),
    ("SOCIETE GENERALE", "SOGEFRPPXXX", "FR"), ("NORDEA", "NDEAFIHHXXX", "FI"),
    ("ANZ", "ANZBAU3MXXX", "AU"), ("WESTPAC", "WPACAU2SXXX", "AU"),
    ("BCA", "CENAIDJA", "ID"), ("MANDIRI", "BMRIIDJA", "ID"),
    ("BRI", "BRINIDJA", "ID"), ("BNI", "BNINIDJA", "ID"),
]

GLOBAL_BANKS_LIST = [
    "BCA (Bank Central Asia)", "Bank Mandiri", "BRI (Bank Rakyat Indonesia)",
    "BNI (Bank Negara Indonesia)", "CIMB Niaga", "Bank Danamon",
    "JPMorgan Chase (USA)", "Bank of America (USA)", "Wells Fargo (USA)",
    "Citigroup (USA)", "HSBC (UK/Global)", "Barclays (UK)",
    "Deutsche Bank (Germany)", "BNP Paribas (France)", "UBS Group (Switzerland)",
    "Credit Suisse (Switzerland)", "DBS Bank (Singapore)", "MUFG (Japan)",
    "Santander (Spain)", "ING Group (Netherlands)", "Commonwealth Bank (Australia)",
    "Standard Chartered (UK)", "Goldman Sachs (USA)", "ANZ (Australia)",
]

CURRENCIES = ["EUR", "USD", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", "SGD", "IDR"]

TRANSACTION_PROTOCOLS = [
    "101.1 Online 6 DG", "101.1 Online 4 DG", "101.2 Cloud Sale 6 DG",
    "101.3 Cloud Purchase 4 DG", "101.3 Cloud Purchase 6 DG",
    "101.4 Cloud Purchase 4 DG", "101.4 Cloud Purchase 6 DG",
    "101.5 MO/TO Cloud", "101.6 Cloud Pre-Auth",
    "201 Offline Auth", "201.1 Cloud Completion",
    "201.2 Offline Post", "201.3 Offline 6 DG",
]

USDT_NETWORKS = [
    "USDT - TRC20 (Tron)", "USDT - ERC20 (Ethereum)",
    "USDT - BEP20 (BSC)", "USDT - SOL (Solana)", "USDT - MATIC (Polygon)",
]


# =====================================================================
# [ ACCOUNT HOLDER LOOKUP ]
# =====================================================================
ACCOUNT_HOLDER_MAP = {
    "1640004347177": "HARVIANSYAH KURNIAWAN",
    "1100004416787": "PT.RAJAWALI NUSINDO",
}

# =====================================================================
# [ TERMINAL STYLING — ANSI CODES ]
# =====================================================================
class S:
    """ANSI escape codes for terminal styling."""
    H = '\033[95m'; C = '\033[96m'; B = '\033[94m'
    G = '\033[92m'; Y = '\033[93m'; R = '\033[91m'
    W = '\033[97m'; BD = '\033[1m'; DM = '\033[2m'
    UL = '\033[4m'; RST = '\033[0m'; BL = '\033[5m'
    # Extended
    ORANGE = '\033[38;5;208m'
    PURPLE = '\033[38;5;141m'
    TEAL = '\033[38;5;43m'
    GOLD = '\033[38;5;220m'

    @staticmethod
    def init():
        if os.name == 'nt':
            os.system('')


# =====================================================================
# [ UTILITY FUNCTIONS ]
# =====================================================================
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def ts():
    return datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]

def datestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def gen_ref(prefix="TRN"):
    return f"{prefix}-{random.randint(10000,99999)}-{random.choice(string.ascii_uppercase)}{random.randint(10,99)}{random.choice(string.ascii_uppercase)}"

def gen_uetr():
    """Generate UUID-like UETR for GPI tracking."""
    chars = string.hexdigits[:16]
    parts = [
        ''.join(random.choices(chars, k=8)),
        ''.join(random.choices(chars, k=4)),
        ''.join(random.choices(chars, k=4)),
        ''.join(random.choices(chars, k=4)),
        ''.join(random.choices(chars, k=12)),
    ]
    return '-'.join(parts)

def gen_session_id():
    seed = f"{time.time()}{random.randint(0,99999)}"
    return hashlib.sha256(seed.encode()).hexdigest()[:20].upper()

def gen_tx_hash():
    return "0x" + hashlib.sha256(f"{time.time()}{random.random()}".encode()).hexdigest()[:64]

def gen_iban(country="GB"):
    return f"{country}{random.randint(10,99)}{''.join([str(random.randint(0,9)) for _ in range(20)])}"


def header(title, subtitle=None, width=66, color=S.C):
    """Print formatted header box."""
    border = "═" * width
    print(f"\n{color}{S.BD}╔{border}╗{S.RST}")
    pad = (width - len(title)) // 2
    print(f"{color}{S.BD}║{' '*pad}{S.W}{S.BD}{title}{color}{' '*(width-pad-len(title))}║{S.RST}")
    if subtitle:
        pad_s = (width - len(subtitle)) // 2
        print(f"{color}{S.BD}║{S.DM}{' '*pad_s}{subtitle}{' '*(width-pad_s-len(subtitle))}{color}{S.BD}║{S.RST}")
    print(f"{color}{S.BD}╚{border}╝{S.RST}")

def sep(width=66, ch="─"):
    print(f"  {S.DM}{ch * width}{S.RST}")

def status(tag, msg, st=None, color=S.C):
    tag_s = f"{color}[{tag}]{S.RST}"
    if st:
        sc = S.G if st in ("OK","VERIFIED","PASSED","ACTIVE","CLEAN","CONNECTED") else \
             S.R if st in ("FAIL","ERROR","REJECTED","DENIED") else S.Y
        print(f"  {tag_s} {msg} {sc}[{st}]{S.RST}")
    else:
        print(f"  {tag_s} {msg}")

def slow_type(text, delay=0.03, color=S.RST):
    sys.stdout.write(color)
    for ch in text:
        sys.stdout.write(ch); sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(S.RST + '\n')


def progress(label, duration=3.0, width=35, color=S.G):
    """Animated progress bar."""
    step = duration / width
    for i in range(width):
        filled = i + 1
        empty = width - filled
        bar_str = f"{S.DM}{'░' * empty}{S.RST}{color}{'█' * filled}{S.RST}"
        pct = int((filled / width) * 100)
        sys.stdout.write(f"\r  {S.C}[SYS]{S.RST} {label} [{bar_str}] {S.G}{pct:>3}%{S.RST}")
        sys.stdout.flush()
        time.sleep(step)
    sys.stdout.write(f"\r  {S.C}[SYS]{S.RST} {label} [{color}{'█' * width}{S.RST}] {S.G}{S.BD}100%{S.RST}\n")

def spinner(label, duration=2.0):
    """Braille spinner animation."""
    chars = ['⣾','⣽','⣻','⢿','⡿','⣟','⣯','⣷']
    start = time.time()
    i = 0
    while time.time() - start < duration:
        elapsed = time.time() - start
        pct = min(int((elapsed/duration)*100), 99)
        sys.stdout.write(f"\r  {S.C}[{chars[i%len(chars)]}]{S.RST} {label} {S.DM}({pct}%){S.RST}")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write(f"\r  {S.G}[✓]{S.RST} {label} {S.G}(100%){S.RST}  \n")

def multi_spinner(label, duration=2.0):
    """Double spinner with dots."""
    frames = ['◐','◓','◑','◒']
    dots = ['   ', '.  ', '.. ', '...']
    start = time.time()
    i = 0
    while time.time() - start < duration:
        sys.stdout.write(f"\r  {S.Y}[{frames[i%4]}]{S.RST} {label}{S.Y}{dots[i%4]}{S.RST}")
        sys.stdout.flush()
        time.sleep(0.15)
        i += 1
    sys.stdout.write(f"\r  {S.G}[●]{S.RST} {label} {S.G}[DONE]{S.RST}   \n")


def scanning_animation(label, duration=1.5):
    """Hex scanning animation."""
    start = time.time()
    while time.time() - start < duration:
        hex_data = ' '.join([f"{random.randint(0,255):02X}" for _ in range(8)])
        sys.stdout.write(f"\r  {S.DM}[SCAN]{S.RST} {label} {S.DM}│ {hex_data} │{S.RST}")
        sys.stdout.flush()
        time.sleep(0.06)
    sys.stdout.write(f"\r  {S.G}[LOCK]{S.RST} {label} {S.G}│ SIGNATURE CAPTURED{S.RST}              \n")

def trace_hop_animation(hop_num, node_name, node_type, duration=1.2):
    """Animate a single trace hop."""
    frames = ['▹▹▹▹▹', '▸▹▹▹▹', '▸▸▹▹▹', '▸▸▸▹▹', '▸▸▸▸▹', '▸▸▸▸▸']
    latency = random.randint(12, 189)
    start = time.time()
    i = 0
    while time.time() - start < duration:
        frame = frames[i % len(frames)]
        sys.stdout.write(f"\r  {S.Y}HOP {hop_num:02d}{S.RST} {S.C}{frame}{S.RST} {node_name:<25} [{node_type}]")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write(f"\r  {S.G}HOP {hop_num:02d}{S.RST} {S.G}▸▸▸▸▸{S.RST} {node_name:<25} [{node_type}] {S.DM}{latency}ms{S.RST} {S.G}✓{S.RST}\n")

def get_masked_input(prompt=""):
    """Get password input with masking."""
    sys.stdout.write(prompt); sys.stdout.flush()
    password = ""
    try:
        import tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1)
                if ch in ('\r','\n'):
                    sys.stdout.write('\r\n'); break
                elif ch in ('\x7f','\x08'):
                    if password:
                        password = password[:-1]
                        sys.stdout.write('\b \b'); sys.stdout.flush()
                elif ch == '\x03':
                    sys.stdout.write('\r\n'); raise KeyboardInterrupt
                else:
                    password += ch
                    sys.stdout.write('•'); sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
    except (ImportError, OSError):
        import getpass
        password = getpass.getpass(prompt="")
    return password


def input_expiry_mmyy(prompt=""):
    """Read MM/YY expiry with auto-inserted '/' after 2 digits."""
    sys.stdout.write(prompt)
    sys.stdout.flush()
    result = ""
    try:
        import tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1)
                if ch in ('\r', '\n'):
                    sys.stdout.write('\r\n')
                    break
                elif ch in ('\x7f', '\x08'):
                    if result:
                        if result[-1] == '/':
                            result = result[:-1]
                            sys.stdout.write('\b \b')
                            sys.stdout.flush()
                        result = result[:-1]
                        sys.stdout.write('\b \b')
                        sys.stdout.flush()
                elif ch == '\x03':
                    sys.stdout.write('\r\n')
                    raise KeyboardInterrupt
                elif ch.isdigit():
                    raw_digits = result.replace('/', '')
                    if len(raw_digits) >= 4:
                        continue
                    result += ch
                    sys.stdout.write(ch)
                    sys.stdout.flush()
                    raw_digits = result.replace('/', '')
                    if len(raw_digits) == 2 and '/' not in result:
                        result += '/'
                        sys.stdout.write('/')
                        sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
    except (ImportError, OSError):
        result = input("")
    return result


def module_spinner(module_key, count=3):
    """Run module-specific loading spinners from config."""
    messages = LOADING_MESSAGES.get(module_key, ["Processing..."])
    duration = LOADING_DURATION.get(module_key, 2.0)
    per_msg_duration = duration / min(count, len(messages))
    min_duration = 0.5
    per_msg_duration = max(per_msg_duration, min_duration)
    selected = messages[:count] if len(messages) >= count else messages
    for msg in selected:
        spinner(msg, per_msg_duration)


def display_customer_info_box(user_data):
    """Display formatted box with customer data fields."""
    cardholder = user_data.get("cardholder", "N/A")
    bank_provider = user_data.get("bank_provider", "N/A")
    iso_country = user_data.get("iso_country", "N/A")
    iso_a2 = user_data.get("iso_a2", "N/A")
    iso_a3 = user_data.get("iso_a3", "N/A")
    iso_num = user_data.get("iso_num", "N/A")

    box_width = 54
    print(f"\n  {S.C}{S.BD}\u250c{'─' * box_width}\u2510{S.RST}")
    print(f"  {S.C}{S.BD}\u2502{S.RST} {S.W}{S.BD}{'CUSTOMER DATA':^{box_width - 2}}{S.RST} {S.C}{S.BD}\u2502{S.RST}")
    print(f"  {S.C}{S.BD}\u251c{'─' * box_width}\u2524{S.RST}")
    print(f"  {S.C}{S.BD}\u2502{S.RST}  {S.DM}Cardholder  :{S.RST} {S.W}{S.BD}{cardholder:<36}{S.RST} {S.C}{S.BD}\u2502{S.RST}")
    print(f"  {S.C}{S.BD}\u2502{S.RST}  {S.DM}Bank        :{S.RST} {S.W}{bank_provider:<36}{S.RST} {S.C}{S.BD}\u2502{S.RST}")
    print(f"  {S.C}{S.BD}\u2502{S.RST}  {S.DM}Country     :{S.RST} {S.W}{iso_country:<36}{S.RST} {S.C}{S.BD}\u2502{S.RST}")
    print(f"  {S.C}{S.BD}\u2502{S.RST}  {S.DM}ISO Alpha-2 :{S.RST} {S.W}{iso_a2:<36}{S.RST} {S.C}{S.BD}\u2502{S.RST}")
    print(f"  {S.C}{S.BD}\u2502{S.RST}  {S.DM}ISO Alpha-3 :{S.RST} {S.W}{iso_a3:<36}{S.RST} {S.C}{S.BD}\u2502{S.RST}")
    print(f"  {S.C}{S.BD}\u2502{S.RST}  {S.DM}ISO Numeric :{S.RST} {S.W}{iso_num:<36}{S.RST} {S.C}{S.BD}\u2502{S.RST}")
    print(f"  {S.C}{S.BD}\u2514{'─' * box_width}\u2518{S.RST}")


def system_status_bar(module_name):
    """Display a system status bar at the top of each module."""
    session = gen_session_id()[:12]
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"  {S.DM}\u250c{'─' * 66}\u2510{S.RST}")
    print(f"  {S.DM}\u2502 {S.C}MODULE{S.DM}: {S.W}{module_name:<20}{S.DM} {S.C}SESSION{S.DM}: {S.W}{session}  {S.C}TIME{S.DM}: {S.W}{now}{S.DM} \u2502{S.RST}")
    print(f"  {S.DM}\u2514{'─' * 66}\u2518{S.RST}")
    print()


def show_result(module_key, tx_details):
    """Display transaction result based on RESULT_CONFIG."""
    result = RESULT_CONFIG.get(module_key, "SUCCESS").upper()
    custom_msg = RESULT_MESSAGE.get(module_key, "")

    print()
    if result == "SUCCESS":
        msg = custom_msg or "Transaction settled successfully. Funds confirmed."
        print(f"  {S.G}{S.BD}╔{'═'*60}╗{S.RST}")
        print(f"  {S.G}{S.BD}║{'SETTLEMENT SUCCESSFUL':^60}║{S.RST}")
        print(f"  {S.G}{S.BD}╠{'═'*60}╣{S.RST}")
        for k, v in tx_details.items():
            line = f"  {k}: {v}"
            print(f"  {S.G}{S.BD}║{S.RST}  {S.W}{k:<18}: {S.G}{v}{S.RST}{'':>{38-len(str(v))-len(k)}}{S.G}{S.BD}║{S.RST}")
        print(f"  {S.G}{S.BD}║{S.RST}  {S.W}{'Status':<18}: {S.G}{msg}{S.RST}{'':>{38-len(msg)}}{S.G}{S.BD}║{S.RST}")
        print(f"  {S.G}{S.BD}╚{'═'*60}╝{S.RST}")
    elif result == "PENDING":
        msg = custom_msg or "Transaction queued for manual review."
        print(f"  {S.Y}{S.BD}╔{'═'*60}╗{S.RST}")
        print(f"  {S.Y}{S.BD}║{'SETTLEMENT PENDING':^60}║{S.RST}")
        print(f"  {S.Y}{S.BD}╠{'═'*60}╣{S.RST}")
        for k, v in tx_details.items():
            print(f"  {S.Y}{S.BD}║{S.RST}  {S.W}{k:<18}: {S.Y}{v}{S.RST}{'':>{38-len(str(v))-len(k)}}{S.Y}{S.BD}║{S.RST}")
        print(f"  {S.Y}{S.BD}║{S.RST}  {S.W}{'Status':<18}: {S.Y}{msg}{S.RST}{'':>{38-len(msg)}}{S.Y}{S.BD}║{S.RST}")
        print(f"  {S.Y}{S.BD}╚{'═'*60}╝{S.RST}")
    else:
        msg = custom_msg or "Transaction declined by settlement engine."
        print(f"  {S.R}{S.BD}╔{'═'*60}╗{S.RST}")
        print(f"  {S.R}{S.BD}║{'SETTLEMENT FAILED':^60}║{S.RST}")
        print(f"  {S.R}{S.BD}╠{'═'*60}╣{S.RST}")
        for k, v in tx_details.items():
            print(f"  {S.R}{S.BD}║{S.RST}  {S.W}{k:<18}: {S.R}{v}{S.RST}{'':>{38-len(str(v))-len(k)}}{S.R}{S.BD}║{S.RST}")
        print(f"  {S.R}{S.BD}║{S.RST}  {S.W}{'Reason':<18}: {S.R}{msg}{S.RST}{'':>{38-len(msg)}}{S.R}{S.BD}║{S.RST}")
        print(f"  {S.R}{S.BD}╚{'═'*60}╝{S.RST}")
    print()


def settlement_progress(module_key, duration=None):
    """Final settlement progress bar with result."""
    if duration is None:
        duration = TIMING["settlement_duration"]
    
    result = RESULT_CONFIG.get(module_key, "SUCCESS").upper()
    total = 50

    if result == "FAILED":
        fail_at = random.randint(35, 42)
        green_duration = duration * 0.82
        yellow_duration = duration * 0.10
        pause_duration = duration * 0.08

        sys.stdout.write(f"  {S.C}[TX]{S.RST} Settlement propagation: [")
        sys.stdout.flush()
        for i in range(fail_at):
            sys.stdout.write(f"{S.G}█{S.RST}")
            sys.stdout.flush()
            time.sleep(green_duration / fail_at)
        for i in range(3):
            sys.stdout.write(f"{S.Y}█{S.RST}")
            sys.stdout.flush()
            time.sleep(yellow_duration / 3)
        time.sleep(pause_duration)
        remaining = total - fail_at - 3
        sys.stdout.write(f"{S.R}{'█'*2}{S.RST}{S.DM}{'░'*(remaining-2)}{S.RST}] {S.R}{S.BD}FAILED{S.RST}\n")
    elif result == "PENDING":
        pend_at = random.randint(38, 45)
        step_time = duration / pend_at
        sys.stdout.write(f"  {S.C}[TX]{S.RST} Settlement propagation: [")
        sys.stdout.flush()
        for i in range(pend_at):
            sys.stdout.write(f"{S.G}█{S.RST}")
            sys.stdout.flush()
            time.sleep(step_time)
        remaining = total - pend_at
        sys.stdout.write(f"{S.Y}{'█'*remaining}{S.RST}] {S.Y}{S.BD}PENDING{S.RST}\n")
    else:
        step_time = duration / total
        sys.stdout.write(f"  {S.C}[TX]{S.RST} Settlement propagation: [")
        sys.stdout.flush()
        for i in range(total):
            sys.stdout.write(f"{S.G}█{S.RST}")
            sys.stdout.flush()
            time.sleep(step_time)
        sys.stdout.write(f"] {S.G}{S.BD}CONFIRMED{S.RST}\n")


# =====================================================================
# [ MODULE ASCII LOGOS ]
# =====================================================================
LOGOS = {
    "main": f"""{S.C}
    ╔═══════════════════════════════════════════════════════════════════╗
    ║   ██████╗ ██████╗ ███████╗███████╗    ███████╗███╗   ██╗ ██████╗║
    ║  ██╔════╝ ██╔══██╗██╔════╝██╔════╝    ██╔════╝████╗  ██║██╔════╝║
    ║  ██║  ███╗██████╔╝███████╗█████╗      █████╗  ██╔██╗ ██║██║  ███║
    ║  ██║   ██║██╔═══╝ ╚════██║██╔══╝      ██╔══╝  ██║╚██╗██║██║   ██║
    ║  ╚██████╔╝██║     ███████║███████╗    ███████╗██║ ╚████║╚██████╔╝║
    ║   ╚═════╝ ╚═╝     ╚══════╝╚══════╝    ╚══════╝╚═╝  ╚═══╝ ╚═════╝║
    ║           GLOBAL PAYMENT SETTLEMENT ENGINE v{VERSION}             ║
    ╚═══════════════════════════════════════════════════════════════════╝
{S.RST}""",

    "protocol": f"""{S.ORANGE}
    ╔═══════════════════════════════════════════════════════╗
    ║  ██████╗ ██████╗  ██████╗ ████████╗ ██████╗  ██████╗║
    ║  ██╔══██╗██╔══██╗██╔═══██╗╚══██╔══╝██╔═══██╗██╔════╝║
    ║  ██████╔╝██████╔╝██║   ██║   ██║   ██║   ██║██║     ║
    ║  ██╔═══╝ ██╔══██╗██║   ██║   ██║   ██║   ██║██║     ║
    ║  ██║     ██║  ██║╚██████╔╝   ██║   ╚██████╔╝╚██████╗║
    ║  ╚═╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝  ╚═════╝║
    ║        PROTOCOL TRANSACTION ENGINE v3.1               ║
    ╚═══════════════════════════════════════════════════════╝
{S.RST}""",

    "interbank": f"""{S.C}
    ██╗███╗   ██╗████████╗███████╗██████╗ ██████╗  █████╗ ███╗   ██╗██╗  ██╗
    ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██╔══██╗████╗  ██║██║ ██╔╝
    ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝██████╔╝███████║██╔██╗ ██║█████╔╝
    ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗██╔══██╗██╔══██║██║╚██╗██║██╔═██╗
    ██║██║ ╚████║   ██║   ███████╗██║  ██║██████╔╝██║  ██║██║ ╚████║██║  ██╗
    ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝
{S.RST}""",
}


LOGOS["ip2ip"] = f"""{S.TEAL}
    ╔═══════════════════════════════════════════════════╗
    ║  ██╗██████╗     ████████╗ ██████╗     ██╗██████╗ ║
    ║  ██║██╔══██╗    ╚══██╔══╝██╔═══██╗    ██║██╔══██╗║
    ║  ██║██████╔╝       ██║   ██║   ██║    ██║██████╔╝║
    ║  ██║██╔═══╝        ██║   ██║   ██║    ██║██╔═══╝ ║
    ║  ██║██║            ██║   ╚██████╔╝    ██║██║     ║
    ║  ╚═╝╚═╝            ╚═╝    ╚═════╝     ╚═╝╚═╝     ║
    ║     DIRECT IP TRANSFER PROTOCOL v2.4              ║
    ╚═══════════════════════════════════════════════════╝
{S.RST}"""

LOGOS["s2s"] = f"""{S.PURPLE}
    ╔═══════════════════════════════════════════════════╗
    ║  ███████╗██████╗ ███████╗    ███████╗██████╗ ██╗ ║
    ║  ██╔════╝╚════██╗██╔════╝    ██╔════╝██╔══██╗██║ ║
    ║  ███████╗ █████╔╝███████╗    ███████╗██████╔╝██║ ║
    ║  ╚════██║██╔═══╝ ╚════██║    ╚════██║██╔═══╝ ██║ ║
    ║  ███████║███████╗███████║    ███████║██║     ██║ ║
    ║  ╚══════╝╚══════╝╚══════╝    ╚══════╝╚═╝     ╚═╝ ║
    ║    SERVER-TO-SERVER SETTLEMENT API v4.0            ║
    ╚═══════════════════════════════════════════════════╝
{S.RST}"""

LOGOS["gpi"] = f"""{S.GOLD}
    ╔═══════════════════════════════════════════════════╗
    ║   ██████╗ ██████╗ ██╗    ████████╗██████╗  ██╗  ║
    ║  ██╔════╝ ██╔══██╗██║    ╚══██╔══╝██╔══██╗██╔╝  ║
    ║  ██║  ███╗██████╔╝██║       ██║   ██████╔╝██║   ║
    ║  ██║   ██║██╔═══╝ ██║       ██║   ██╔══██╗██║   ║
    ║  ╚██████╔╝██║     ██║       ██║   ██║  ██║╚██╗  ║
    ║   ╚═════╝ ╚═╝     ╚═╝       ╚═╝   ╚═╝  ╚═╝ ╚═╝  ║
    ║   SWIFT GPI — Global Payment Innovation v6.0      ║
    ╚═══════════════════════════════════════════════════╝
{S.RST}"""

LOGOS["mt103"] = f"""{S.B}
    ╔═══════════════════════════════════════════════════╗
    ║  ███╗   ███╗████████╗ ██╗ ██████╗  ██████╗      ║
    ║  ████╗ ████║╚══██╔══╝███║██╔═████╗ ╚════██╗     ║
    ║  ██╔████╔██║   ██║   ╚██║██║██╔██║  █████╔╝     ║
    ║  ██║╚██╔╝██║   ██║    ██║████╔╝██║  ╚═══██╗     ║
    ║  ██║ ╚═╝ ██║   ██║    ██║╚██████╔╝██████╔╝      ║
    ║  ╚═╝     ╚═╝   ╚═╝    ╚═╝ ╚═════╝ ╚═════╝       ║
    ║   SWIFT MT103 — Single Customer Credit Transfer   ║
    ╚═══════════════════════════════════════════════════╝
{S.RST}"""

LOGOS["rtgs"] = f"""{S.G}
    ╔═══════════════════════════════════════════════════╗
    ║  ██████╗ ████████╗ ██████╗ ███████╗             ║
    ║  ██╔══██╗╚══██╔══╝██╔════╝ ██╔════╝             ║
    ║  ██████╔╝   ██║   ██║  ███╗███████╗             ║
    ║  ██╔══██╗   ██║   ██║   ██║╚════██║             ║
    ║  ██║  ██║   ██║   ╚██████╔╝███████║             ║
    ║  ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚══════╝             ║
    ║  Real-Time Gross Settlement System v8.2           ║
    ╚═══════════════════════════════════════════════════╝
{S.RST}"""


# =====================================================================
# [ BOOT SEQUENCE ]
# =====================================================================
def phase_boot():
    """System boot sequence."""
    clear()
    print(LOGOS["main"])
    print(f"  {S.DM}{'─'*68}{S.RST}")
    print(f"  {S.W}{S.BD}   ▸▸▸  GLOBAL PAYMENT SETTLEMENT ENGINE  ◂◂◂{S.RST}")
    print(f"  {S.DM}  Protocol: MULTI-NET | Encryption: AES-256-GCM | TLS 1.3{S.RST}")
    print(f"  {S.DM}  Build: {BUILD} | Modules: 7 | Status: OPERATIONAL{S.RST}")
    print(f"  {S.DM}{'─'*68}{S.RST}\n")
    time.sleep(1)

    boot_items = [
        ("KERNEL", "Loading secure kernel module v4.19.2"),
        ("CRYPTO", "Initializing OpenSSL 3.1.4 / LibreSSL 3.8.1"),
        ("NET", "Binding to Multi-Protocol Network Interface"),
        ("HSM", "Hardware Security Module handshake (Thales Luna 7)"),
        ("PKI", "Loading X.509 certificate chain (4096-bit RSA)"),
        ("AUTH", "Starting PAM authentication daemon"),
        ("AUDIT", "Enabling ISO 27001 compliance audit logger"),
        ("MEM", "Allocating 2048MB secure memory partition"),
        ("CLOCK", "NTP sync to stratum-1 (deviation: <2ms)"),
        ("CORE", "Connecting to Settlement Core Engine v12.7"),
    ]
    for tag, msg in boot_items:
        status(tag, msg, "OK")
        time.sleep(random.uniform(0.15, 0.4))

    print()
    progress("System Initialization", duration=TIMING["boot_progress"], width=40)
    print()
    print(f"  {S.G}{S.BD}  ████  SYSTEM READY  ████{S.RST}")
    print(f"  {S.DM}  Uptime: 0d 0h 0m | Load: 0.42 | Mem: 67%{S.RST}")
    time.sleep(1.5)


# =====================================================================
# [ MAIN MENU ]
# =====================================================================
def main_menu():
    """Display main module selection menu."""
    clear()
    print(LOGOS["main"])
    print(f"  {S.DM}{'─'*68}{S.RST}")
    print(f"  {S.W}{S.BD}  SELECT TRANSACTION MODULE{S.RST}")
    print(f"  {S.DM}  Build {BUILD} | {len(MODULE_TOKENS)} Active Modules | Status: OPERATIONAL{S.RST}")
    print(f"  {S.DM}{'─'*68}{S.RST}\n")

    modules = [
        ("1", "Protocol Transaction", "Card-based multi-protocol settlement (Visa/MC auto-detect)", S.ORANGE),
        ("2", "Interbank Transfer", "SWIFT Network interbank fund settlement engine", S.C),
        ("3", "IP-to-IP Transfer", "Direct peer-to-peer IP tunnel fund transfer", S.TEAL),
        ("4", "Server-to-Server (S2S)", "REST API settlement between payment servers", S.PURPLE),
        ("5", "SWIFT GPI", "Global Payment Innovation real-time tracker", S.GOLD),
        ("6", "MT103 Transfer", "SWIFT MT103 single customer credit transfer", S.B),
        ("7", "RTGS Settlement", "Real-Time Gross Settlement System", S.G),
    ]

    for num, name, desc, color in modules:
        print(f"  {color}{S.BD} [{num}]{S.RST}  {S.W}{S.BD}{name}{S.RST}")
        print(f"        {S.DM}{desc}{S.RST}\n")

    print(f"  {S.C}{S.BD} [8]{S.RST}  {S.W}{S.BD}Settings Editor{S.RST}")
    print(f"        {S.DM}Configure tokens, timing, and messages{S.RST}\n")

    print(f"  {S.R}{S.BD} [0]{S.RST}  {S.DM}Exit Terminal{S.RST}\n")
    sep()

    choice = input(f"\n  {S.Y}\u25b8 Select Module [0-8] : {S.RST}").strip()
    return choice


# =====================================================================
# [ MODULE 1: PROTOCOL TRANSACTION (Code B - CLI) ]
# =====================================================================
def module_protocol_transaction():
    """Protocol Transaction — converted from GUI to CLI with BIN detection."""
    clear()
    print(LOGOS["protocol"])
    system_status_bar("PROTOCOL TRANSACTION")
    print(f"  {S.DM}{'─'*60}{S.RST}")
    print(f"  {S.ORANGE}{S.BD}  PROTOCOL TRANSACTION ENGINE{S.RST}")
    print(f"  {S.DM}  Card-based settlement with Visa/Mastercard auto-detection{S.RST}")
    print(f"  {S.DM}{'─'*60}{S.RST}\n")

    # Token Auth
    tokens = MODULE_TOKENS["protocol_transaction"]
    print(f"  {S.C}[AUTH]{S.RST} Enter 5-character Access Token:")
    token_input = input(f"  {S.Y}▸ Token : {S.RST}").strip().upper()

    if token_input not in tokens:
        print(f"\n  {S.R}[✗] ACCESS DENIED — Invalid token for Protocol module.{S.RST}")
        input(f"\n  {S.DM}Press ENTER to return...{S.RST}")
        return

    user_data = tokens[token_input]
    print(f"\n  {S.G}[✓]{S.RST} Authenticated as: {S.W}{S.BD}{user_data['name']}{S.RST}")
    module_spinner("protocol_transaction", count=2)
    print()

    # Protocol Selection
    print(f"  {S.W}{S.BD}  AVAILABLE PROTOCOLS:{S.RST}\n")
    for i, proto in enumerate(TRANSACTION_PROTOCOLS, 1):
        print(f"    {S.ORANGE}[{i:2d}]{S.RST} {proto}")
    print()
    
    proto_choice = input(f"  {S.Y}▸ Select Protocol [1-{len(TRANSACTION_PROTOCOLS)}] : {S.RST}").strip()
    try:
        proto_idx = int(proto_choice) - 1
        if 0 <= proto_idx < len(TRANSACTION_PROTOCOLS):
            selected_proto = TRANSACTION_PROTOCOLS[proto_idx]
        else:
            selected_proto = TRANSACTION_PROTOCOLS[0]
    except ValueError:
        selected_proto = TRANSACTION_PROTOCOLS[0]

    print(f"\n  {S.G}[✓]{S.RST} Protocol: {S.W}{S.BD}{selected_proto}{S.RST}")
    spinner("Connecting to issuer network", 1.5)

    # Card Input with BIN detection
    print(f"\n  {S.W}{S.BD}  CARD DETAILS{S.RST}")
    sep(40)
    card_num = input(f"  {S.Y}▸ Card Number (16 digits) : {S.RST}").strip().replace(" ", "").replace("-", "")

    if len(card_num) != 16 or not card_num.isdigit():
        print(f"  {S.R}[✗] Invalid card number format.{S.RST}")
        input(f"\n  {S.DM}Press ENTER to return...{S.RST}")
        return

    # BIN Auto-Detection
    network, brand = detect_card_brand(card_num)
    last4 = card_num[-4:]

    # Check allowed card
    allowed = user_data.get("allowed_card_last4")
    if allowed and last4 != allowed:
        print(f"  {S.R}[✗] Card not authorized for this session.{S.RST}")
        input(f"\n  {S.DM}Press ENTER to return...{S.RST}")
        return

    print(f"\n  {S.G}[✓] BIN DETECTED:{S.RST}")
    print(f"      Network : {S.W}{S.BD}{network}{S.RST}")
    print(f"      Type    : {S.W}{brand}{S.RST}")
    print(f"      Card    : {S.DM}**** **** **** {S.W}{last4}{S.RST}")

    # Display customer data from token
    display_customer_info_box(user_data)

    spinner("Validating card BIN with issuer", 1.5)

    # Expiry with MM/YY auto-format
    expiry = input_expiry_mmyy(f"\n  {S.Y}\u25b8 Expiry Date (MM/YY) : {S.RST}")
    spinner("Checking card status", 1.0)


    # Transfer type selection
    print(f"\n  {S.W}{S.BD}  TRANSFER TYPE:{S.RST}")
    print(f"    {S.ORANGE}[1]{S.RST} Bank Transfer")
    print(f"    {S.ORANGE}[2]{S.RST} Crypto Transfer (USDT)")
    tt = input(f"\n  {S.Y}▸ Select [1-2] : {S.RST}").strip()

    tx_data = {
        "protocol": selected_proto,
        "card": f"**** **** **** {last4}",
        "network": network,
        "brand": brand,
    }

    if tt == "2":
        # Crypto Transfer
        print(f"\n  {S.W}{S.BD}  CRYPTO TRANSFER DETAILS{S.RST}")
        sep(40)
        print(f"  {S.DM}  Available Networks:{S.RST}")
        for i, net in enumerate(USDT_NETWORKS, 1):
            print(f"    [{i}] {net}")
        net_choice = input(f"\n  {S.Y}▸ Network : {S.RST}").strip()
        try:
            net_idx = int(net_choice) - 1
            crypto_net = USDT_NETWORKS[net_idx] if 0 <= net_idx < len(USDT_NETWORKS) else USDT_NETWORKS[0]
        except:
            crypto_net = USDT_NETWORKS[0]

        rec_wallet = input(f"  {S.Y}▸ Receiver Wallet : {S.RST}").strip()
        snd_wallet = input(f"  {S.Y}▸ Sender Wallet   : {S.RST}").strip()
        amount = input(f"  {S.Y}▸ Amount (EUR)    : {S.RST}").strip()

        tx_data["type"] = "Crypto Transfer"
        tx_data["crypto_network"] = crypto_net
        tx_data["receiver"] = rec_wallet[:20] + "..." if len(rec_wallet) > 20 else rec_wallet
        tx_data["amount"] = f"EUR {amount}"
    else:
        # Bank Transfer
        print(f"\n  {S.W}{S.BD}  BANK TRANSFER DETAILS{S.RST}")
        sep(40)
        bank_name = input(f"  {S.Y}▸ Destination Bank : {S.RST}").strip()
        ben_name = input(f"  {S.Y}▸ Beneficiary Name : {S.RST}").strip()
        acc_num = input(f"  {S.Y}▸ Account Number   : {S.RST}").strip()
        swift_code = input(f"  {S.Y}▸ SWIFT/BIC Code   : {S.RST}").strip()
        currency = input(f"  {S.Y}▸ Currency [{'/'.join(CURRENCIES[:5])}] : {S.RST}").strip().upper() or "EUR"
        amount = input(f"  {S.Y}▸ Amount           : {S.RST}").strip()

        tx_data["type"] = "Bank Transfer"
        tx_data["bank"] = bank_name
        tx_data["beneficiary"] = ben_name
        tx_data["account"] = acc_num
        tx_data["amount"] = f"{currency} {amount}"

    # Authorization Code
    digits_required = 6 if "6 DG" in selected_proto else 4
    print(f"\n  {S.W}{S.BD}  AUTHORIZATION{S.RST}")
    auth_code = input(f"  {S.Y}▸ Auth Code ({digits_required} digits) : {S.RST}").strip()
    if len(auth_code) != digits_required or not auth_code.isdigit():
        print(f"  {S.R}[✗] Invalid auth code. Expected {digits_required} digits.{S.RST}")
        input(f"\n  {S.DM}Press ENTER to return...{S.RST}")
        return

    # Processing
    print()
    module_spinner("protocol_transaction", count=4)
    print()

    # Settlement
    settlement_progress("protocol_transaction", duration=TIMING["settlement_duration"])

    # Result
    tx_id = f"PTX-{random.randint(100000000, 999999999)}"
    tx_data["TX ID"] = tx_id
    tx_data["Timestamp"] = f"{datestamp()} {ts()}"
    tx_data["Signature"] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=24))

    show_result("protocol_transaction", tx_data)
    input(f"  {S.DM}Press ENTER to return to menu...{S.RST}")


# =====================================================================
# [ MODULE 2: INTERBANK TRANSFER (Code A - Integrated) ]
# =====================================================================
def module_interbank():
    """Interbank Transfer — Full SWIFT network simulation."""
    clear()
    print(LOGOS["interbank"])
    system_status_bar("INTERBANK TRANSFER")
    print(f"  {S.DM}{'─'*68}{S.RST}")
    print(f"  {S.W}{S.BD}        ▸▸▸  INTERBANK TRANSFER TRANSACTION  ◂◂◂{S.RST}")
    print(f"  {S.DM}  Protocol: BANK-SERVER | Encryption: AES-256-GCM | TLS 1.3{S.RST}")
    print(f"  {S.DM}{'─'*68}{S.RST}\n")
    time.sleep(1)

    # Auth
    fake_ip = f"103.{random.randint(10,99)}.{random.randint(100,255)}.{random.randint(2,254)}"
    session_id = gen_session_id()
    print(f"  {S.DM}┌────────────────────────────────────────────────────────────┐{S.RST}")
    print(f"  {S.DM}│{S.RST} {S.C}Server   :{S.RST} {S.W}ibank-server.settlement.net ({fake_ip}){S.RST}  {S.DM}│{S.RST}")
    print(f"  {S.DM}│{S.RST} {S.C}Protocol :{S.RST} {S.W}TLS 1.3 / AES-256-GCM-SHA384{S.RST}           {S.DM}│{S.RST}")
    print(f"  {S.DM}│{S.RST} {S.C}Session  :{S.RST} {S.W}{session_id}{S.RST}             {S.DM}│{S.RST}")
    print(f"  {S.DM}└────────────────────────────────────────────────────────────┘{S.RST}")
    print()

    spinner(f"Establishing secure connection to {fake_ip}", TIMING["auth_connect"])
    print()

    # Login
    max_attempts = 3
    for attempt in range(max_attempts):
        user_input = get_masked_input(f"  {S.Y}▸ Operator ID : {S.RST}")
        pass_input = get_masked_input(f"  {S.Y}▸ Access Key  : {S.RST}")

        admin_token = MODULE_TOKENS["interbank"]["ADMIN"]
        pw_hash = hashlib.sha256(pass_input.encode()).hexdigest()
        if user_input == admin_token["username"] and pw_hash == admin_token["password_hash"]:
            print()
            module_spinner("interbank", count=3)
            print(f"\n  {S.G}{S.BD}[✓] IDENTITY CONFIRMED — ACCESS GRANTED{S.RST}\n")
            time.sleep(1)
            break
        else:
            remaining = max_attempts - attempt - 1
            print(f"\n  {S.R}[✗] ACCESS DENIED{S.RST}")
            if remaining > 0:
                print(f"  {S.DM}    {remaining} attempt(s) remaining.{S.RST}\n")
            else:
                print(f"\n  {S.R}{S.BD}[LOCKED] Terminal disabled.{S.RST}")
                input(f"  {S.DM}Press ENTER to return...{S.RST}")
                return


    # Network Handshake
    clear()
    header("NETWORK HANDSHAKE", "Establishing Multi-Node Secure Tunnel")
    print()
    hops = [
        (1, "LOCAL-GATEWAY", "ENTRY"), (2, "ISP-CORE-ROUTER", "RELAY"),
        (3, "EU-BACKBONE-NODE-7", "TRUNK"), (4, "BANK-PROXY-BRUSSELS", "BANK-SRV"),
        (5, "INTERBANK-CORE-LDN", "CORE"), (6, "SETTLEMENT-ENGINE-A", "TARGET"),
    ]
    for hop_num, node, ntype in hops:
        trace_hop_animation(hop_num, node, ntype, duration=random.uniform(0.7, 1.3))
    print()
    spinner("Performing ECDHE key exchange (P-384)", TIMING["net_ecdhe"])
    spinner("Establishing forward-secrecy channel", TIMING["net_forward_secrecy"])
    progress("Secure Tunnel Establishment", duration=TIMING["net_tunnel_progress"], width=35)
    print(f"\n  {S.G}{S.BD}[✓] CONNECTED TO GLOBAL SETTLEMENT NETWORK{S.RST}\n")
    time.sleep(1)

    # TRN Scan
    clear()
    header("DEEP TRACE — FUND TRACKING ENGINE", "Multi-Node Transaction Scanner")
    print()
    trn_input = input(f"  {S.Y}▸ Enter Target TRN Signature : {S.RST}").strip()
    if not trn_input:
        trn_input = "7743127735841025"
        print(f"  {S.DM}  (Auto-assigned: {trn_input}){S.RST}")
    print()

    scan_nodes = [
        "SWIFT Tracker (Brussels)", "FEDWIRE Real-Time (New York)",
        "TARGET2 Cluster (Frankfurt)", "CHAPS Sterling (London)",
    ]
    for node in scan_nodes:
        multi_spinner(f"Probing {node}", duration=random.uniform(2.0, 4.0))

    print(f"\n  {S.G}[✓]{S.RST} Scan probes deployed.\n")
    time.sleep(0.5)

    # Simulated TRN feed (shorter than original for UX)
    print(f"  {S.DM}  Scanning 10,000,000+ ledger entries...{S.RST}\n")
    for _ in range(random.randint(8, 15)):
        trn_ref = gen_ref("TRN")
        bank = random.choice(BANK_REGISTRY)
        amt = random.randint(100000, 25000000)
        txn_type = random.choice(["WIRE","MT202","SEPA-CT","TARGET2","CHAPS"])
        st = random.choice(["PENDING","CLEARED","SETTLING"])
        sc = S.G if st == "CLEARED" else S.Y
        print(f"  {S.Y}{trn_ref}{S.RST} │ {S.B}{txn_type:<8}{S.RST} │ {S.C}{bank[0]:<12}{S.RST} │ {S.W}€{amt:>12,}{S.RST} │ {sc}{st}{S.RST}")
        time.sleep(random.uniform(0.05, 0.15))

    scanning_animation(f"Batch scan | 9,847,231 scanned", duration=3.0)
    print()
    print(f"  {S.G}{S.BD}  ✓ TARGET SIGNATURE MATCHED — FUND TRACE CONFIRMED{S.RST}\n")
    time.sleep(1)


    # Routing
    clear()
    header("SETTLEMENT ROUTING", "Destination Bank Configuration")
    print()
    
    bank_name = ""
    while True:
        bank_name = input(f"  {S.Y}▸ Destination Bank      : {S.RST}").strip()
        if bank_name and all(c.isalpha() or c.isspace() for c in bank_name):
            break
        print(f"  {S.R}    [!] Bank name required (alphabets only).{S.RST}")

    account_no = ""
    while True:
        account_no = input(f"  {S.Y}▸ Account Number        : {S.RST}").strip()
        if account_no and account_no.isdigit():
            break
        print(f"  {S.R}    [!] Account number required (numbers only).{S.RST}")

    bank_code = input(f"  {S.Y}▸ SWIFT Code            : {S.RST}").strip() or "XXXXXXXXXXX"

    holder_name = ACCOUNT_HOLDER_MAP.get(account_no, "ACCOUNT HOLDER")

    print()
    spinner("Validating SWIFT Code against ISO 9362", TIMING["routing_validate"])
    multi_spinner("Cross-referencing AML/KYC database", TIMING["routing_aml"])
    spinner("Confirming correspondent bank", TIMING["routing_correspondent"])
    print()

    masked_acc = '*' * (len(account_no) - 4) + account_no[-4:] if len(account_no) > 4 else account_no
    print(f"  {S.G}{S.BD}  ROUTING VERIFIED{S.RST}")
    print(f"    Bank    : {S.W}{bank_name.upper()}{S.RST}")
    print(f"    Account : {S.W}{masked_acc}{S.RST}")
    print(f"    Holder  : {S.W}{holder_name}{S.RST}")
    print(f"    AML     : {S.G}CLEARED{S.RST}")
    print()

    input(f"  {S.Y}▸ Press ENTER to initiate settlement...{S.RST}")

    # Settlement Bridge
    clear()
    header("SETTLEMENT BRIDGE", "Institutional Firewall Traversal")
    print()
    firewalls = [
        ("SANCTIONS-SCREEN", "COMPLIANCE"), ("FED-RESERVE-OFAC", "REGULATORY"),
        ("ECB-OVERSIGHT-NODE", "REGULATORY"), ("INTERPOL-I-24/7", "SECURITY"),
        ("FATF-GREYLST-CHECK", "AML"), ("TREASURY-NOSTRO", "BANKING"),
    ]
    for fw_name, fw_type in firewalls:
        sys.stdout.write(f"  {S.B}  [{fw_type:^12}]{S.RST} {fw_name:<24} ")
        sys.stdout.flush()
        for _ in range(random.randint(5, 10)):
            sys.stdout.write(f"{S.Y}·{S.RST}")
            sys.stdout.flush()
            time.sleep(0.08)
        print(f" {S.G}[CLEARED]{S.RST}")
        time.sleep(0.2)

    print()
    progress("Settlement Tunnel Sync", duration=TIMING["bridge_sync_progress"], width=35)
    print(f"\n  {S.G}{S.BD}[✓] BRIDGE ACTIVE{S.RST}\n")
    time.sleep(1)

    # Final Settlement
    print()
    spinner("Signing transaction with HSM key", 1.5)
    spinner("Broadcasting to settlement network", 1.0)
    print()
    settlement_progress("interbank", duration=TIMING["settlement_duration"])

    tx_details = {
        "TX Reference": gen_ref("IBK"),
        "Bank": bank_name.upper(),
        "Account": masked_acc,
        "Holder": holder_name,
        "TRN": trn_input,
        "Timestamp": f"{datestamp()} {ts()}",
    }
    show_result("interbank", tx_details)
    input(f"  {S.DM}Press ENTER to return to menu...{S.RST}")


# =====================================================================
# [ MODULE 3: IP-TO-IP TRANSFER ]
# =====================================================================
def module_ip_to_ip():
    """Direct IP-to-IP peer transfer protocol."""
    clear()
    print(LOGOS["ip2ip"])
    system_status_bar("IP-TO-IP TRANSFER")
    print(f"  {S.DM}{'─'*60}{S.RST}")
    print(f"  {S.TEAL}{S.BD}  DIRECT IP TRANSFER PROTOCOL{S.RST}")
    print(f"  {S.DM}  Peer-to-peer encrypted tunnel fund settlement{S.RST}")
    print(f"  {S.DM}{'─'*60}{S.RST}\n")

    # Token Auth
    tokens = MODULE_TOKENS["ip_to_ip"]
    print(f"  {S.C}[AUTH]{S.RST} Enter 5-character Access Token:")
    token_input = input(f"  {S.Y}▸ Token : {S.RST}").strip().upper()

    if token_input not in tokens:
        print(f"\n  {S.R}[✗] ACCESS DENIED — Invalid token.{S.RST}")
        input(f"\n  {S.DM}Press ENTER to return...{S.RST}")
        return

    user_data = tokens[token_input]
    print(f"\n  {S.G}[✓]{S.RST} Operator: {S.W}{S.BD}{user_data['operator']}{S.RST}")
    print(f"      Clearance: {S.TEAL}{user_data['clearance']}{S.RST} | Region: {S.W}{user_data['region']}{S.RST}")
    module_spinner("ip_to_ip", count=2)
    print()

    # Source/Dest IP Configuration
    print(f"  {S.W}{S.BD}  TUNNEL CONFIGURATION{S.RST}")
    sep(40)
    src_ip = input(f"  {S.Y}▸ Source IP Address      : {S.RST}").strip()
    src_port = input(f"  {S.Y}▸ Source Port            : {S.RST}").strip() or "8443"
    dst_ip = input(f"  {S.Y}▸ Destination IP Address : {S.RST}").strip()
    dst_port = input(f"  {S.Y}▸ Destination Port       : {S.RST}").strip() or "8443"
    
    if not src_ip: src_ip = f"192.168.{random.randint(1,254)}.{random.randint(1,254)}"
    if not dst_ip: dst_ip = f"10.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"

    print()
    spinner(f"Resolving {src_ip}:{src_port}", 1.5)
    spinner(f"Resolving {dst_ip}:{dst_port}", 1.5)
    spinner("Performing mutual TLS handshake", 2.0)
    spinner("Establishing encrypted P2P tunnel", 2.5)
    print()

    # Tunnel status
    tunnel_id = gen_session_id()[:12]
    print(f"  {S.G}{S.BD}  TUNNEL ESTABLISHED{S.RST}")
    print(f"    Tunnel ID  : {S.W}{tunnel_id}{S.RST}")
    print(f"    Route      : {S.TEAL}{src_ip}:{src_port}{S.RST} ──► {S.TEAL}{dst_ip}:{dst_port}{S.RST}")
    print(f"    Cipher     : {S.DM}ChaCha20-Poly1305{S.RST}")
    print(f"    Latency    : {S.DM}{random.randint(5,45)}ms{S.RST}")
    print()


    # Transfer Details
    print(f"  {S.W}{S.BD}  FUND TRANSFER{S.RST}")
    sep(40)
    sender_name = input(f"  {S.Y}▸ Sender Name        : {S.RST}").strip()
    sender_acc = input(f"  {S.Y}▸ Sender Account     : {S.RST}").strip()
    receiver_name = input(f"  {S.Y}▸ Receiver Name      : {S.RST}").strip()
    receiver_acc = input(f"  {S.Y}▸ Receiver Account   : {S.RST}").strip()
    currency = input(f"  {S.Y}▸ Currency [EUR/USD]  : {S.RST}").strip().upper() or "EUR"
    amount = input(f"  {S.Y}▸ Amount             : {S.RST}").strip()
    memo = input(f"  {S.Y}▸ Reference/Memo     : {S.RST}").strip() or "IP-TRANSFER"
    print()

    # Processing
    spinner("Encrypting payload (AES-256-CTR)", 2.0)
    spinner("Transmitting through secure tunnel", 3.0)
    progress("Data Transfer", duration=4.0, width=35, color=S.TEAL)
    module_spinner("ip_to_ip", count=2)
    print()

    # Settlement
    settlement_progress("ip_to_ip", duration=TIMING["settlement_duration"])

    tx_details = {
        "TX Reference": gen_ref("IP2"),
        "Tunnel ID": tunnel_id,
        "Source": f"{src_ip}:{src_port}",
        "Destination": f"{dst_ip}:{dst_port}",
        "Sender": sender_name,
        "Receiver": receiver_name,
        "Amount": f"{currency} {amount}",
        "Timestamp": f"{datestamp()} {ts()}",
    }
    show_result("ip_to_ip", tx_details)
    input(f"  {S.DM}Press ENTER to return to menu...{S.RST}")


# =====================================================================
# [ MODULE 4: SERVER-TO-SERVER (S2S) ]
# =====================================================================
def module_s2s():
    """Server-to-Server REST API settlement."""
    clear()
    print(LOGOS["s2s"])
    system_status_bar("SERVER-TO-SERVER")
    print(f"  {S.DM}{'─'*60}{S.RST}")
    print(f"  {S.PURPLE}{S.BD}  SERVER-TO-SERVER SETTLEMENT API{S.RST}")
    print(f"  {S.DM}  RESTful payment processing between merchant servers{S.RST}")
    print(f"  {S.DM}{'─'*60}{S.RST}\n")

    # Token Auth
    tokens = MODULE_TOKENS["s2s"]
    print(f"  {S.C}[AUTH]{S.RST} Enter 5-character API Token:")
    token_input = input(f"  {S.Y}▸ Token : {S.RST}").strip().upper()

    if token_input not in tokens:
        print(f"\n  {S.R}[✗] ACCESS DENIED — Invalid API token.{S.RST}")
        input(f"\n  {S.DM}Press ENTER to return...{S.RST}")
        return

    user_data = tokens[token_input]
    print(f"\n  {S.G}[✓]{S.RST} Engine: {S.W}{S.BD}{user_data['name']}{S.RST}")
    print(f"      Merchant: {S.W}{user_data['merchant']}{S.RST}")
    print(f"      API: {S.PURPLE}{user_data['api_version']}{S.RST} | Env: {S.G}{user_data['environment']}{S.RST}")
    module_spinner("s2s", count=2)
    print()

    # API Endpoint Config
    print(f"  {S.W}{S.BD}  API CONFIGURATION{S.RST}")
    sep(40)
    endpoint_url = input(f"  {S.Y}▸ Settlement Endpoint URL : {S.RST}").strip()
    if not endpoint_url:
        endpoint_url = f"https://api.payment-{random.randint(100,999)}.net/v3/settle"
    api_key = input(f"  {S.Y}▸ API Key (Bearer)       : {S.RST}").strip()
    if not api_key:
        api_key = f"sk_live_{''.join(random.choices(string.ascii_lowercase + string.digits, k=24))}"
    webhook_url = input(f"  {S.Y}▸ Webhook Callback URL   : {S.RST}").strip() or "N/A"

    print()
    spinner(f"Connecting to {endpoint_url[:40]}...", 2.0)
    spinner("Validating API key with OAuth 2.0 server", 1.5)
    spinner("Establishing server-to-server session", 2.0)
    print()

    print(f"  {S.G}{S.BD}  CONNECTION ESTABLISHED{S.RST}")
    print(f"    Endpoint : {S.W}{endpoint_url}{S.RST}")
    print(f"    Auth     : {S.DM}Bearer {api_key[:12]}...{S.RST}")
    print(f"    TLS      : {S.DM}TLS 1.3 / HTTP/2{S.RST}")
    print()


    # Payment Details
    print(f"  {S.W}{S.BD}  PAYMENT PAYLOAD{S.RST}")
    sep(40)
    merchant_id = input(f"  {S.Y}▸ Merchant ID         : {S.RST}").strip() or f"MID-{random.randint(100000,999999)}"
    customer_id = input(f"  {S.Y}▸ Customer Reference  : {S.RST}").strip() or f"CUS-{random.randint(10000,99999)}"
    ben_name = input(f"  {S.Y}▸ Beneficiary Name    : {S.RST}").strip()
    ben_account = input(f"  {S.Y}▸ Beneficiary Account : {S.RST}").strip()
    ben_bank = input(f"  {S.Y}▸ Beneficiary Bank    : {S.RST}").strip()
    currency = input(f"  {S.Y}▸ Currency            : {S.RST}").strip().upper() or "EUR"
    amount = input(f"  {S.Y}▸ Amount              : {S.RST}").strip()
    description = input(f"  {S.Y}▸ Description         : {S.RST}").strip() or "S2S Payment"

    print()
    # Simulate API call
    print(f"  {S.PURPLE}[API]{S.RST} POST {endpoint_url}")
    print(f"  {S.DM}  Content-Type: application/json{S.RST}")
    print(f"  {S.DM}  Authorization: Bearer {api_key[:12]}...{S.RST}")
    print(f"  {S.DM}  X-Idempotency-Key: {gen_session_id()}{S.RST}")
    print()

    spinner("Serializing JSON payload", 1.0)
    spinner("Sending POST request to settlement server", 2.5)
    module_spinner("s2s", count=2)
    print()

    # Show simulated response
    resp_code = "200 OK" if RESULT_CONFIG.get("s2s", "SUCCESS") == "SUCCESS" else "402 Payment Required"
    print(f"  {S.PURPLE}[RESPONSE]{S.RST} HTTP/{resp_code}")
    print(f"  {S.DM}  {{'status': 'processed', 'settlement_id': '{gen_ref('STL')}'}}{S.RST}")
    print()

    settlement_progress("s2s", duration=TIMING["settlement_duration"])

    tx_details = {
        "TX Reference": gen_ref("S2S"),
        "Merchant": merchant_id,
        "Customer": customer_id,
        "Beneficiary": ben_name,
        "Bank": ben_bank,
        "Amount": f"{currency} {amount}",
        "Endpoint": endpoint_url[:35] + "...",
        "Timestamp": f"{datestamp()} {ts()}",
    }
    show_result("s2s", tx_details)
    input(f"  {S.DM}Press ENTER to return to menu...{S.RST}")


# =====================================================================
# [ MODULE 5: SWIFT GPI ]
# =====================================================================
def module_gpi():
    """SWIFT GPI — Global Payment Innovation tracker."""
    clear()
    print(LOGOS["gpi"])
    system_status_bar("SWIFT GPI")
    print(f"  {S.DM}{'─'*60}{S.RST}")
    print(f"  {S.GOLD}{S.BD}  SWIFT GPI — GLOBAL PAYMENT INNOVATION{S.RST}")
    print(f"  {S.DM}  End-to-end payment tracking with UETR reference{S.RST}")
    print(f"  {S.DM}{'─'*60}{S.RST}\n")

    # Token Auth
    tokens = MODULE_TOKENS["gpi"]
    print(f"  {S.C}[AUTH]{S.RST} Enter 5-character GPI Token:")
    token_input = input(f"  {S.Y}▸ Token : {S.RST}").strip().upper()

    if token_input not in tokens:
        print(f"\n  {S.R}[✗] ACCESS DENIED — Invalid GPI token.{S.RST}")
        input(f"\n  {S.DM}Press ENTER to return...{S.RST}")
        return

    user_data = tokens[token_input]
    print(f"\n  {S.G}[✓]{S.RST} Institution: {S.W}{S.BD}{user_data['institution']}{S.RST}")
    print(f"      BIC: {S.GOLD}{user_data['bic']}{S.RST} | Member: {S.W}{user_data['gpi_member_id']}{S.RST}")
    module_spinner("gpi", count=2)
    print()

    # GPI Transaction Setup
    print(f"  {S.W}{S.BD}  GPI PAYMENT INITIATION{S.RST}")
    sep(50)
    
    uetr = gen_uetr()
    print(f"  {S.GOLD}[UETR]{S.RST} Generated: {S.W}{S.BD}{uetr}{S.RST}")
    print()

    ordering_inst = input(f"  {S.Y}▸ Ordering Institution (BIC)   : {S.RST}").strip().upper() or user_data['bic']
    ordering_name = input(f"  {S.Y}▸ Ordering Customer Name       : {S.RST}").strip()
    ordering_acc = input(f"  {S.Y}▸ Ordering Account              : {S.RST}").strip()
    ben_inst = input(f"  {S.Y}▸ Beneficiary Institution (BIC): {S.RST}").strip().upper() or "BNPAFRPPXXX"
    ben_name = input(f"  {S.Y}▸ Beneficiary Name              : {S.RST}").strip()
    ben_acc = input(f"  {S.Y}▸ Beneficiary Account (IBAN)    : {S.RST}").strip()
    currency = input(f"  {S.Y}▸ Currency                      : {S.RST}").strip().upper() or "EUR"
    amount = input(f"  {S.Y}▸ Amount                        : {S.RST}").strip()
    charge_bearer = input(f"  {S.Y}▸ Charge Bearer [SHA/OUR/BEN]  : {S.RST}").strip().upper() or "SHA"
    remit_info = input(f"  {S.Y}▸ Remittance Info               : {S.RST}").strip() or "PAYMENT"

    print()
    module_spinner("gpi", count=3)
    print()


    # GPI Tracking simulation
    print(f"  {S.GOLD}{S.BD}  GPI TRACKER STATUS{S.RST}")
    sep(50)
    
    gpi_hops = [
        (ordering_inst, "ACCEPTED", "Debited ordering customer"),
        ("SWIFT NETWORK", "IN TRANSIT", "Message validated and forwarded"),
        (ben_inst, "CREDITED", "Funds credited to beneficiary"),
    ]
    
    for inst, gpi_status, desc in gpi_hops:
        sys.stdout.write(f"  {S.GOLD}[GPI]{S.RST} {inst:<20} ")
        sys.stdout.flush()
        for _ in range(random.randint(8, 15)):
            sys.stdout.write(f"{S.GOLD}·{S.RST}")
            sys.stdout.flush()
            time.sleep(0.15)
        sc = S.G if gpi_status == "CREDITED" else S.Y
        print(f" {sc}[{gpi_status}]{S.RST}")
        print(f"       {S.DM}└─ {desc}{S.RST}")
        time.sleep(0.5)

    print()
    progress("GPI Settlement Confirmation", duration=5.0, width=35, color=S.GOLD)
    print()

    settlement_progress("gpi", duration=TIMING["settlement_duration"])

    tx_details = {
        "UETR": uetr,
        "Ordering BIC": ordering_inst,
        "Beneficiary BIC": ben_inst,
        "Beneficiary": ben_name,
        "Amount": f"{currency} {amount}",
        "Charge Bearer": charge_bearer,
        "GPI Status": "CREDITED" if RESULT_CONFIG.get("gpi") == "SUCCESS" else "REJECTED",
        "Timestamp": f"{datestamp()} {ts()}",
    }
    show_result("gpi", tx_details)
    input(f"  {S.DM}Press ENTER to return to menu...{S.RST}")


# =====================================================================
# [ MODULE 6: MT103 TRANSFER ]
# =====================================================================
def module_mt103():
    """SWIFT MT103 — Single Customer Credit Transfer message."""
    clear()
    print(LOGOS["mt103"])
    system_status_bar("SWIFT MT103")
    print(f"  {S.DM}{'─'*60}{S.RST}")
    print(f"  {S.B}{S.BD}  SWIFT MT103 — SINGLE CUSTOMER CREDIT TRANSFER{S.RST}")
    print(f"  {S.DM}  FIN message format for cross-border wire transfers{S.RST}")
    print(f"  {S.DM}{'─'*60}{S.RST}\n")

    # Token Auth
    tokens = MODULE_TOKENS["mt103"]
    print(f"  {S.C}[AUTH]{S.RST} Enter 5-character SWIFT Token:")
    token_input = input(f"  {S.Y}▸ Token : {S.RST}").strip().upper()

    if token_input not in tokens:
        print(f"\n  {S.R}[✗] ACCESS DENIED — Invalid SWIFT token.{S.RST}")
        input(f"\n  {S.DM}Press ENTER to return...{S.RST}")
        return

    user_data = tokens[token_input]
    print(f"\n  {S.G}[✓]{S.RST} Gateway: {S.W}{S.BD}{user_data['name']}{S.RST}")
    print(f"      Institution: {S.W}{user_data['institution']}{S.RST}")
    print(f"      BIC: {S.B}{user_data['bic']}{S.RST} | Branch: {S.W}{user_data['branch']}{S.RST}")
    module_spinner("mt103", count=2)
    print()

    # MT103 Message Fields
    print(f"  {S.W}{S.BD}  MT103 MESSAGE FIELDS{S.RST}")
    sep(50)
    print(f"  {S.DM}  Constructing SWIFT MT103 message block...{S.RST}\n")

    # Field 20: Transaction Reference
    txn_ref = input(f"  {S.Y}▸ :20: Transaction Ref Number : {S.RST}").strip() or gen_ref("FT")
    # Field 23B: Bank Operation Code
    bank_op = input(f"  {S.Y}▸ :23B: Bank Operation Code   : {S.RST}").strip().upper() or "CRED"
    # Field 32A: Value Date/Currency/Amount
    value_date = input(f"  {S.Y}▸ :32A: Value Date (YYMMDD)   : {S.RST}").strip() or datetime.datetime.now().strftime("%y%m%d")
    currency = input(f"  {S.Y}▸       Currency               : {S.RST}").strip().upper() or "EUR"
    amount = input(f"  {S.Y}▸       Amount                  : {S.RST}").strip() or "1000000"
    # Field 50K: Ordering Customer
    ord_name = input(f"  {S.Y}▸ :50K: Ordering Customer Name : {S.RST}").strip()
    ord_acc = input(f"  {S.Y}▸       Ordering Account        : {S.RST}").strip()
    ord_addr = input(f"  {S.Y}▸       Ordering Address        : {S.RST}").strip()
    # Field 52A: Ordering Institution
    ord_inst = input(f"  {S.Y}▸ :52A: Ordering Institution   : {S.RST}").strip().upper() or user_data['bic']
    # Field 53A: Sender Correspondent
    snd_corr = input(f"  {S.Y}▸ :53A: Sender Correspondent   : {S.RST}").strip().upper() or "CHASUS33XXX"
    # Field 57A: Account With Institution
    acc_inst = input(f"  {S.Y}▸ :57A: Account With Inst      : {S.RST}").strip().upper() or "BNPAFRPPXXX"
    # Field 59: Beneficiary
    ben_name = input(f"  {S.Y}▸ :59:  Beneficiary Name       : {S.RST}").strip()
    ben_acc = input(f"  {S.Y}▸       Beneficiary Account     : {S.RST}").strip()
    ben_addr = input(f"  {S.Y}▸       Beneficiary Address     : {S.RST}").strip()
    # Field 71A: Charges
    charges = input(f"  {S.Y}▸ :71A: Details of Charges      : {S.RST}").strip().upper() or "SHA"
    # Field 72: Sender to Receiver Info
    s2r_info = input(f"  {S.Y}▸ :72:  Sender-to-Receiver Info : {S.RST}").strip() or "/ACC/PAYMENT"

    print()


    # Display constructed MT103 message
    print(f"  {S.B}{S.BD}  CONSTRUCTED MT103 MESSAGE{S.RST}")
    sep(50)
    mt103_fields = [
        (":20:", txn_ref),
        (":23B:", bank_op),
        (":32A:", f"{value_date}{currency}{amount}"),
        (":50K:", f"/{ord_acc}\n         {ord_name}\n         {ord_addr}"),
        (":52A:", ord_inst),
        (":53A:", snd_corr),
        (":57A:", acc_inst),
        (":59:", f"/{ben_acc}\n         {ben_name}\n         {ben_addr}"),
        (":71A:", charges),
        (":72:", s2r_info),
    ]
    
    print(f"  {S.DM}  {{1:F01{ord_inst}0000000000}}{{2:I103{acc_inst}N}}{{4:{S.RST}")
    for field_tag, field_val in mt103_fields:
        first_line = field_val.split('\n')[0] if '\n' in field_val else field_val
        print(f"  {S.B}{field_tag}{S.RST}{S.W}{first_line}{S.RST}")
        if '\n' in field_val:
            for extra in field_val.split('\n')[1:]:
                print(f"  {S.W}{extra}{S.RST}")
    print(f"  {S.DM}  -}}{S.RST}")
    print()

    # Processing
    module_spinner("mt103", count=3)
    
    # Network trace
    print()
    trace_hops = [
        (1, f"{ord_inst[:8]}", "SENDER"),
        (2, "SWIFT-FIN-NET", "NETWORK"),
        (3, f"{snd_corr[:8]}", "CORR-BANK"),
        (4, f"{acc_inst[:8]}", "ACC-INST"),
    ]
    for num, node, ntype in trace_hops:
        trace_hop_animation(num, node, ntype, duration=random.uniform(0.8, 1.5))

    print()
    spinner("Confirming delivery and settlement", 2.0)
    print()

    settlement_progress("mt103", duration=TIMING["settlement_duration"])

    tx_details = {
        "MT103 Ref": txn_ref,
        "Value Date": value_date,
        "Currency/Amt": f"{currency} {amount}",
        "Ordering": f"{ord_name} ({ord_inst})",
        "Beneficiary": f"{ben_name} ({acc_inst})",
        "Charges": charges,
        "UETR": gen_uetr(),
        "Timestamp": f"{datestamp()} {ts()}",
    }
    show_result("mt103", tx_details)
    input(f"  {S.DM}Press ENTER to return to menu...{S.RST}")


# =====================================================================
# [ MODULE 7: RTGS SETTLEMENT ]
# =====================================================================
def module_rtgs():
    """Real-Time Gross Settlement System."""
    clear()
    print(LOGOS["rtgs"])
    system_status_bar("RTGS SETTLEMENT")
    print(f"  {S.DM}{'─'*60}{S.RST}")
    print(f"  {S.G}{S.BD}  RTGS — REAL-TIME GROSS SETTLEMENT{S.RST}")
    print(f"  {S.DM}  Central bank operated high-value payment system{S.RST}")
    print(f"  {S.DM}{'─'*60}{S.RST}\n")

    # Token Auth
    tokens = MODULE_TOKENS["rtgs"]
    print(f"  {S.C}[AUTH]{S.RST} Enter 5-character RTGS Token:")
    token_input = input(f"  {S.Y}▸ Token : {S.RST}").strip().upper()

    if token_input not in tokens:
        print(f"\n  {S.R}[✗] ACCESS DENIED — Invalid RTGS token.{S.RST}")
        input(f"\n  {S.DM}Press ENTER to return...{S.RST}")
        return

    user_data = tokens[token_input]
    print(f"\n  {S.G}[✓]{S.RST} System: {S.W}{S.BD}{user_data['name']}{S.RST}")
    print(f"      Operator: {S.W}{user_data['system']}{S.RST}")
    print(f"      Routing: {S.G}{user_data['routing']}{S.RST} | Node: {S.W}{user_data['node']}{S.RST}")
    module_spinner("rtgs", count=2)
    print()

    # RTGS System Selection
    print(f"  {S.W}{S.BD}  RTGS SYSTEM DETECTED{S.RST}")
    sep(40)
    systems = [
        "FEDWIRE (USA — Federal Reserve)",
        "TARGET2 (EU — European Central Bank)",
        "CHAPS (UK — Bank of England)",
        "BOJ-NET (Japan — Bank of Japan)",
        "RTGS (India — Reserve Bank of India)",
        "MEPS+ (Singapore — MAS)",
    ]
    for i, sys_name in enumerate(systems, 1):
        print(f"    {S.G}[{i}]{S.RST} {sys_name}")
    print()
    sys_choice = input(f"  {S.Y}▸ Select System [1-{len(systems)}] : {S.RST}").strip()
    try:
        selected_system = systems[int(sys_choice)-1] if sys_choice.isdigit() and 1 <= int(sys_choice) <= len(systems) else systems[0]
    except:
        selected_system = systems[0]

    print(f"\n  {S.G}[✓]{S.RST} System: {S.W}{selected_system}{S.RST}")
    spinner(f"Establishing link to {selected_system.split('(')[0].strip()}", 2.0)
    print()


    # RTGS Payment Details
    print(f"  {S.W}{S.BD}  RTGS PAYMENT INSTRUCTION{S.RST}")
    sep(50)
    
    sender_bank = input(f"  {S.Y}▸ Sending Bank (Name)        : {S.RST}").strip()
    sender_bic = input(f"  {S.Y}▸ Sending Bank BIC/Routing   : {S.RST}").strip().upper()
    sender_acc = input(f"  {S.Y}▸ Sender Account Number      : {S.RST}").strip()
    sender_name = input(f"  {S.Y}▸ Sender Name                : {S.RST}").strip()
    receiver_bank = input(f"  {S.Y}▸ Receiving Bank (Name)      : {S.RST}").strip()
    receiver_bic = input(f"  {S.Y}▸ Receiving Bank BIC/Routing : {S.RST}").strip().upper()
    receiver_acc = input(f"  {S.Y}▸ Receiver Account Number    : {S.RST}").strip()
    receiver_name = input(f"  {S.Y}▸ Receiver Name              : {S.RST}").strip()
    currency = input(f"  {S.Y}▸ Currency                   : {S.RST}").strip().upper() or "EUR"
    amount = input(f"  {S.Y}▸ Amount (min 1,000,000)     : {S.RST}").strip()
    purpose = input(f"  {S.Y}▸ Payment Purpose            : {S.RST}").strip() or "HIGH-VALUE SETTLEMENT"
    priority = input(f"  {S.Y}▸ Priority [URGENT/NORMAL]   : {S.RST}").strip().upper() or "URGENT"

    print()
    # RTGS Processing
    module_spinner("rtgs", count=3)
    
    # Queue simulation
    print()
    print(f"  {S.G}[RTGS]{S.RST} Payment entered into settlement queue:")
    print(f"         Priority: {S.G}{S.BD}{priority}{S.RST}")
    print(f"         Queue Position: {S.W}1 of 1{S.RST}")
    print()

    spinner("Processing gross settlement (irrevocable)", 3.0)
    module_spinner("rtgs", count=3)
    print()

    # Real-time confirmation
    progress("RTGS Finality Processing", duration=5.0, width=35, color=S.G)
    print()
    
    settlement_progress("rtgs", duration=TIMING["settlement_duration"])

    settlement_ref = f"RTGS-{datetime.datetime.now().strftime('%Y%m%d')}-{random.randint(100000,999999)}"
    tx_details = {
        "Settlement Ref": settlement_ref,
        "System": selected_system.split("(")[0].strip(),
        "Sender": f"{sender_name} ({sender_bic})",
        "Receiver": f"{receiver_name} ({receiver_bic})",
        "Amount": f"{currency} {amount}",
        "Priority": priority,
        "Finality": "IRREVOCABLE",
        "Timestamp": f"{datestamp()} {ts()}",
    }
    show_result("rtgs", tx_details)
    input(f"  {S.DM}Press ENTER to return to menu...{S.RST}")


# =====================================================================
# [ SETTINGS EDITOR LAUNCHER ]
# =====================================================================
def launch_settings_editor():
    """Launch the interactive configuration editor."""
    try:
        base = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        base = os.getcwd()
    editor_path = os.path.join(base, "config_editor.py")
    if not os.path.exists(editor_path):
        print(f"\n  {S.R}[ERROR]{S.RST} config_editor.py not found.")
        input(f"\n  {S.DM}Press ENTER to return...{S.RST}")
        return
    try:
        import subprocess
        subprocess.run([sys.executable, editor_path])
        # Reload config after editor changes
        load_config()
    except Exception as e:
        print(f"\n  {S.R}[ERROR]{S.RST} Failed to launch editor: {e}")
        input(f"\n  {S.DM}Press ENTER to return...{S.RST}")


# =====================================================================
# [ MAIN EXECUTION ]
# =====================================================================
def main():
    """Main execution flow."""
    S.init()

    # Set terminal title
    if os.name == 'nt':
        os.system('title GLOBAL PAYMENT SETTLEMENT ENGINE')
    else:
        sys.stdout.write('\033]0;GLOBAL PAYMENT SETTLEMENT ENGINE\007')
        sys.stdout.flush()

    # Boot
    phase_boot()

    # Main loop
    while True:
        choice = main_menu()

        if choice == "0":
            clear()
            print(f"\n  {S.R}[SYSTEM]{S.RST} Terminating secure session...")
            spinner("Purging volatile memory", 1.5)
            spinner("Closing encrypted tunnels", 1.0)
            print(f"\n  {S.DM}  Session terminated. No trace remains.{S.RST}\n")
            sys.exit(0)
        elif choice == "1":
            module_protocol_transaction()
        elif choice == "2":
            module_interbank()
        elif choice == "3":
            module_ip_to_ip()
        elif choice == "4":
            module_s2s()
        elif choice == "5":
            module_gpi()
        elif choice == "6":
            module_mt103()
        elif choice == "7":
            module_rtgs()
        elif choice == "8":
            launch_settings_editor()
        else:
            print(f"\n  {S.R}[!] Invalid selection.{S.RST}")
            time.sleep(1)


# =====================================================================
# [ ENTRY POINT ]
# =====================================================================
if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg in ("-h", "--help"):
            print(f"GLOBAL PAYMENT SETTLEMENT ENGINE v{VERSION}")
            print(f"Usage: python engine.py")
            print(f"\nModules: Protocol TX | Interbank | IP-to-IP | S2S | GPI | MT103 | RTGS")
            print(f"\nAccess tokens are required per module.")
            sys.exit(0)
        elif arg in ("-v", "--version"):
            print(f"GPSE v{VERSION} (Build {BUILD})")
            sys.exit(0)

    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {S.R}[!] Session forcibly terminated.{S.RST}")
        print(f"  {S.DM}Volatile memory purged. No trace remains.{S.RST}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n  {S.R}[FATAL] System error: {e}{S.RST}")
        print(f"  {S.DM}Core dump saved. Restart required.{S.RST}\n")
        sys.exit(1)
