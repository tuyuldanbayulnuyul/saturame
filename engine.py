#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GLOBAL PAYMENT SETTLEMENT ENGINE v5.0
Build 2026.05.26 | Multi-Protocol Financial Terminal
[ SIMULATION / DEMONSTRATION TOOL ONLY ]

Web-based GUI running on localhost:8080 using Python http.server.
All HTML/CSS/JS is embedded as Python string constants.
LOADING_DURATION controls all animation timing (auto-distributed).
"""

import os
import sys
import json
import hashlib
import datetime
import string
import random
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

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
    "interbank": "Validator quorum unreachable - TX voided",
    "ip_to_ip": "",
    "s2s": "",
    "gpi": "",
    "mt103": "",
    "rtgs": "",
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
# [ CONFIG LOAD ]
# =====================================================================
def load_config():
    """Load configuration from config.json. Falls back to defaults if missing."""
    global MODULE_TOKENS, RESULT_CONFIG, RESULT_MESSAGE, BIN_DATABASE
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
        BIN_DATABASE = config.get("BIN_DATABASE", _DEFAULT_BIN_DATABASE)
        LOADING_MESSAGES = config.get("LOADING_MESSAGES", _DEFAULT_LOADING_MESSAGES)
        LOADING_DURATION = config.get("LOADING_DURATION", _DEFAULT_LOADING_DURATION)
    else:
        MODULE_TOKENS = _DEFAULT_MODULE_TOKENS
        RESULT_CONFIG = _DEFAULT_RESULT_CONFIG
        RESULT_MESSAGE = _DEFAULT_RESULT_MESSAGE
        BIN_DATABASE = _DEFAULT_BIN_DATABASE
        LOADING_MESSAGES = _DEFAULT_LOADING_MESSAGES
        LOADING_DURATION = _DEFAULT_LOADING_DURATION


# Load configuration at module level
load_config()


# =====================================================================
# [ BUSINESS LOGIC - BIN DETECTION ]
# =====================================================================
def detect_card_brand(card_number):
    """Auto-detect card brand from BIN (first digits)."""
    if not card_number or len(card_number) < 2:
        return "UNKNOWN", "UNKNOWN"
    prefix2 = card_number[:2]
    if prefix2 in BIN_DATABASE:
        brand = BIN_DATABASE[prefix2]
        network = "VISA" if brand.startswith("VISA") else \
                  "MASTERCARD" if brand.startswith("MASTERCARD") else \
                  brand.split()[0]
        return network, brand
    prefix1 = card_number[:1]
    if prefix1 in BIN_DATABASE:
        brand = BIN_DATABASE[prefix1]
        network = brand.split()[0]
        return network, brand
    return "UNKNOWN", "UNKNOWN"


# =====================================================================
# [ UTILITY FUNCTIONS ]
# =====================================================================
def ts():
    return datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]

def datestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def gen_ref(prefix="TRN"):
    return f"{prefix}-{random.randint(10000,99999)}-{random.choice(string.ascii_uppercase)}{random.randint(10,99)}{random.choice(string.ascii_uppercase)}"

def gen_uetr():
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
    import time as _time
    seed = f"{_time.time()}{random.randint(0,99999)}"
    return hashlib.sha256(seed.encode()).hexdigest()[:20].upper()

def gen_tx_hash():
    import time as _time
    return "0x" + hashlib.sha256(f"{_time.time()}{random.random()}".encode()).hexdigest()[:64]


# =====================================================================
# [ STATIC DATA ]
# =====================================================================
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

CURRENCIES = ["EUR", "USD", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", "SGD", "IDR"]

ACCOUNT_HOLDER_MAP = {
    "1640004347177": "HARVIANSYAH KURNIAWAN",
    "1100004416787": "PT.RAJAWALI NUSINDO",
}

RTGS_SYSTEMS = [
    "FEDWIRE (USA - Federal Reserve)",
    "TARGET2 (EU - European Central Bank)",
    "CHAPS (UK - Bank of England)",
    "BOJ-NET (Japan - Bank of Japan)",
    "RTGS (India - Reserve Bank of India)",
    "MEPS+ (Singapore - MAS)",
]



# =====================================================================
# [ HTML TEMPLATES - CSS STYLES ]
# =====================================================================
CSS_STYLES = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    background: #0d1117;
    color: #c9d1d9;
    font-family: 'Courier New', 'Consolas', monospace;
    min-height: 100vh;
    line-height: 1.6;
}
.container { max-width: 900px; margin: 0 auto; padding: 20px; }
.header {
    text-align: center;
    padding: 30px 0;
    border-bottom: 1px solid #21262d;
    margin-bottom: 30px;
}
.header pre {
    color: #58a6ff;
    font-size: 10px;
    line-height: 1.2;
    display: inline-block;
    text-align: left;
}
.header .version {
    color: #8b949e;
    font-size: 12px;
    margin-top: 10px;
}
.status-bar {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 6px;
    padding: 12px 20px;
    margin-bottom: 24px;
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 10px;
}
.status-bar span { color: #58a6ff; font-size: 13px; }
.status-bar .val { color: #3fb950; }
.modules-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
    gap: 16px;
    margin-bottom: 30px;
}
.module-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 20px;
    cursor: pointer;
    transition: all 0.2s;
    text-decoration: none;
    display: block;
}
.module-card:hover {
    border-color: #58a6ff;
    background: #1c2128;
    transform: translateY(-2px);
}
.module-card .num {
    display: inline-block;
    width: 28px; height: 28px;
    background: #21262d;
    border-radius: 4px;
    text-align: center;
    line-height: 28px;
    font-weight: bold;
    margin-right: 10px;
}
.module-card .name { color: #f0f6fc; font-weight: bold; font-size: 15px; }
.module-card .desc { color: #8b949e; font-size: 12px; margin-top: 6px; }
.module-card.proto .num { color: #f0883e; border: 1px solid #f0883e; }
.module-card.interbank .num { color: #58a6ff; border: 1px solid #58a6ff; }
.module-card.ip2ip .num { color: #3fb950; border: 1px solid #3fb950; }
.module-card.s2s .num { color: #a371f7; border: 1px solid #a371f7; }
.module-card.gpi .num { color: #d29922; border: 1px solid #d29922; }
.module-card.mt103 .num { color: #58a6ff; border: 1px solid #58a6ff; }
.module-card.rtgs .num { color: #3fb950; border: 1px solid #3fb950; }
.module-card.settings .num { color: #8b949e; border: 1px solid #8b949e; }
.settings-link {
    text-align: center;
    margin-top: 20px;
    padding: 15px;
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 8px;
}
.settings-link a { color: #58a6ff; text-decoration: none; }
.settings-link a:hover { text-decoration: underline; }

/* Form styles */
.form-page {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 30px;
    margin: 20px 0;
}
.form-page h2 {
    color: #58a6ff;
    margin-bottom: 20px;
    font-size: 18px;
    border-bottom: 1px solid #21262d;
    padding-bottom: 10px;
}
.form-page h3 {
    color: #c9d1d9;
    margin: 15px 0 10px 0;
    font-size: 14px;
}
.form-group {
    margin-bottom: 16px;
}
.form-group label {
    display: block;
    color: #8b949e;
    font-size: 12px;
    margin-bottom: 4px;
}
.form-group input, .form-group select {
    width: 100%;
    padding: 10px 14px;
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 4px;
    color: #c9d1d9;
    font-family: 'Courier New', monospace;
    font-size: 14px;
}
.form-group input:focus, .form-group select:focus {
    outline: none;
    border-color: #58a6ff;
}
.btn {
    display: inline-block;
    padding: 10px 24px;
    background: #238636;
    color: #fff;
    border: none;
    border-radius: 6px;
    font-family: 'Courier New', monospace;
    font-size: 14px;
    cursor: pointer;
    transition: background 0.2s;
    text-decoration: none;
}
.btn:hover { background: #2ea043; }
.btn-secondary { background: #21262d; color: #c9d1d9; }
.btn-secondary:hover { background: #30363d; }
.btn-danger { background: #da3633; }
.btn-danger:hover { background: #f85149; }

/* Processing animation */
.processing-container {
    text-align: center;
    padding: 40px 20px;
}
.spinner {
    width: 50px; height: 50px;
    border: 3px solid #21262d;
    border-top: 3px solid #58a6ff;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 20px auto;
}
@keyframes spin { to { transform: rotate(360deg); } }
.progress-bar-container {
    width: 100%;
    max-width: 500px;
    margin: 20px auto;
    background: #21262d;
    border-radius: 4px;
    height: 24px;
    overflow: hidden;
    position: relative;
}
.progress-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #238636, #3fb950);
    border-radius: 4px;
    width: 0%;
    transition: width 0.3s linear;
}
.progress-bar-fill.failed {
    background: linear-gradient(90deg, #da3633, #f85149);
}
.progress-bar-fill.pending {
    background: linear-gradient(90deg, #9e6a03, #d29922);
}
.progress-pct {
    position: absolute;
    right: 10px;
    top: 0;
    line-height: 24px;
    font-size: 12px;
    color: #fff;
    font-weight: bold;
}
.loading-message {
    color: #58a6ff;
    font-size: 13px;
    margin-top: 15px;
    min-height: 20px;
}

/* Result styles */
.result-box {
    border-radius: 8px;
    padding: 24px;
    margin: 20px 0;
    border: 2px solid;
}
.result-box.success { border-color: #3fb950; background: #0d1117; }
.result-box.success .result-title { color: #3fb950; }
.result-box.failed { border-color: #f85149; background: #0d1117; }
.result-box.failed .result-title { color: #f85149; }
.result-box.pending { border-color: #d29922; background: #0d1117; }
.result-box.pending .result-title { color: #d29922; }
.result-title {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 16px;
    text-align: center;
}
.result-details { margin-top: 12px; }
.result-details .row {
    display: flex;
    padding: 6px 0;
    border-bottom: 1px solid #21262d;
}
.result-details .row .key { color: #8b949e; width: 180px; flex-shrink: 0; }
.result-details .row .value { color: #c9d1d9; }
.back-link {
    display: inline-block;
    margin-top: 20px;
    color: #58a6ff;
    text-decoration: none;
}
.back-link:hover { text-decoration: underline; }
.customer-box {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 16px;
    margin: 15px 0;
}
.customer-box h4 { color: #58a6ff; margin-bottom: 10px; font-size: 13px; }
.customer-box .row { display: flex; padding: 3px 0; font-size: 13px; }
.customer-box .row .key { color: #8b949e; width: 140px; }
.customer-box .row .value { color: #f0f6fc; }
.bin-info {
    background: #0d1117;
    border: 1px solid #3fb950;
    border-radius: 6px;
    padding: 12px 16px;
    margin: 10px 0;
    font-size: 13px;
}
.bin-info .network { color: #3fb950; font-weight: bold; }
.error-msg { color: #f85149; margin: 10px 0; font-size: 13px; }
.hidden { display: none; }
.step-indicator {
    display: flex;
    gap: 8px;
    margin-bottom: 20px;
    flex-wrap: wrap;
}
.step-indicator .step {
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 11px;
    background: #21262d;
    color: #8b949e;
}
.step-indicator .step.active { background: #58a6ff; color: #fff; }
.step-indicator .step.done { background: #238636; color: #fff; }
"""



