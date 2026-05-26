#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPSE Configuration Editor v2.0
Web-based settings editor for config.json
Runs on http://localhost:8585
LOADING_DURATION controls all internal timing distribution per module.
"""

import os
import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# =====================================================================
# [ CONFIGURATION PATH ]
# =====================================================================
try:
    CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
except NameError:
    CONFIG_PATH = os.path.join(os.getcwd(), "config.json")

PORT = 8585

# =====================================================================
# [ CONFIG LOAD / SAVE ]
# =====================================================================
def load_config():
    """Load configuration from config.json."""
    if not os.path.exists(CONFIG_PATH):
        print(f"[ERROR] config.json not found at: {CONFIG_PATH}")
        sys.exit(1)
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON in config.json: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"[ERROR] Cannot read config.json: {e}")
        sys.exit(1)
    return config


def save_config(config):
    """Save configuration to config.json with proper formatting and permissions."""
    try:
        json_str = json.dumps(config, indent=2, ensure_ascii=False)
    except (TypeError, ValueError) as e:
        return False, str(e)
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            f.write(json_str)
        os.chmod(CONFIG_PATH, 0o600)
        return True, ""
    except IOError as e:
        return False, str(e)


# =====================================================================
# [ HTML PAGE - EMBEDDED ]
# =====================================================================
HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GPSE Configuration Editor</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    background: #0a0a0a;
    color: #c8c8c8;
    font-family: 'Courier New', monospace;
    font-size: 14px;
    min-height: 100vh;
}
.container {
    max-width: 1100px;
    margin: 0 auto;
    padding: 20px;
}
.header {
    text-align: center;
    padding: 20px 0;
    border-bottom: 1px solid #1a3a4a;
    margin-bottom: 20px;
}
.header h1 {
    color: #00e5ff;
    font-size: 22px;
    letter-spacing: 2px;
}
.header p {
    color: #607070;
    font-size: 12px;
    margin-top: 6px;
}
.tabs {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    margin-bottom: 20px;
    border-bottom: 1px solid #1a3a4a;
    padding-bottom: 10px;
}
.tab-btn {
    background: #111;
    color: #888;
    border: 1px solid #222;
    padding: 8px 16px;
    cursor: pointer;
    font-family: inherit;
    font-size: 12px;
    border-radius: 4px 4px 0 0;
    transition: all 0.2s;
}
.tab-btn:hover { color: #00e5ff; border-color: #00e5ff; }
.tab-btn.active {
    background: #0d2a35;
    color: #00e5ff;
    border-color: #00e5ff;
    border-bottom-color: #0d2a35;
}
.tab-content { display: none; }
.tab-content.active { display: block; }
.section-title {
    color: #00e5ff;
    font-size: 16px;
    margin-bottom: 15px;
    padding-bottom: 8px;
    border-bottom: 1px solid #1a3a4a;
}
.module-group {
    background: #111;
    border: 1px solid #1a2a2a;
    border-radius: 6px;
    padding: 15px;
    margin-bottom: 12px;
}
.module-group h3 {
    color: #4de8b0;
    font-size: 13px;
    margin-bottom: 10px;
}
.token-list {
    margin-left: 10px;
}
.token-item {
    background: #0a0a0a;
    border: 1px solid #1a2a2a;
    border-radius: 4px;
    padding: 10px;
    margin-bottom: 8px;
}
.token-item .token-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}
.token-item .token-id {
    color: #ffd740;
    font-weight: bold;
    font-size: 13px;
}
.token-fields {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 8px;
}
.field-row {
    display: flex;
    flex-direction: column;
    gap: 2px;
}
.field-row label {
    color: #607070;
    font-size: 11px;
    text-transform: uppercase;
}
.field-row input, .field-row select, .field-row textarea {
    background: #0d1a1a;
    border: 1px solid #1a3a4a;
    color: #c8c8c8;
    padding: 6px 8px;
    border-radius: 3px;
    font-family: inherit;
    font-size: 13px;
}
.field-row input:focus, .field-row select:focus, .field-row textarea:focus {
    outline: none;
    border-color: #00e5ff;
}
.btn {
    background: #0d2a35;
    color: #00e5ff;
    border: 1px solid #00e5ff;
    padding: 6px 14px;
    cursor: pointer;
    font-family: inherit;
    font-size: 12px;
    border-radius: 3px;
    transition: all 0.2s;
}
.btn:hover {
    background: #00e5ff;
    color: #0a0a0a;
}
.btn-danger {
    border-color: #ff4444;
    color: #ff4444;
}
.btn-danger:hover {
    background: #ff4444;
    color: #0a0a0a;
}
.btn-success {
    border-color: #4de8b0;
    color: #4de8b0;
}
.btn-success:hover {
    background: #4de8b0;
    color: #0a0a0a;
}
.save-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: #111;
    border-top: 1px solid #1a3a4a;
    padding: 12px 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 15px;
    z-index: 1000;
}
.save-bar .btn {
    padding: 10px 30px;
    font-size: 14px;
}
.status-msg {
    color: #4de8b0;
    font-size: 12px;
    min-height: 18px;
}
.status-msg.error { color: #ff4444; }
.message-item {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
}
.message-item input {
    flex: 1;
    background: #0d1a1a;
    border: 1px solid #1a3a4a;
    color: #c8c8c8;
    padding: 6px 8px;
    border-radius: 3px;
    font-family: inherit;
    font-size: 13px;
}
.message-item input:focus { outline: none; border-color: #00e5ff; }
.bin-row {
    display: flex;
    gap: 10px;
    align-items: center;
    margin-bottom: 6px;
}
.bin-row input {
    background: #0d1a1a;
    border: 1px solid #1a3a4a;
    color: #c8c8c8;
    padding: 6px 8px;
    border-radius: 3px;
    font-family: inherit;
    font-size: 13px;
}
.bin-row input:first-child { width: 80px; }
.bin-row input:nth-child(2) { flex: 1; }
.padding-bottom { padding-bottom: 70px; }
select {
    background: #0d1a1a;
    border: 1px solid #1a3a4a;
    color: #c8c8c8;
    padding: 6px 8px;
    border-radius: 3px;
    font-family: inherit;
    font-size: 13px;
}
textarea {
    resize: vertical;
    min-height: 50px;
}
</style>
</head>
<body>
<div class="container padding-bottom">
<div class="header">
    <h1>[ GPSE CONFIGURATION EDITOR ]</h1>
    <p>Web-based settings manager v2.0 | http://localhost:8585</p>
</div>
<div class="tabs">
    <button class="tab-btn active" onclick="switchTab('tokens')">Module Tokens</button>
    <button class="tab-btn" onclick="switchTab('results')">Result Configuration</button>
    <button class="tab-btn" onclick="switchTab('duration')">Loading Duration</button>
    <button class="tab-btn" onclick="switchTab('messages')">Loading Messages</button>
    <button class="tab-btn" onclick="switchTab('bin')">BIN Database</button>
</div>
<div id="tab-tokens" class="tab-content active"></div>
<div id="tab-results" class="tab-content"></div>
<div id="tab-duration" class="tab-content"></div>
<div id="tab-messages" class="tab-content"></div>
<div id="tab-bin" class="tab-content"></div>
</div>
<div class="save-bar">
    <span class="status-msg" id="statusMsg"></span>
    <button class="btn btn-success" onclick="saveConfig()">SAVE CONFIGURATION</button>
</div>
<script>
let config = {};
const MODULES = ['protocol_transaction','interbank','ip_to_ip','s2s','gpi','mt103','rtgs'];
const MODULE_LABELS = {
    protocol_transaction: 'Protocol Transaction',
    interbank: 'Interbank Transfer',
    ip_to_ip: 'IP-to-IP Transfer',
    s2s: 'Server-to-Server (S2S)',
    gpi: 'SWIFT GPI',
    mt103: 'MT103 Transfer',
    rtgs: 'RTGS Settlement'
};
const TOKEN_TEMPLATES = {
    protocol_transaction: {name:'',cardholder:'',bank_provider:'',iso_country:'',iso_a2:'',iso_a3:'',iso_num:'',allowed_card_last4:''},
    interbank: {name:'',username:'',password_hash:''},
    ip_to_ip: {name:'',operator:'',clearance:'',region:''},
    s2s: {name:'',merchant:'',api_version:'',environment:''},
    gpi: {name:'',institution:'',bic:'',gpi_member_id:''},
    mt103: {name:'',institution:'',bic:'',branch:''},
    rtgs: {name:'',system:'',routing:'',node:''}
};

function switchTab(name) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
    document.getElementById('tab-' + name).classList.add('active');
    event.target.classList.add('active');
}

function setStatus(msg, isError) {
    const el = document.getElementById('statusMsg');
    el.textContent = msg;
    el.className = 'status-msg' + (isError ? ' error' : '');
    if (msg) setTimeout(() => { el.textContent = ''; }, 4000);
}

function loadConfig() {
    fetch('/api/config')
        .then(r => r.json())
        .then(data => { config = data; renderAll(); })
        .catch(e => setStatus('Failed to load config: ' + e, true));
}

function saveConfig() {
    collectAll();
    fetch('/api/config', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(config)
    })
    .then(r => r.json())
    .then(data => {
        if (data.ok) setStatus('Configuration saved successfully!', false);
        else setStatus('Save failed: ' + data.error, true);
    })
    .catch(e => setStatus('Save failed: ' + e, true));
}

function renderAll() {
    renderTokens();
    renderResults();
    renderDuration();
    renderMessages();
    renderBin();
}

function renderTokens() {
    let html = '<h2 class="section-title">Module Tokens</h2>';
    MODULES.forEach(mod => {
        const tokens = (config.MODULE_TOKENS && config.MODULE_TOKENS[mod]) || {};
        html += '<div class="module-group"><h3>' + MODULE_LABELS[mod] + '</h3><div class="token-list">';
        Object.keys(tokens).forEach(tid => {
            const tdata = tokens[tid];
            html += '<div class="token-item"><div class="token-header"><span class="token-id">' + tid + '</span>';
            html += '<button class="btn btn-danger" onclick="deleteToken(\'' + mod + '\',\'' + tid + '\')">Delete</button></div>';
            html += '<div class="token-fields" id="tf-' + mod + '-' + tid + '">';
            Object.keys(tdata).forEach(field => {
                const val = tdata[field] === null ? '' : tdata[field];
                html += '<div class="field-row"><label>' + field + '</label>';
                html += '<input type="text" data-mod="' + mod + '" data-tid="' + tid + '" data-field="' + field + '" value="' + escHtml(String(val)) + '"></div>';
            });
            html += '</div></div>';
        });
        html += '<button class="btn" onclick="addToken(\'' + mod + '\')">+ Add Token</button>';
        html += '</div></div>';
    });
    document.getElementById('tab-tokens').innerHTML = html;
}

function renderResults() {
    let html = '<h2 class="section-title">Result Configuration</h2>';
    MODULES.forEach(mod => {
        const status = (config.RESULT_CONFIG && config.RESULT_CONFIG[mod]) || 'SUCCESS';
        const msg = (config.RESULT_MESSAGE && config.RESULT_MESSAGE[mod]) || '';
        html += '<div class="module-group"><h3>' + MODULE_LABELS[mod] + '</h3>';
        html += '<div class="token-fields">';
        html += '<div class="field-row"><label>Status</label>';
        html += '<select data-result-mod="' + mod + '">';
        ['SUCCESS','FAILED','PENDING'].forEach(s => {
            html += '<option value="' + s + '"' + (s === status ? ' selected' : '') + '>' + s + '</option>';
        });
        html += '</select></div>';
        html += '<div class="field-row"><label>Custom Message</label>';
        html += '<textarea data-result-msg="' + mod + '">' + escHtml(msg) + '</textarea></div>';
        html += '</div></div>';
    });
    document.getElementById('tab-results').innerHTML = html;
}

function renderDuration() {
    let html = '<h2 class="section-title">Loading Duration (seconds per module)</h2>';
    html += '<p style="color:#607070;margin-bottom:15px;font-size:12px;">Controls how long the loading animation runs for each module. Replaces all individual timing settings.</p>';
    MODULES.forEach(mod => {
        const dur = (config.LOADING_DURATION && config.LOADING_DURATION[mod]) || 2.0;
        html += '<div class="module-group"><h3>' + MODULE_LABELS[mod] + '</h3>';
        html += '<div class="field-row"><label>Duration (seconds)</label>';
        html += '<input type="number" step="0.1" min="0.1" data-dur-mod="' + mod + '" value="' + dur + '"></div>';
        html += '</div>';
    });
    document.getElementById('tab-duration').innerHTML = html;
}

function renderMessages() {
    let html = '<h2 class="section-title">Loading Messages</h2>';
    MODULES.forEach(mod => {
        const msgs = (config.LOADING_MESSAGES && config.LOADING_MESSAGES[mod]) || [];
        html += '<div class="module-group"><h3>' + MODULE_LABELS[mod] + '</h3>';
        html += '<div id="msgs-' + mod + '">';
        msgs.forEach((m, i) => {
            html += '<div class="message-item"><input type="text" data-msg-mod="' + mod + '" data-msg-idx="' + i + '" value="' + escHtml(m) + '">';
            html += '<button class="btn btn-danger" onclick="removeMsg(\'' + mod + '\',' + i + ')">X</button></div>';
        });
        html += '</div>';
        html += '<button class="btn" onclick="addMsg(\'' + mod + '\')">+ Add Phrase</button>';
        html += '</div>';
    });
    document.getElementById('tab-messages').innerHTML = html;
}

function renderBin() {
    let html = '<h2 class="section-title">BIN Database</h2>';
    html += '<div class="module-group"><h3>Prefix to Card Brand Mapping</h3><div id="bin-list">';
    const bins = config.BIN_DATABASE || {};
    Object.keys(bins).forEach((prefix, i) => {
        html += '<div class="bin-row"><input type="text" data-bin-key="' + i + '" value="' + escHtml(prefix) + '">';
        html += '<input type="text" data-bin-val="' + i + '" value="' + escHtml(bins[prefix]) + '">';
        html += '<button class="btn btn-danger" onclick="removeBin(\'' + escHtml(prefix) + '\')">X</button></div>';
    });
    html += '</div><button class="btn" onclick="addBin()">+ Add Entry</button></div>';
    document.getElementById('tab-bin').innerHTML = html;
}

function escHtml(s) {
    return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function collectAll() {
    // Collect tokens
    document.querySelectorAll('[data-mod][data-tid][data-field]').forEach(el => {
        const mod = el.dataset.mod, tid = el.dataset.tid, field = el.dataset.field;
        if (!config.MODULE_TOKENS) config.MODULE_TOKENS = {};
        if (!config.MODULE_TOKENS[mod]) config.MODULE_TOKENS[mod] = {};
        if (!config.MODULE_TOKENS[mod][tid]) config.MODULE_TOKENS[mod][tid] = {};
        const val = el.value;
        if (field === 'allowed_card_last4' && val === '') {
            config.MODULE_TOKENS[mod][tid][field] = null;
        } else {
            config.MODULE_TOKENS[mod][tid][field] = val;
        }
    });
    // Collect results
    document.querySelectorAll('[data-result-mod]').forEach(el => {
        if (!config.RESULT_CONFIG) config.RESULT_CONFIG = {};
        config.RESULT_CONFIG[el.dataset.resultMod] = el.value;
    });
    document.querySelectorAll('[data-result-msg]').forEach(el => {
        if (!config.RESULT_MESSAGE) config.RESULT_MESSAGE = {};
        config.RESULT_MESSAGE[el.dataset.resultMsg] = el.value;
    });
    // Collect duration
    document.querySelectorAll('[data-dur-mod]').forEach(el => {
        if (!config.LOADING_DURATION) config.LOADING_DURATION = {};
        config.LOADING_DURATION[el.dataset.durMod] = parseFloat(el.value) || 2.0;
    });
    // Collect messages
    let msgMap = {};
    document.querySelectorAll('[data-msg-mod]').forEach(el => {
        const mod = el.dataset.msgMod;
        if (!msgMap[mod]) msgMap[mod] = [];
        msgMap[mod].push(el.value);
    });
    if (!config.LOADING_MESSAGES) config.LOADING_MESSAGES = {};
    MODULES.forEach(mod => {
        if (msgMap[mod]) config.LOADING_MESSAGES[mod] = msgMap[mod];
    });
    // Collect BIN
    let newBin = {};
    const binKeys = document.querySelectorAll('[data-bin-key]');
    const binVals = document.querySelectorAll('[data-bin-val]');
    for (let i = 0; i < binKeys.length; i++) {
        const k = binKeys[i].value.trim();
        const v = binVals[i].value.trim();
        if (k) newBin[k] = v;
    }
    config.BIN_DATABASE = newBin;
}

function addToken(mod) {
    const tid = prompt('Enter new Token ID (e.g. ABC12):');
    if (!tid) return;
    const id = tid.toUpperCase().trim();
    if (!id) return;
    if (!config.MODULE_TOKENS) config.MODULE_TOKENS = {};
    if (!config.MODULE_TOKENS[mod]) config.MODULE_TOKENS[mod] = {};
    if (config.MODULE_TOKENS[mod][id]) { alert('Token already exists!'); return; }
    const template = JSON.parse(JSON.stringify(TOKEN_TEMPLATES[mod] || {name:''}));
    config.MODULE_TOKENS[mod][id] = template;
    collectAll();
    renderTokens();
}

function deleteToken(mod, tid) {
    if (!confirm('Delete token ' + tid + '?')) return;
    collectAll();
    delete config.MODULE_TOKENS[mod][tid];
    renderTokens();
}

function addMsg(mod) {
    collectAll();
    if (!config.LOADING_MESSAGES) config.LOADING_MESSAGES = {};
    if (!config.LOADING_MESSAGES[mod]) config.LOADING_MESSAGES[mod] = [];
    config.LOADING_MESSAGES[mod].push('New loading phrase');
    renderMessages();
}

function removeMsg(mod, idx) {
    collectAll();
    config.LOADING_MESSAGES[mod].splice(idx, 1);
    renderMessages();
}

function addBin() {
    collectAll();
    if (!config.BIN_DATABASE) config.BIN_DATABASE = {};
    const prefix = prompt('Enter BIN prefix:');
    if (!prefix) return;
    const brand = prompt('Enter card brand:');
    if (!brand) return;
    config.BIN_DATABASE[prefix.trim()] = brand.trim();
    renderBin();
}

function removeBin(prefix) {
    if (!confirm('Remove BIN entry: ' + prefix + '?')) return;
    collectAll();
    delete config.BIN_DATABASE[prefix];
    renderBin();
}

window.onload = loadConfig;
</script>
</body>
</html>"""