# =====================================================================
# [ HTML TEMPLATES - MAIN PAGE ]
# =====================================================================
MAIN_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GPSE - Global Payment Settlement Engine</title>
<style>{css}</style>
</head>
<body>
<div class="container">
    <div class="header">
        <pre>
 ██████╗ ██████╗ ███████╗███████╗    ███████╗███╗   ██╗ ██████╗
██╔════╝ ██╔══██╗██╔════╝██╔════╝    ██╔════╝████╗  ██║██╔════╝
██║  ███╗██████╔╝███████╗█████╗      █████╗  ██╔██╗ ██║██║  ███╗
██║   ██║██╔═══╝ ╚════██║██╔══╝      ██╔══╝  ██║╚██╗██║██║   ██║
╚██████╔╝██║     ███████║███████╗    ███████╗██║ ╚████║╚██████╔╝
 ╚═════╝ ╚═╝     ╚══════╝╚══════╝    ╚══════╝╚═╝  ╚═══╝ ╚═════╝
        GLOBAL PAYMENT SETTLEMENT ENGINE v{version}
        </pre>
        <div class="version">Build {build} | Multi-Protocol Financial Terminal | SIMULATION ONLY</div>
    </div>

    <div class="status-bar">
        <span>VERSION: <span class="val">{version}</span></span>
        <span>BUILD: <span class="val">{build}</span></span>
        <span>MODULES: <span class="val">7</span></span>
        <span>STATUS: <span class="val">OPERATIONAL</span></span>
    </div>

    <div class="modules-grid">
        <a href="/module/protocol_transaction" class="module-card proto">
            <span class="num">1</span>
            <span class="name">Protocol Transaction</span>
            <div class="desc">Card-based multi-protocol settlement (Visa/MC auto-detect)</div>
        </a>
        <a href="/module/interbank" class="module-card interbank">
            <span class="num">2</span>
            <span class="name">Interbank Transfer</span>
            <div class="desc">SWIFT Network interbank fund settlement engine</div>
        </a>
        <a href="/module/ip_to_ip" class="module-card ip2ip">
            <span class="num">3</span>
            <span class="name">IP-to-IP Transfer</span>
            <div class="desc">Direct peer-to-peer IP tunnel fund transfer</div>
        </a>
        <a href="/module/s2s" class="module-card s2s">
            <span class="num">4</span>
            <span class="name">Server-to-Server (S2S)</span>
            <div class="desc">REST API settlement between payment servers</div>
        </a>
        <a href="/module/gpi" class="module-card gpi">
            <span class="num">5</span>
            <span class="name">SWIFT GPI</span>
            <div class="desc">Global Payment Innovation real-time tracker</div>
        </a>
        <a href="/module/mt103" class="module-card mt103">
            <span class="num">6</span>
            <span class="name">MT103 Transfer</span>
            <div class="desc">SWIFT MT103 single customer credit transfer</div>
        </a>
        <a href="/module/rtgs" class="module-card rtgs">
            <span class="num">7</span>
            <span class="name">RTGS Settlement</span>
            <div class="desc">Real-Time Gross Settlement System</div>
        </a>
    </div>

    <div class="settings-link">
        <a href="http://localhost:8585" target="_blank">Settings Editor (Port 8585)</a>
        <span style="color:#8b949e;"> | Configure tokens, timing, and messages</span>
    </div>
</div>
</body>
</html>"""



# =====================================================================
# [ HTML TEMPLATES - MODULE PAGE ]
# =====================================================================
MODULE_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GPSE - {module_title}</title>
<style>{css}</style>
</head>
<body>
<div class="container">
    <div class="header" style="padding:15px 0;">
        <div style="color:#58a6ff;font-size:16px;font-weight:bold;">{module_title}</div>
        <div class="version">{module_desc}</div>
    </div>

    <div class="step-indicator" id="stepIndicator">
        <span class="step active" id="step1">1. Authentication</span>
        <span class="step" id="step2">2. Data Input</span>
        <span class="step" id="step3">3. Processing</span>
        <span class="step" id="step4">4. Result</span>
    </div>

    <!-- Step 1: Auth -->
    <div class="form-page" id="authSection">
        <h2>Authentication</h2>
        <div id="authForm">
            {auth_form_html}
        </div>
        <div class="error-msg hidden" id="authError"></div>
    </div>

    <!-- Step 2: Data Input -->
    <div class="form-page hidden" id="dataSection">
        <h2>Transaction Data</h2>
        <div id="customerInfo"></div>
        <div id="dataForm">
            {data_form_html}
        </div>
    </div>

    <!-- Step 3: Processing -->
    <div class="form-page hidden" id="processSection">
        <div class="processing-container">
            <div class="spinner"></div>
            <div class="loading-message" id="loadingMsg">Initializing...</div>
            <div class="progress-bar-container">
                <div class="progress-bar-fill" id="progressBar"></div>
                <span class="progress-pct" id="progressPct">0%</span>
            </div>
        </div>
    </div>

    <!-- Step 4: Result -->
    <div class="form-page hidden" id="resultSection">
        <div id="resultContent"></div>
    </div>

    <a href="/" class="back-link">&#8592; Back to Main Menu</a>
</div>

<script>
var MODULE_KEY = "{module_key}";
var LOADING_DURATION = {loading_duration};
var LOADING_MESSAGES = {loading_messages_json};
var AUTH_DATA = null;

{module_js}
</script>
</body>
</html>"""



# =====================================================================
# [ JAVASCRIPT FOR MODULE PAGES ]
# =====================================================================
BASE_MODULE_JS = """
function setStep(n) {
    for (var i = 1; i <= 4; i++) {
        var el = document.getElementById('step' + i);
        el.className = 'step' + (i < n ? ' done' : (i === n ? ' active' : ''));
    }
}

function showSection(id) {
    ['authSection','dataSection','processSection','resultSection'].forEach(function(s){
        document.getElementById(s).classList.add('hidden');
    });
    document.getElementById(id).classList.remove('hidden');
}

function submitAuth() {
    var body = getAuthBody();
    if (!body) return;
    fetch('/api/auth', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(body)
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
        if (data.success) {
            AUTH_DATA = data;
            document.getElementById('authError').classList.add('hidden');
            setStep(2);
            showSection('dataSection');
            onAuthSuccess(data);
        } else {
            var err = document.getElementById('authError');
            err.textContent = data.error || 'Authentication failed';
            err.classList.remove('hidden');
        }
    })
    .catch(function(e) {
        var err = document.getElementById('authError');
        err.textContent = 'Connection error';
        err.classList.remove('hidden');
    });
}

function submitData() {
    var body = getDataBody();
    if (!body) return;
    setStep(3);
    showSection('processSection');
    startProcessing(body);
}

function startProcessing(body) {
    var messages = LOADING_MESSAGES;
    var duration = LOADING_DURATION * 1000;
    var perMsg = duration / messages.length;
    var bar = document.getElementById('progressBar');
    var pct = document.getElementById('progressPct');
    var msgEl = document.getElementById('loadingMsg');
    var startTime = Date.now();
    var msgIdx = 0;

    function updateMsg() {
        if (msgIdx < messages.length) {
            msgEl.textContent = messages[msgIdx];
            msgIdx++;
        }
    }
    updateMsg();
    var msgInterval = setInterval(updateMsg, perMsg);

    var progressInterval = setInterval(function() {
        var elapsed = Date.now() - startTime;
        var progress = Math.min((elapsed / duration) * 100, 100);
        bar.style.width = progress + '%';
        pct.textContent = Math.round(progress) + '%';
        if (progress >= 100) {
            clearInterval(progressInterval);
            clearInterval(msgInterval);
            msgEl.textContent = 'Finalizing settlement...';
            setTimeout(function() { doProcess(body); }, 500);
        }
    }, 100);
}

function doProcess(body) {
    body.module = MODULE_KEY;
    fetch('/api/process', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(body)
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
        setStep(4);
        showSection('resultSection');
        showResult(data);
    })
    .catch(function(e) {
        setStep(4);
        showSection('resultSection');
        document.getElementById('resultContent').innerHTML =
            '<div class="result-box failed"><div class="result-title">CONNECTION ERROR</div></div>';
    });
}

function showResult(data) {
    var cls = (data.result || 'failed').toLowerCase();
    var title = 'SETTLEMENT ' + (data.result || 'FAILED').toUpperCase();
    var bar = document.getElementById('progressBar');
    if (cls === 'failed') bar.className = 'progress-bar-fill failed';
    else if (cls === 'pending') bar.className = 'progress-bar-fill pending';

    var html = '<div class="result-box ' + cls + '">';
    html += '<div class="result-title">' + title + '</div>';
    if (data.message) {
        html += '<div style="text-align:center;color:#8b949e;margin-bottom:16px;">' + data.message + '</div>';
    }
    html += '<div class="result-details">';
    if (data.details) {
        for (var key in data.details) {
            html += '<div class="row"><span class="key">' + key + '</span><span class="value">' + data.details[key] + '</span></div>';
        }
    }
    html += '</div></div>';
    document.getElementById('resultContent').innerHTML = html;
}
"""



# =====================================================================
# [ PER-MODULE AUTH FORMS AND JS ]
# =====================================================================
PROTOCOL_AUTH_FORM = """
<div class="form-group">
    <label>5-Character Access Token</label>
    <input type="text" id="tokenInput" maxlength="5" placeholder="Enter token (e.g., 83GIM)"
           style="text-transform:uppercase;">
</div>
<button class="btn" onclick="submitAuth()">Authenticate</button>
"""

PROTOCOL_DATA_FORM = """
<div id="protoStep1">
    <h3>Protocol Selection</h3>
    <div class="form-group">
        <label>Transaction Protocol</label>
        <select id="protoSelect">{proto_options}</select>
    </div>
    <h3>Card Details</h3>
    <div class="form-group">
        <label>Card Number (16 digits)</label>
        <input type="text" id="cardNumber" maxlength="19" placeholder="4500 1234 5678 9012"
               oninput="checkBin(this.value)">
    </div>
    <div id="binInfo" class="bin-info hidden"></div>
    <div class="form-group">
        <label>Expiry Date (MM/YY)</label>
        <input type="text" id="expiry" maxlength="5" placeholder="12/25"
               oninput="formatExpiry(this)">
    </div>
    <h3>Transfer Type</h3>
    <div class="form-group">
        <label>Type</label>
        <select id="transferType" onchange="showTransferFields()">
            <option value="bank">Bank Transfer</option>
            <option value="crypto">Crypto Transfer (USDT)</option>
        </select>
    </div>
    <div id="bankFields">
        <div class="form-group"><label>Destination Bank</label><input type="text" id="destBank"></div>
        <div class="form-group"><label>Beneficiary Name</label><input type="text" id="benName"></div>
        <div class="form-group"><label>Account Number</label><input type="text" id="accNum"></div>
        <div class="form-group"><label>SWIFT/BIC Code</label><input type="text" id="swiftCode"></div>
        <div class="form-group"><label>Currency</label>
            <select id="currency">{currency_options}</select>
        </div>
        <div class="form-group"><label>Amount</label><input type="text" id="amount" placeholder="1000000"></div>
    </div>
    <div id="cryptoFields" class="hidden">
        <div class="form-group"><label>Network</label>
            <select id="cryptoNet">{usdt_options}</select>
        </div>
        <div class="form-group"><label>Receiver Wallet</label><input type="text" id="recWallet"></div>
        <div class="form-group"><label>Sender Wallet</label><input type="text" id="sndWallet"></div>
        <div class="form-group"><label>Amount (EUR)</label><input type="text" id="cryptoAmount"></div>
    </div>
    <h3>Authorization</h3>
    <div class="form-group">
        <label id="authCodeLabel">Authorization Code (6 digits)</label>
        <input type="text" id="authCode" maxlength="6" placeholder="123456">
    </div>
    <div class="error-msg hidden" id="dataError"></div>
    <button class="btn" onclick="submitData()">Process Transaction</button>
</div>
"""

PROTOCOL_JS = """
function getAuthBody() {
    var token = document.getElementById('tokenInput').value.trim().toUpperCase();
    if (!token) return null;
    return {module: MODULE_KEY, token: token};
}

function onAuthSuccess(data) {
    if (data.user_data) {
        var html = '<div class="customer-box"><h4>CUSTOMER DATA</h4>';
        var fields = data.user_data;
        for (var k in fields) {
            if (k !== 'allowed_card_last4' && k !== 'name') {
                html += '<div class="row"><span class="key">' + k + '</span><span class="value">' + (fields[k]||'N/A') + '</span></div>';
            }
        }
        html += '</div>';
        document.getElementById('customerInfo').innerHTML = html;
    }
    // Update auth code digits based on protocol
    updateAuthCodeLabel();
}

function updateAuthCodeLabel() {
    var sel = document.getElementById('protoSelect');
    var proto = sel ? sel.value : '';
    var digits = (proto.indexOf('6 DG') !== -1) ? 6 : 4;
    var label = document.getElementById('authCodeLabel');
    var input = document.getElementById('authCode');
    label.textContent = 'Authorization Code (' + digits + ' digits)';
    input.maxLength = digits;
    input.placeholder = digits === 6 ? '123456' : '1234';
}

function checkBin(val) {
    val = val.replace(/[^0-9]/g, '');
    if (val.length >= 2) {
        fetch('/api/bin/' + val.substring(0, 6))
        .then(function(r){return r.json();})
        .then(function(d){
            var el = document.getElementById('binInfo');
            if (d.network && d.network !== 'UNKNOWN') {
                el.innerHTML = '<span class="network">' + d.network + '</span> - ' + d.brand + ' | Card: **** **** **** ' + val.slice(-4);
                el.classList.remove('hidden');
            } else if (val.length >= 6) {
                el.innerHTML = 'Network: UNKNOWN';
                el.classList.remove('hidden');
            }
        });
    }
}

function formatExpiry(el) {
    var val = el.value.replace(/[^0-9]/g, '');
    if (val.length >= 2) {
        el.value = val.substring(0,2) + '/' + val.substring(2,4);
    } else {
        el.value = val;
    }
}

function showTransferFields() {
    var type = document.getElementById('transferType').value;
    document.getElementById('bankFields').classList.toggle('hidden', type !== 'bank');
    document.getElementById('cryptoFields').classList.toggle('hidden', type !== 'crypto');
}

function getDataBody() {
    var card = document.getElementById('cardNumber').value.replace(/[^0-9]/g, '');
    if (card.length !== 16) {
        showDataError('Card number must be 16 digits');
        return null;
    }
    var proto = document.getElementById('protoSelect').value;
    var digits = (proto.indexOf('6 DG') !== -1) ? 6 : 4;
    var authCode = document.getElementById('authCode').value.trim();
    if (authCode.length !== digits || !/^[0-9]+$/.test(authCode)) {
        showDataError('Auth code must be ' + digits + ' digits');
        return null;
    }
    var expiry = document.getElementById('expiry').value;
    var type = document.getElementById('transferType').value;
    var body = {
        card_number: card,
        protocol: proto,
        expiry: expiry,
        auth_code: authCode,
        transfer_type: type,
        token: document.getElementById('tokenInput').value.trim().toUpperCase()
    };
    if (type === 'bank') {
        body.dest_bank = document.getElementById('destBank').value;
        body.ben_name = document.getElementById('benName').value;
        body.acc_num = document.getElementById('accNum').value;
        body.swift_code = document.getElementById('swiftCode').value;
        body.currency = document.getElementById('currency').value;
        body.amount = document.getElementById('amount').value;
    } else {
        body.crypto_network = document.getElementById('cryptoNet').value;
        body.rec_wallet = document.getElementById('recWallet').value;
        body.snd_wallet = document.getElementById('sndWallet').value;
        body.amount = document.getElementById('cryptoAmount').value;
        body.currency = 'EUR';
    }
    hideDataError();
    return body;
}

function showDataError(msg) {
    var el = document.getElementById('dataError');
    el.textContent = msg; el.classList.remove('hidden');
}
function hideDataError() {
    document.getElementById('dataError').classList.add('hidden');
}

document.getElementById('protoSelect').addEventListener('change', updateAuthCodeLabel);
"""