# =====================================================================
# [ REQUEST HANDLER ]
# =====================================================================
class ConfigHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the configuration editor."""

    def log_message(self, format, *args):
        """Override to customize logging."""
        print(f"  [HTTP] {args[0]}")

    def do_GET(self):
        """Handle GET requests."""
        path = urlparse(self.path).path

        if path == "/" or path == "":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))

        elif path == "/api/config":
            config = load_config()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(config, indent=2).encode("utf-8"))

        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode("utf-8"))

    def do_POST(self):
        """Handle POST requests."""
        path = urlparse(self.path).path

        if path == "/api/config":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            try:
                new_config = json.loads(body.decode("utf-8"))
            except json.JSONDecodeError as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"ok": False, "error": f"Invalid JSON: {e}"}).encode("utf-8"))
                return

            ok, err = save_config(new_config)
            if ok:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"ok": True}).encode("utf-8"))
            else:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"ok": False, "error": err}).encode("utf-8"))

        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode("utf-8"))


# =====================================================================
# [ MAIN EXECUTION ]
# =====================================================================
def main():
    """Start the web-based configuration editor."""
    print()
    print("  ╔══════════════════════════════════════════════════╗")
    print("  ║   GPSE Configuration Editor v2.0                ║")
    print("  ║   Web-based settings manager                    ║")
    print("  ╠══════════════════════════════════════════════════╣")
    print("  ║                                                  ║")
    print("  ║   URL: http://localhost:8585                     ║")
    print("  ║                                                  ║")
    print("  ║   Press Ctrl+C to stop the server               ║")
    print("  ╚══════════════════════════════════════════════════╝")
    print()

    server = HTTPServer(("127.0.0.1", PORT), ConfigHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  [*] Server stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