# =====================================================================
# [ INTERBANK MODULE FORMS AND JS ]
# =====================================================================
INTERBANK_AUTH_FORM = """
<div class="form-group">
    <label>Operator ID (Username)</label>
    <input type="text" id="usernameInput" placeholder="Enter username">
</div>
<div class="form-group">
    <label>Access Key (Password)</label>
    <input type="password" id="passwordInput" placeholder="Enter password">
</div>
<button class="btn" onclick="submitAuth()">Login</button>
"""

INTERBANK_DATA_FORM = """
<div class="form-group"><label>Target TRN Signature</label>
    <input type="text" id="trnInput" placeholder="7743127735841025"></div>
<h3>Destination Bank Configuration</h3>
<div class="form-group"><label>Destination Bank</label>
    <input type="text" id="destBank" placeholder="Bank name (alphabets only)"></div>
<div class="form-group"><label>Account Number</label>
    <input type="text" id="accountNo" placeholder="Account number (numbers only)"></div>
<div class="form-group"><label>SWIFT Code</label>
    <input type="text" id="swiftCode" placeholder="XXXXXXXXXXX"></div>
<div class="error-msg hidden" id="dataError"></div>
<button class="btn" onclick="submitData()">Initiate Settlement</button>
"""

INTERBANK_JS = """
function getAuthBody() {
    var user = document.getElementById('usernameInput').value.trim();
    var pass = document.getElementById('passwordInput').value;
    if (!user || !pass) return null;
    return {module: MODULE_KEY, username: user, password: pass};
}

function onAuthSuccess(data) {}

function getDataBody() {
    var bank = document.getElementById('destBank').value.trim();
    var acc = document.getElementById('accountNo').value.trim();
    if (!bank) { showDataError('Bank name required'); return null; }
    if (!acc || !/^[0-9]+$/.test(acc)) { showDataError('Account number required (numbers only)'); return null; }
    hideDataError();
    return {
        trn: document.getElementById('trnInput').value.trim() || '7743127735841025',
        dest_bank: bank,
        account_no: acc,
        swift_code: document.getElementById('swiftCode').value.trim() || 'XXXXXXXXXXX'
    };
}
function showDataError(msg) { var el=document.getElementById('dataError'); el.textContent=msg; el.classList.remove('hidden'); }
function hideDataError() { document.getElementById('dataError').classList.add('hidden'); }
"""



# =====================================================================
# [ IP-TO-IP MODULE FORMS AND JS ]
# =====================================================================
IP2IP_AUTH_FORM = """
<div class="form-group">
    <label>5-Character Access Token</label>
    <input type="text" id="tokenInput" maxlength="5" placeholder="Enter token"
           style="text-transform:uppercase;">
</div>
<button class="btn" onclick="submitAuth()">Authenticate</button>
"""

IP2IP_DATA_FORM = """
<h3>Tunnel Configuration</h3>
<div class="form-group"><label>Source IP Address</label><input type="text" id="srcIp" placeholder="192.168.1.100"></div>
<div class="form-group"><label>Source Port</label><input type="text" id="srcPort" value="8443"></div>
<div class="form-group"><label>Destination IP Address</label><input type="text" id="dstIp" placeholder="10.0.0.50"></div>
<div class="form-group"><label>Destination Port</label><input type="text" id="dstPort" value="8443"></div>
<h3>Fund Transfer</h3>
<div class="form-group"><label>Sender Name</label><input type="text" id="senderName"></div>
<div class="form-group"><label>Sender Account</label><input type="text" id="senderAcc"></div>
<div class="form-group"><label>Receiver Name</label><input type="text" id="receiverName"></div>
<div class="form-group"><label>Receiver Account</label><input type="text" id="receiverAcc"></div>
<div class="form-group"><label>Currency</label>
    <select id="currency">{currency_options}</select></div>
<div class="form-group"><label>Amount</label><input type="text" id="amount"></div>
<div class="form-group"><label>Reference/Memo</label><input type="text" id="memo" value="IP-TRANSFER"></div>
<div class="error-msg hidden" id="dataError"></div>
<button class="btn" onclick="submitData()">Execute Transfer</button>
"""

IP2IP_JS = """
function getAuthBody() {
    var token = document.getElementById('tokenInput').value.trim().toUpperCase();
    if (!token) return null;
    return {module: MODULE_KEY, token: token};
}
function onAuthSuccess(data) {
    if (data.user_data) {
        var html = '<div class="customer-box"><h4>OPERATOR INFO</h4>';
        html += '<div class="row"><span class="key">Operator</span><span class="value">'+(data.user_data.operator||'')+'</span></div>';
        html += '<div class="row"><span class="key">Clearance</span><span class="value">'+(data.user_data.clearance||'')+'</span></div>';
        html += '<div class="row"><span class="key">Region</span><span class="value">'+(data.user_data.region||'')+'</span></div>';
        html += '</div>';
        document.getElementById('customerInfo').innerHTML = html;
    }
}
function getDataBody() {
    hideDataError();
    return {
        src_ip: document.getElementById('srcIp').value.trim(),
        src_port: document.getElementById('srcPort').value.trim(),
        dst_ip: document.getElementById('dstIp').value.trim(),
        dst_port: document.getElementById('dstPort').value.trim(),
        sender_name: document.getElementById('senderName').value.trim(),
        sender_acc: document.getElementById('senderAcc').value.trim(),
        receiver_name: document.getElementById('receiverName').value.trim(),
        receiver_acc: document.getElementById('receiverAcc').value.trim(),
        currency: document.getElementById('currency').value,
        amount: document.getElementById('amount').value.trim(),
        memo: document.getElementById('memo').value.trim()
    };
}
function showDataError(msg) { var el=document.getElementById('dataError'); el.textContent=msg; el.classList.remove('hidden'); }
function hideDataError() { document.getElementById('dataError').classList.add('hidden'); }
"""



# =====================================================================
# [ S2S MODULE FORMS AND JS ]
# =====================================================================
S2S_AUTH_FORM = """
<div class="form-group">
    <label>5-Character API Token</label>
    <input type="text" id="tokenInput" maxlength="5" placeholder="Enter token"
           style="text-transform:uppercase;">
</div>
<button class="btn" onclick="submitAuth()">Authenticate</button>
"""

S2S_DATA_FORM = """
<h3>API Configuration</h3>
<div class="form-group"><label>Settlement Endpoint URL</label><input type="text" id="endpointUrl" placeholder="https://api.payment.net/v3/settle"></div>
<div class="form-group"><label>API Key (Bearer)</label><input type="text" id="apiKey" placeholder="sk_live_..."></div>
<div class="form-group"><label>Webhook Callback URL</label><input type="text" id="webhookUrl" placeholder="https://..."></div>
<h3>Payment Payload</h3>
<div class="form-group"><label>Merchant ID</label><input type="text" id="merchantId"></div>
<div class="form-group"><label>Customer Reference</label><input type="text" id="customerId"></div>
<div class="form-group"><label>Beneficiary Name</label><input type="text" id="benName"></div>
<div class="form-group"><label>Beneficiary Account</label><input type="text" id="benAccount"></div>
<div class="form-group"><label>Beneficiary Bank</label><input type="text" id="benBank"></div>
<div class="form-group"><label>Currency</label>
    <select id="currency">{currency_options}</select></div>
<div class="form-group"><label>Amount</label><input type="text" id="amount"></div>
<div class="form-group"><label>Description</label><input type="text" id="description" value="S2S Payment"></div>
<div class="error-msg hidden" id="dataError"></div>
<button class="btn" onclick="submitData()">Send API Request</button>
"""

S2S_JS = """
function getAuthBody() {
    var token = document.getElementById('tokenInput').value.trim().toUpperCase();
    if (!token) return null;
    return {module: MODULE_KEY, token: token};
}
function onAuthSuccess(data) {
    if (data.user_data) {
        var html = '<div class="customer-box"><h4>ENGINE INFO</h4>';
        html += '<div class="row"><span class="key">Engine</span><span class="value">'+(data.user_data.name||'')+'</span></div>';
        html += '<div class="row"><span class="key">Merchant</span><span class="value">'+(data.user_data.merchant||'')+'</span></div>';
        html += '<div class="row"><span class="key">API Version</span><span class="value">'+(data.user_data.api_version||'')+'</span></div>';
        html += '<div class="row"><span class="key">Environment</span><span class="value">'+(data.user_data.environment||'')+'</span></div>';
        html += '</div>';
        document.getElementById('customerInfo').innerHTML = html;
    }
}
function getDataBody() {
    hideDataError();
    return {
        endpoint_url: document.getElementById('endpointUrl').value.trim(),
        api_key: document.getElementById('apiKey').value.trim(),
        webhook_url: document.getElementById('webhookUrl').value.trim(),
        merchant_id: document.getElementById('merchantId').value.trim(),
        customer_id: document.getElementById('customerId').value.trim(),
        ben_name: document.getElementById('benName').value.trim(),
        ben_account: document.getElementById('benAccount').value.trim(),
        ben_bank: document.getElementById('benBank').value.trim(),
        currency: document.getElementById('currency').value,
        amount: document.getElementById('amount').value.trim(),
        description: document.getElementById('description').value.trim()
    };
}
function showDataError(msg) { var el=document.getElementById('dataError'); el.textContent=msg; el.classList.remove('hidden'); }
function hideDataError() { document.getElementById('dataError').classList.add('hidden'); }
"""



# =====================================================================
# [ GPI MODULE FORMS AND JS ]
# =====================================================================
GPI_AUTH_FORM = """
<div class="form-group">
    <label>5-Character GPI Token</label>
    <input type="text" id="tokenInput" maxlength="5" placeholder="Enter token"
           style="text-transform:uppercase;">
</div>
<button class="btn" onclick="submitAuth()">Authenticate</button>
"""

GPI_DATA_FORM = """
<h3>GPI Payment Initiation</h3>
<div class="form-group"><label>Ordering Institution (BIC)</label><input type="text" id="orderingInst" style="text-transform:uppercase;"></div>
<div class="form-group"><label>Ordering Customer Name</label><input type="text" id="orderingName"></div>
<div class="form-group"><label>Ordering Account</label><input type="text" id="orderingAcc"></div>
<div class="form-group"><label>Beneficiary Institution (BIC)</label><input type="text" id="benInst" placeholder="BNPAFRPPXXX" style="text-transform:uppercase;"></div>
<div class="form-group"><label>Beneficiary Name</label><input type="text" id="benName"></div>
<div class="form-group"><label>Beneficiary Account (IBAN)</label><input type="text" id="benAcc"></div>
<div class="form-group"><label>Currency</label>
    <select id="currency">{currency_options}</select></div>
<div class="form-group"><label>Amount</label><input type="text" id="amount"></div>
<div class="form-group"><label>Charge Bearer</label>
    <select id="chargeBearer"><option value="SHA">SHA</option><option value="OUR">OUR</option><option value="BEN">BEN</option></select></div>
<div class="form-group"><label>Remittance Info</label><input type="text" id="remitInfo" value="PAYMENT"></div>
<div class="error-msg hidden" id="dataError"></div>
<button class="btn" onclick="submitData()">Initiate GPI Transfer</button>
"""

GPI_JS = """
function getAuthBody() {
    var token = document.getElementById('tokenInput').value.trim().toUpperCase();
    if (!token) return null;
    return {module: MODULE_KEY, token: token};
}
function onAuthSuccess(data) {
    if (data.user_data) {
        var html = '<div class="customer-box"><h4>INSTITUTION INFO</h4>';
        html += '<div class="row"><span class="key">Institution</span><span class="value">'+(data.user_data.institution||'')+'</span></div>';
        html += '<div class="row"><span class="key">BIC</span><span class="value">'+(data.user_data.bic||'')+'</span></div>';
        html += '<div class="row"><span class="key">GPI Member ID</span><span class="value">'+(data.user_data.gpi_member_id||'')+'</span></div>';
        html += '</div>';
        document.getElementById('customerInfo').innerHTML = html;
        if (data.user_data.bic) {
            document.getElementById('orderingInst').value = data.user_data.bic;
        }
    }
}
function getDataBody() {
    hideDataError();
    return {
        ordering_inst: document.getElementById('orderingInst').value.trim().toUpperCase(),
        ordering_name: document.getElementById('orderingName').value.trim(),
        ordering_acc: document.getElementById('orderingAcc').value.trim(),
        ben_inst: document.getElementById('benInst').value.trim().toUpperCase() || 'BNPAFRPPXXX',
        ben_name: document.getElementById('benName').value.trim(),
        ben_acc: document.getElementById('benAcc').value.trim(),
        currency: document.getElementById('currency').value,
        amount: document.getElementById('amount').value.trim(),
        charge_bearer: document.getElementById('chargeBearer').value,
        remit_info: document.getElementById('remitInfo').value.trim()
    };
}
function showDataError(msg) { var el=document.getElementById('dataError'); el.textContent=msg; el.classList.remove('hidden'); }
function hideDataError() { document.getElementById('dataError').classList.add('hidden'); }
"""



# =====================================================================
# [ MT103 MODULE FORMS AND JS ]
# =====================================================================
MT103_AUTH_FORM = """
<div class="form-group">
    <label>5-Character SWIFT Token</label>
    <input type="text" id="tokenInput" maxlength="5" placeholder="Enter token"
           style="text-transform:uppercase;">
</div>
<button class="btn" onclick="submitAuth()">Authenticate</button>
"""

MT103_DATA_FORM = """
<h3>MT103 Message Fields</h3>
<div class="form-group"><label>:20: Transaction Reference Number</label><input type="text" id="txnRef" placeholder="Auto-generated if blank"></div>
<div class="form-group"><label>:23B: Bank Operation Code</label><input type="text" id="bankOp" value="CRED" style="text-transform:uppercase;"></div>
<div class="form-group"><label>:32A: Value Date (YYMMDD)</label><input type="text" id="valueDate" maxlength="6"></div>
<div class="form-group"><label>Currency</label>
    <select id="currency">{currency_options}</select></div>
<div class="form-group"><label>Amount</label><input type="text" id="amount" value="1000000"></div>
<h3>Ordering Customer (:50K)</h3>
<div class="form-group"><label>Name</label><input type="text" id="ordName"></div>
<div class="form-group"><label>Account</label><input type="text" id="ordAcc"></div>
<div class="form-group"><label>Address</label><input type="text" id="ordAddr"></div>
<h3>Institutions</h3>
<div class="form-group"><label>:52A: Ordering Institution (BIC)</label><input type="text" id="ordInst" style="text-transform:uppercase;"></div>
<div class="form-group"><label>:53A: Sender Correspondent</label><input type="text" id="sndCorr" value="CHASUS33XXX" style="text-transform:uppercase;"></div>
<div class="form-group"><label>:57A: Account With Institution</label><input type="text" id="accInst" value="BNPAFRPPXXX" style="text-transform:uppercase;"></div>
<h3>Beneficiary (:59)</h3>
<div class="form-group"><label>Name</label><input type="text" id="benName"></div>
<div class="form-group"><label>Account</label><input type="text" id="benAcc"></div>
<div class="form-group"><label>Address</label><input type="text" id="benAddr"></div>
<h3>Additional</h3>
<div class="form-group"><label>:71A: Details of Charges</label>
    <select id="charges"><option value="SHA">SHA</option><option value="OUR">OUR</option><option value="BEN">BEN</option></select></div>
<div class="form-group"><label>:72: Sender-to-Receiver Info</label><input type="text" id="s2rInfo" value="/ACC/PAYMENT"></div>
<div class="error-msg hidden" id="dataError"></div>
<button class="btn" onclick="submitData()">Submit MT103 Message</button>
"""

MT103_JS = """
function getAuthBody() {
    var token = document.getElementById('tokenInput').value.trim().toUpperCase();
    if (!token) return null;
    return {module: MODULE_KEY, token: token};
}
function onAuthSuccess(data) {
    if (data.user_data) {
        var html = '<div class="customer-box"><h4>GATEWAY INFO</h4>';
        html += '<div class="row"><span class="key">Gateway</span><span class="value">'+(data.user_data.name||'')+'</span></div>';
        html += '<div class="row"><span class="key">Institution</span><span class="value">'+(data.user_data.institution||'')+'</span></div>';
        html += '<div class="row"><span class="key">BIC</span><span class="value">'+(data.user_data.bic||'')+'</span></div>';
        html += '<div class="row"><span class="key">Branch</span><span class="value">'+(data.user_data.branch||'')+'</span></div>';
        html += '</div>';
        document.getElementById('customerInfo').innerHTML = html;
        if (data.user_data.bic) {
            document.getElementById('ordInst').value = data.user_data.bic;
        }
    }
}
function getDataBody() {
    hideDataError();
    return {
        txn_ref: document.getElementById('txnRef').value.trim(),
        bank_op: document.getElementById('bankOp').value.trim().toUpperCase() || 'CRED',
        value_date: document.getElementById('valueDate').value.trim(),
        currency: document.getElementById('currency').value,
        amount: document.getElementById('amount').value.trim(),
        ord_name: document.getElementById('ordName').value.trim(),
        ord_acc: document.getElementById('ordAcc').value.trim(),
        ord_addr: document.getElementById('ordAddr').value.trim(),
        ord_inst: document.getElementById('ordInst').value.trim().toUpperCase(),
        snd_corr: document.getElementById('sndCorr').value.trim().toUpperCase(),
        acc_inst: document.getElementById('accInst').value.trim().toUpperCase(),
        ben_name: document.getElementById('benName').value.trim(),
        ben_acc: document.getElementById('benAcc').value.trim(),
        ben_addr: document.getElementById('benAddr').value.trim(),
        charges: document.getElementById('charges').value,
        s2r_info: document.getElementById('s2rInfo').value.trim()
    };
}
function showDataError(msg) { var el=document.getElementById('dataError'); el.textContent=msg; el.classList.remove('hidden'); }
function hideDataError() { document.getElementById('dataError').classList.add('hidden'); }
"""



# =====================================================================
# [ RTGS MODULE FORMS AND JS ]
# =====================================================================
RTGS_AUTH_FORM = """
<div class="form-group">
    <label>5-Character RTGS Token</label>
    <input type="text" id="tokenInput" maxlength="5" placeholder="Enter token"
           style="text-transform:uppercase;">
</div>
<button class="btn" onclick="submitAuth()">Authenticate</button>
"""

RTGS_DATA_FORM = """
<h3>RTGS System Selection</h3>
<div class="form-group"><label>Settlement System</label>
    <select id="rtgsSystem">{rtgs_options}</select></div>
<h3>Payment Instruction</h3>
<div class="form-group"><label>Sending Bank (Name)</label><input type="text" id="senderBank"></div>
<div class="form-group"><label>Sending Bank BIC/Routing</label><input type="text" id="senderBic" style="text-transform:uppercase;"></div>
<div class="form-group"><label>Sender Account Number</label><input type="text" id="senderAcc"></div>
<div class="form-group"><label>Sender Name</label><input type="text" id="senderName"></div>
<div class="form-group"><label>Receiving Bank (Name)</label><input type="text" id="receiverBank"></div>
<div class="form-group"><label>Receiving Bank BIC/Routing</label><input type="text" id="receiverBic" style="text-transform:uppercase;"></div>
<div class="form-group"><label>Receiver Account Number</label><input type="text" id="receiverAcc"></div>
<div class="form-group"><label>Receiver Name</label><input type="text" id="receiverName"></div>
<div class="form-group"><label>Currency</label>
    <select id="currency">{currency_options}</select></div>
<div class="form-group"><label>Amount (min 1,000,000)</label><input type="text" id="amount"></div>
<div class="form-group"><label>Payment Purpose</label><input type="text" id="purpose" value="HIGH-VALUE SETTLEMENT"></div>
<div class="form-group"><label>Priority</label>
    <select id="priority"><option value="URGENT">URGENT</option><option value="NORMAL">NORMAL</option></select></div>
<div class="error-msg hidden" id="dataError"></div>
<button class="btn" onclick="submitData()">Submit RTGS Payment</button>
"""

RTGS_JS = """
function getAuthBody() {
    var token = document.getElementById('tokenInput').value.trim().toUpperCase();
    if (!token) return null;
    return {module: MODULE_KEY, token: token};
}
function onAuthSuccess(data) {
    if (data.user_data) {
        var html = '<div class="customer-box"><h4>SYSTEM INFO</h4>';
        html += '<div class="row"><span class="key">System</span><span class="value">'+(data.user_data.name||'')+'</span></div>';
        html += '<div class="row"><span class="key">Operator</span><span class="value">'+(data.user_data.system||'')+'</span></div>';
        html += '<div class="row"><span class="key">Routing</span><span class="value">'+(data.user_data.routing||'')+'</span></div>';
        html += '<div class="row"><span class="key">Node</span><span class="value">'+(data.user_data.node||'')+'</span></div>';
        html += '</div>';
        document.getElementById('customerInfo').innerHTML = html;
    }
}
function getDataBody() {
    hideDataError();
    return {
        rtgs_system: document.getElementById('rtgsSystem').value,
        sender_bank: document.getElementById('senderBank').value.trim(),
        sender_bic: document.getElementById('senderBic').value.trim().toUpperCase(),
        sender_acc: document.getElementById('senderAcc').value.trim(),
        sender_name: document.getElementById('senderName').value.trim(),
        receiver_bank: document.getElementById('receiverBank').value.trim(),
        receiver_bic: document.getElementById('receiverBic').value.trim().toUpperCase(),
        receiver_acc: document.getElementById('receiverAcc').value.trim(),
        receiver_name: document.getElementById('receiverName').value.trim(),
        currency: document.getElementById('currency').value,
        amount: document.getElementById('amount').value.trim(),
        purpose: document.getElementById('purpose').value.trim(),
        priority: document.getElementById('priority').value
    };
}
function showDataError(msg) { var el=document.getElementById('dataError'); el.textContent=msg; el.classList.remove('hidden'); }
function hideDataError() { document.getElementById('dataError').classList.add('hidden'); }
"""



# =====================================================================
# [ MODULE CONFIGURATION HELPER ]
# =====================================================================
MODULE_INFO = {
    "protocol_transaction": {
        "title": "Protocol Transaction Engine",
        "desc": "Card-based multi-protocol settlement with Visa/MC auto-detect",
        "auth_form": "PROTOCOL_AUTH_FORM",
        "data_form": "PROTOCOL_DATA_FORM",
        "js": "PROTOCOL_JS",
    },
    "interbank": {
        "title": "Interbank Transfer",
        "desc": "SWIFT Network interbank fund settlement engine",
        "auth_form": "INTERBANK_AUTH_FORM",
        "data_form": "INTERBANK_DATA_FORM",
        "js": "INTERBANK_JS",
    },
    "ip_to_ip": {
        "title": "IP-to-IP Transfer",
        "desc": "Direct peer-to-peer IP tunnel fund transfer",
        "auth_form": "IP2IP_AUTH_FORM",
        "data_form": "IP2IP_DATA_FORM",
        "js": "IP2IP_JS",
    },
    "s2s": {
        "title": "Server-to-Server (S2S)",
        "desc": "RESTful payment processing between merchant servers",
        "auth_form": "S2S_AUTH_FORM",
        "data_form": "S2S_DATA_FORM",
        "js": "S2S_JS",
    },
    "gpi": {
        "title": "SWIFT GPI",
        "desc": "Global Payment Innovation - end-to-end payment tracking",
        "auth_form": "GPI_AUTH_FORM",
        "data_form": "GPI_DATA_FORM",
        "js": "GPI_JS",
    },
    "mt103": {
        "title": "SWIFT MT103",
        "desc": "Single Customer Credit Transfer - FIN message format",
        "auth_form": "MT103_AUTH_FORM",
        "data_form": "MT103_DATA_FORM",
        "js": "MT103_JS",
    },
    "rtgs": {
        "title": "RTGS Settlement",
        "desc": "Real-Time Gross Settlement System - high-value payments",
        "auth_form": "RTGS_AUTH_FORM",
        "data_form": "RTGS_DATA_FORM",
        "js": "RTGS_JS",
    },
}


def get_form_template(name):
    """Get form template by name."""
    templates = {
        "PROTOCOL_AUTH_FORM": PROTOCOL_AUTH_FORM,
        "PROTOCOL_DATA_FORM": PROTOCOL_DATA_FORM,
        "PROTOCOL_JS": PROTOCOL_JS,
        "INTERBANK_AUTH_FORM": INTERBANK_AUTH_FORM,
        "INTERBANK_DATA_FORM": INTERBANK_DATA_FORM,
        "INTERBANK_JS": INTERBANK_JS,
        "IP2IP_AUTH_FORM": IP2IP_AUTH_FORM,
        "IP2IP_DATA_FORM": IP2IP_DATA_FORM,
        "IP2IP_JS": IP2IP_JS,
        "S2S_AUTH_FORM": S2S_AUTH_FORM,
        "S2S_DATA_FORM": S2S_DATA_FORM,
        "S2S_JS": S2S_JS,
        "GPI_AUTH_FORM": GPI_AUTH_FORM,
        "GPI_DATA_FORM": GPI_DATA_FORM,
        "GPI_JS": GPI_JS,
        "MT103_AUTH_FORM": MT103_AUTH_FORM,
        "MT103_DATA_FORM": MT103_DATA_FORM,
        "MT103_JS": MT103_JS,
        "RTGS_AUTH_FORM": RTGS_AUTH_FORM,
        "RTGS_DATA_FORM": RTGS_DATA_FORM,
        "RTGS_JS": RTGS_JS,
    }
    return templates.get(name, "")


def build_currency_options():
    """Build HTML options for currency select."""
    return ''.join(f'<option value="{c}">{c}</option>' for c in CURRENCIES)


def build_proto_options():
    """Build HTML options for protocol select."""
    return ''.join(f'<option value="{p}">{p}</option>' for p in TRANSACTION_PROTOCOLS)


def build_usdt_options():
    """Build HTML options for USDT network select."""
    return ''.join(f'<option value="{n}">{n}</option>' for n in USDT_NETWORKS)


def build_rtgs_options():
    """Build HTML options for RTGS systems."""
    return ''.join(f'<option value="{s}">{s}</option>' for s in RTGS_SYSTEMS)


def render_module_page(module_key):
    """Render complete HTML page for a module."""
    info = MODULE_INFO.get(module_key)
    if not info:
        return None

    currency_opts = build_currency_options()
    proto_opts = build_proto_options()
    usdt_opts = build_usdt_options()
    rtgs_opts = build_rtgs_options()

    auth_form = get_form_template(info["auth_form"])
    data_form = get_form_template(info["data_form"])
    data_form = data_form.replace("{currency_options}", currency_opts)
    data_form = data_form.replace("{proto_options}", proto_opts)
    data_form = data_form.replace("{usdt_options}", usdt_opts)
    data_form = data_form.replace("{rtgs_options}", rtgs_opts)

    module_js = BASE_MODULE_JS + "\n" + get_form_template(info["js"])

    duration = LOADING_DURATION.get(module_key, 2.0)
    messages = LOADING_MESSAGES.get(module_key, ["Processing..."])

    html = MODULE_PAGE_TEMPLATE.format(
        css=CSS_STYLES,
        module_title=info["title"],
        module_desc=info["desc"],
        module_key=module_key,
        auth_form_html=auth_form,
        data_form_html=data_form,
        loading_duration=duration,
        loading_messages_json=json.dumps(messages),
        module_js=module_js,
    )
    return html



# =====================================================================
# [ HTTP REQUEST HANDLER ]
# =====================================================================
class GPSEHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the GPSE web GUI."""

    def log_message(self, format, *args):
        """Suppress default logging to keep console clean."""
        pass

    def send_json(self, data, status=200):
        """Send JSON response."""
        body = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, html, status=200):
        """Send HTML response."""
        body = html.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        """Handle GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/')

        if path == '' or path == '/':
            self.serve_main_page()
        elif path.startswith('/module/'):
            module_key = path[len('/module/'):]
            self.serve_module_page(module_key)
        elif path.startswith('/api/bin/'):
            card_prefix = path[len('/api/bin/'):]
            self.serve_bin_lookup(card_prefix)
        elif path == '/api/status':
            self.send_json({
                "version": VERSION,
                "build": BUILD,
                "modules": 7,
                "status": "OPERATIONAL",
            })
        else:
            self.send_html("<h1>404 Not Found</h1>", 404)

    def do_POST(self):
        """Handle POST requests."""
        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/')

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else '{}'

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_json({"error": "Invalid JSON"}, 400)
            return

        if path == '/api/auth':
            self.handle_auth(data)
        elif path == '/api/process':
            self.handle_process(data)
        else:
            self.send_json({"error": "Not found"}, 404)

    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def serve_main_page(self):
        """Serve the main page."""
        html = MAIN_PAGE_TEMPLATE.format(
            css=CSS_STYLES,
            version=VERSION,
            build=BUILD,
        )
        self.send_html(html)

    def serve_module_page(self, module_key):
        """Serve a module page."""
        html = render_module_page(module_key)
        if html:
            self.send_html(html)
        else:
            self.send_html("<h1>Module not found</h1>", 404)

    def serve_bin_lookup(self, card_prefix):
        """BIN lookup API endpoint."""
        card_prefix = card_prefix.replace(' ', '').replace('-', '')
        network, brand = detect_card_brand(card_prefix)
        self.send_json({"network": network, "brand": brand, "prefix": card_prefix})

    def handle_auth(self, data):
        """Handle authentication requests."""
        module_key = data.get("module", "")

        # Reload config to pick up any changes from settings editor
        load_config()

        if module_key == "interbank":
            return self.handle_interbank_auth(data)

        # Token-based auth for all other modules
        token = data.get("token", "").strip().upper()
        tokens = MODULE_TOKENS.get(module_key, {})

        if token not in tokens:
            self.send_json({"success": False, "error": "ACCESS DENIED - Invalid token"})
            return

        user_data = tokens[token]
        # Return user data (exclude sensitive fields like password_hash)
        safe_data = {k: v for k, v in user_data.items() if k != "password_hash"}
        self.send_json({"success": True, "user_data": safe_data})

    def handle_interbank_auth(self, data):
        """Handle interbank username/password auth."""
        username = data.get("username", "").strip()
        password = data.get("password", "")

        admin_token = MODULE_TOKENS.get("interbank", {}).get("ADMIN", {})
        if not admin_token:
            self.send_json({"success": False, "error": "No admin token configured"})
            return

        pw_hash = hashlib.sha256(password.encode()).hexdigest()
        if username == admin_token.get("username") and pw_hash == admin_token.get("password_hash"):
            self.send_json({"success": True, "user_data": {"name": admin_token.get("name", "ADMIN")}})
        else:
            self.send_json({"success": False, "error": "ACCESS DENIED - Invalid credentials"})

    def handle_process(self, data):
        """Handle transaction processing."""
        module_key = data.get("module", "")
        result_status = RESULT_CONFIG.get(module_key, "SUCCESS").upper()
        custom_msg = RESULT_MESSAGE.get(module_key, "")

        if result_status == "SUCCESS":
            message = custom_msg or "Transaction settled successfully. Funds confirmed."
        elif result_status == "PENDING":
            message = custom_msg or "Transaction queued for manual review."
        else:
            message = custom_msg or "Transaction declined by settlement engine."

        # Build transaction details based on module
        details = self.build_tx_details(module_key, data)

        self.send_json({
            "result": result_status,
            "message": message,
            "details": details,
        })

    def build_tx_details(self, module_key, data):
        """Build transaction detail dict per module."""
        now_ts = f"{datestamp()} {ts()}"
        sig = ''.join(random.choices(string.ascii_uppercase + string.digits, k=24))

        if module_key == "protocol_transaction":
            return self.build_protocol_details(data, now_ts, sig)
        elif module_key == "interbank":
            return self.build_interbank_details(data, now_ts)
        elif module_key == "ip_to_ip":
            return self.build_ip2ip_details(data, now_ts)
        elif module_key == "s2s":
            return self.build_s2s_details(data, now_ts)
        elif module_key == "gpi":
            return self.build_gpi_details(data, now_ts)
        elif module_key == "mt103":
            return self.build_mt103_details(data, now_ts)
        elif module_key == "rtgs":
            return self.build_rtgs_details(data, now_ts)
        else:
            return {"TX Reference": gen_ref("TXN"), "Timestamp": now_ts}

    def build_protocol_details(self, data, now_ts, sig):
        """Build protocol transaction details with card validation."""
        card = data.get("card_number", "")
        last4 = card[-4:] if len(card) >= 4 else "0000"
        token = data.get("token", "").upper()
        tokens = MODULE_TOKENS.get("protocol_transaction", {})
        user_data = tokens.get(token, {})

        # Validate allowed_card_last4
        allowed = user_data.get("allowed_card_last4")
        if allowed and last4 != allowed:
            return {
                "TX Reference": gen_ref("PTX"),
                "Status": "CARD NOT AUTHORIZED",
                "Timestamp": now_ts,
            }

        network, brand = detect_card_brand(card)
        details = {
            "TX Reference": f"PTX-{random.randint(100000000, 999999999)}",
            "Protocol": data.get("protocol", "N/A"),
            "Card": f"**** **** **** {last4}",
            "Network": network,
            "Brand": brand,
        }
        if data.get("transfer_type") == "crypto":
            details["Type"] = "Crypto Transfer"
            details["Crypto Network"] = data.get("crypto_network", "N/A")
            details["Amount"] = f"EUR {data.get('amount', '0')}"
        else:
            details["Type"] = "Bank Transfer"
            details["Bank"] = data.get("dest_bank", "N/A")
            details["Beneficiary"] = data.get("ben_name", "N/A")
            details["Amount"] = f"{data.get('currency', 'EUR')} {data.get('amount', '0')}"
        details["Timestamp"] = now_ts
        details["Signature"] = sig
        return details

    def build_interbank_details(self, data, now_ts):
        """Build interbank transfer details."""
        acc = data.get("account_no", "")
        masked_acc = '*' * max(0, len(acc) - 4) + acc[-4:] if len(acc) > 4 else acc
        holder = ACCOUNT_HOLDER_MAP.get(acc, "ACCOUNT HOLDER")
        return {
            "TX Reference": gen_ref("IBK"),
            "Bank": data.get("dest_bank", "N/A").upper(),
            "Account": masked_acc,
            "Holder": holder,
            "TRN": data.get("trn", "N/A"),
            "Timestamp": now_ts,
        }

    def build_ip2ip_details(self, data, now_ts):
        """Build IP-to-IP transfer details."""
        import time as _time
        tunnel_id = hashlib.sha256(f"{_time.time()}{random.randint(0,99999)}".encode()).hexdigest()[:12].upper()
        src = data.get("src_ip", "0.0.0.0") + ":" + data.get("src_port", "8443")
        dst = data.get("dst_ip", "0.0.0.0") + ":" + data.get("dst_port", "8443")
        return {
            "TX Reference": gen_ref("IP2"),
            "Tunnel ID": tunnel_id,
            "Source": src,
            "Destination": dst,
            "Sender": data.get("sender_name", "N/A"),
            "Receiver": data.get("receiver_name", "N/A"),
            "Amount": f"{data.get('currency', 'EUR')} {data.get('amount', '0')}",
            "Timestamp": now_ts,
        }

    def build_s2s_details(self, data, now_ts):
        """Build S2S transfer details."""
        endpoint = data.get("endpoint_url", "N/A")
        if len(endpoint) > 35:
            endpoint = endpoint[:35] + "..."
        return {
            "TX Reference": gen_ref("S2S"),
            "Merchant": data.get("merchant_id", "N/A"),
            "Customer": data.get("customer_id", "N/A"),
            "Beneficiary": data.get("ben_name", "N/A"),
            "Bank": data.get("ben_bank", "N/A"),
            "Amount": f"{data.get('currency', 'EUR')} {data.get('amount', '0')}",
            "Endpoint": endpoint,
            "Timestamp": now_ts,
        }

    def build_gpi_details(self, data, now_ts):
        """Build GPI transfer details."""
        uetr = gen_uetr()
        gpi_status = "CREDITED" if RESULT_CONFIG.get("gpi") == "SUCCESS" else "REJECTED"
        return {
            "UETR": uetr,
            "Ordering BIC": data.get("ordering_inst", "N/A"),
            "Beneficiary BIC": data.get("ben_inst", "N/A"),
            "Beneficiary": data.get("ben_name", "N/A"),
            "Amount": f"{data.get('currency', 'EUR')} {data.get('amount', '0')}",
            "Charge Bearer": data.get("charge_bearer", "SHA"),
            "GPI Status": gpi_status,
            "Timestamp": now_ts,
        }

    def build_mt103_details(self, data, now_ts):
        """Build MT103 transfer details."""
        txn_ref = data.get("txn_ref") or gen_ref("FT")
        return {
            "MT103 Ref": txn_ref,
            "Value Date": data.get("value_date", "N/A"),
            "Currency/Amt": f"{data.get('currency', 'EUR')} {data.get('amount', '0')}",
            "Ordering": f"{data.get('ord_name', 'N/A')} ({data.get('ord_inst', 'N/A')})",
            "Beneficiary": f"{data.get('ben_name', 'N/A')} ({data.get('acc_inst', 'N/A')})",
            "Charges": data.get("charges", "SHA"),
            "UETR": gen_uetr(),
            "Timestamp": now_ts,
        }

    def build_rtgs_details(self, data, now_ts):
        """Build RTGS settlement details."""
        system = data.get("rtgs_system", "FEDWIRE")
        if "(" in system:
            system = system.split("(")[0].strip()
        ref = f"RTGS-{datetime.datetime.now().strftime('%Y%m%d')}-{random.randint(100000,999999)}"
        return {
            "Settlement Ref": ref,
            "System": system,
            "Sender": f"{data.get('sender_name', 'N/A')} ({data.get('sender_bic', 'N/A')})",
            "Receiver": f"{data.get('receiver_name', 'N/A')} ({data.get('receiver_bic', 'N/A')})",
            "Amount": f"{data.get('currency', 'EUR')} {data.get('amount', '0')}",
            "Priority": data.get("priority", "URGENT"),
            "Finality": "IRREVOCABLE",
            "Timestamp": now_ts,
        }



# =====================================================================
# [ SERVER STARTUP ]
# =====================================================================
class GPSEServer(HTTPServer):
    """HTTP server with SO_REUSEADDR enabled."""
    allow_reuse_address = True


def main():
    """Start the GPSE web server on port 8080."""
    port = 8080
    server = GPSEServer(('', port), GPSEHandler)

    print(f"")
    print(f"  =====================================================")
    print(f"  GLOBAL PAYMENT SETTLEMENT ENGINE v{VERSION}")
    print(f"  Build {BUILD} | Web Interface")
    print(f"  =====================================================")
    print(f"")
    print(f"  Engine running at:   http://localhost:{port}")
    print(f"  Settings editor at:  http://localhost:8585")
    print(f"")
    print(f"  Press Ctrl+C to stop the server.")
    print(f"  =====================================================")
    print(f"")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(f"\n  Server stopped.")
        server.server_close()


# =====================================================================
# [ ENTRY POINT ]
# =====================================================================
if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg in ("-h", "--help"):
            print(f"GLOBAL PAYMENT SETTLEMENT ENGINE v{VERSION}")
            print(f"Usage: python engine.py")
            print(f"")
            print(f"Starts web server on http://localhost:8080")
            print(f"Modules: Protocol TX | Interbank | IP-to-IP | S2S | GPI | MT103 | RTGS")
            print(f"")
            print(f"Access tokens are required per module.")
            sys.exit(0)
        elif arg in ("-v", "--version"):
            print(f"GPSE v{VERSION} (Build {BUILD})")
            sys.exit(0)

    main()
