#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPSE Configuration Editor v1.0
Terminal-based interactive settings editor for config.json
"""

import os
import sys
import json
import copy


# =====================================================================
# [ CONFIGURATION PATH ]
# =====================================================================
try:
    CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
except NameError:
    CONFIG_PATH = os.path.join(os.getcwd(), "config.json")


# =====================================================================
# [ TERMINAL STYLING - ANSI CODES ]
# =====================================================================
class S:
    """ANSI escape codes for terminal styling."""
    H = '\033[95m'; C = '\033[96m'; B = '\033[94m'
    G = '\033[92m'; Y = '\033[93m'; R = '\033[91m'
    W = '\033[97m'; BD = '\033[1m'; DM = '\033[2m'
    UL = '\033[4m'; RST = '\033[0m'; BL = '\033[5m'
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


def header(title, subtitle=None, width=66, color=S.C):
    """Print formatted header box."""
    border = "\u2550" * width
    print(f"\n{color}{S.BD}\u2554{border}\u2557{S.RST}")
    pad = (width - len(title)) // 2
    print(f"{color}{S.BD}\u2551{' ' * pad}{S.W}{S.BD}{title}{color}{' ' * (width - pad - len(title))}\u2551{S.RST}")
    if subtitle:
        pad2 = (width - len(subtitle)) // 2
        print(f"{color}{S.BD}\u2551{' ' * pad2}{S.DM}{subtitle}{color}{S.BD}{' ' * (width - pad2 - len(subtitle))}\u2551{S.RST}")
    print(f"{color}{S.BD}\u255a{border}\u255d{S.RST}")


def sep(width=66, char="\u2500", color=S.DM):
    """Print separator line."""
    print(f"  {color}{char * width}{S.RST}")


def prompt(text, color=S.Y):
    """Display prompt and get input."""
    return input(f"\n  {color}\u25b8 {text}: {S.RST}").strip()


def info(text, prefix="INFO", color=S.C):
    """Display info message."""
    print(f"  {color}[{prefix}]{S.RST} {text}")


def success(text):
    """Display success message."""
    print(f"  {S.G}[\u2713]{S.RST} {text}")


def error(text):
    """Display error message."""
    print(f"  {S.R}[\u2717]{S.RST} {text}")


def wait():
    """Wait for user to press Enter."""
    input(f"\n  {S.DM}Press ENTER to continue...{S.RST}")


def confirm(text):
    """Ask for yes/no confirmation."""
    resp = input(f"\n  {S.Y}\u25b8 {text} (y/n): {S.RST}").strip().lower()
    return resp in ('y', 'yes')


# =====================================================================
# [ CONFIG LOAD / SAVE ]
# =====================================================================
def load_config():
    """Load configuration from config.json."""
    if not os.path.exists(CONFIG_PATH):
        error(f"config.json not found at: {CONFIG_PATH}")
        error("Please run engine.py first to generate the default config.")
        sys.exit(1)

    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        error(f"Invalid JSON in config.json: {e}")
        sys.exit(1)
    except IOError as e:
        error(f"Cannot read config.json: {e}")
        sys.exit(1)

    return config


def save_config(config):
    """Save configuration to config.json with validation."""
    # Validate JSON serialization first
    try:
        json_str = json.dumps(config, indent=2, ensure_ascii=False)
    except (TypeError, ValueError) as e:
        error(f"Configuration contains invalid data: {e}")
        return False

    try:
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            f.write(json_str)
        return True
    except IOError as e:
        error(f"Cannot write config.json: {e}")
        return False


# =====================================================================
# [ MODULE TOKENS EDITOR ]
# =====================================================================
MODULE_NAMES = {
    "protocol_transaction": "Protocol Transaction",
    "interbank": "Interbank Transfer",
    "ip_to_ip": "IP-to-IP Transfer",
    "s2s": "Server-to-Server (S2S)",
    "gpi": "SWIFT GPI",
    "mt103": "MT103 Transfer",
    "rtgs": "RTGS Settlement",
}

MODULE_KEYS = list(MODULE_NAMES.keys())


def edit_module_tokens(config):
    """Edit module tokens section."""
    while True:
        clear()
        header("MODULE TOKENS EDITOR", "Edit access tokens for all 7 modules", color=S.ORANGE)
        print()

        tokens = config.get("MODULE_TOKENS", {})

        for i, key in enumerate(MODULE_KEYS, 1):
            mod_tokens = tokens.get(key, {})
            count = len(mod_tokens)
            color = S.ORANGE if i <= 1 else S.C if i <= 2 else S.TEAL if i <= 3 else S.PURPLE if i <= 4 else S.GOLD if i <= 5 else S.B if i <= 6 else S.G
            print(f"  {color}{S.BD} [{i}]{S.RST}  {S.W}{S.BD}{MODULE_NAMES[key]}{S.RST}")
            print(f"        {S.DM}{count} token(s) configured{S.RST}\n")

        print(f"  {S.R}{S.BD} [0]{S.RST}  {S.DM}Back to Main Menu{S.RST}")
        sep()

        choice = prompt("Select module [0-7]")

        if choice == "0":
            return
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(MODULE_KEYS):
                edit_module_token_detail(config, MODULE_KEYS[idx])
        except ValueError:
            pass


def edit_module_token_detail(config, module_key):
    """Edit tokens for a specific module."""
    while True:
        clear()
        header(f"TOKENS: {MODULE_NAMES[module_key].upper()}", color=S.ORANGE)
        print()

        tokens = config.get("MODULE_TOKENS", {}).get(module_key, {})

        if not tokens:
            info("No tokens configured for this module.", prefix="EMPTY")
        else:
            print(f"  {S.W}{S.BD}  {'#':<4}{'TOKEN ID':<12}{'NAME':<25}{'FIELDS'}{S.RST}")
            sep(60)
            for i, (token_id, data) in enumerate(tokens.items(), 1):
                name = data.get("name", "N/A")
                fields = len(data)
                print(f"  {S.C}  {i:<4}{S.W}{token_id:<12}{name:<25}{S.DM}{fields} fields{S.RST}")

        print()
        sep()
        print(f"\n  {S.DM}  [#] Select token number to edit")
        print(f"  {S.DM}  [A] Add new token")
        print(f"  {S.DM}  [D] Delete a token")
        print(f"  {S.DM}  [0] Back{S.RST}")

        choice = prompt("Action").upper()

        if choice == "0":
            return
        elif choice == "A":
            add_token(config, module_key)
        elif choice == "D":
            delete_token(config, module_key)
        else:
            try:
                idx = int(choice) - 1
                token_ids = list(tokens.keys())
                if 0 <= idx < len(token_ids):
                    edit_token_fields(config, module_key, token_ids[idx])
            except ValueError:
                pass


def edit_token_fields(config, module_key, token_id):
    """Edit individual fields of a token."""
    while True:
        clear()
        header(f"TOKEN: {token_id} ({MODULE_NAMES[module_key]})", color=S.TEAL)
        print()

        data = config["MODULE_TOKENS"][module_key][token_id]

        print(f"  {S.W}{S.BD}  {'#':<4}{'FIELD':<25}{'VALUE'}{S.RST}")
        sep(60)
        fields = list(data.items())
        for i, (field, value) in enumerate(fields, 1):
            val_str = str(value) if value is not None else "(null)"
            print(f"  {S.C}  {i:<4}{S.W}{field:<25}{S.DM}{val_str}{S.RST}")

        print()
        sep()
        print(f"\n  {S.DM}  [#] Select field number to edit")
        print(f"  {S.DM}  [A] Add new field")
        print(f"  {S.DM}  [R] Remove a field")
        print(f"  {S.DM}  [0] Back{S.RST}")

        choice = prompt("Action").upper()

        if choice == "0":
            return
        elif choice == "A":
            field_name = prompt("New field name")
            if field_name:
                field_value = prompt(f"Value for '{field_name}' (leave empty for null)")
                if field_value == "":
                    config["MODULE_TOKENS"][module_key][token_id][field_name] = None
                else:
                    config["MODULE_TOKENS"][module_key][token_id][field_name] = field_value
                success(f"Field '{field_name}' added.")
                wait()
        elif choice == "R":
            field_num = prompt("Field number to remove")
            try:
                fidx = int(field_num) - 1
                if 0 <= fidx < len(fields):
                    fname = fields[fidx][0]
                    if confirm(f"Remove field '{fname}'?"):
                        del config["MODULE_TOKENS"][module_key][token_id][fname]
                        success(f"Field '{fname}' removed.")
                    wait()
            except ValueError:
                pass
        else:
            try:
                fidx = int(choice) - 1
                if 0 <= fidx < len(fields):
                    fname = fields[fidx][0]
                    fval = fields[fidx][1]
                    print(f"\n  {S.DM}Current value: {fval}{S.RST}")
                    new_val = prompt(f"New value for '{fname}' (empty for null)")
                    if new_val == "":
                        config["MODULE_TOKENS"][module_key][token_id][fname] = None
                    else:
                        config["MODULE_TOKENS"][module_key][token_id][fname] = new_val
                    success(f"Field '{fname}' updated.")
                    wait()
            except ValueError:
                pass


def add_token(config, module_key):
    """Add a new token to a module."""
    print()
    token_id = prompt("New Token ID (e.g. ABC12)")
    if not token_id:
        return

    token_id = token_id.upper()
    if token_id in config["MODULE_TOKENS"].get(module_key, {}):
        error(f"Token '{token_id}' already exists.")
        wait()
        return

    name = prompt("Token name")
    if not name:
        return

    if module_key not in config["MODULE_TOKENS"]:
        config["MODULE_TOKENS"][module_key] = {}

    config["MODULE_TOKENS"][module_key][token_id] = {"name": name.upper()}
    success(f"Token '{token_id}' created with name '{name.upper()}'.")
    info("Use the token editor to add more fields.")
    wait()


def delete_token(config, module_key):
    """Delete a token from a module."""
    tokens = config["MODULE_TOKENS"].get(module_key, {})
    if not tokens:
        error("No tokens to delete.")
        wait()
        return

    token_num = prompt("Token number to delete")
    try:
        idx = int(token_num) - 1
        token_ids = list(tokens.keys())
        if 0 <= idx < len(token_ids):
            tid = token_ids[idx]
            if confirm(f"Delete token '{tid}'?"):
                del config["MODULE_TOKENS"][module_key][tid]
                success(f"Token '{tid}' deleted.")
        else:
            error("Invalid token number.")
    except ValueError:
        error("Invalid input.")
    wait()


# =====================================================================
# [ RESULT CONFIGURATION EDITOR ]
# =====================================================================
VALID_STATUSES = ["SUCCESS", "FAILED", "PENDING"]


def edit_result_config(config):
    """Edit result configuration (status per module)."""
    while True:
        clear()
        header("RESULT CONFIGURATION", "Set outcome status per module", color=S.G)
        print()

        result_cfg = config.get("RESULT_CONFIG", {})
        result_msg = config.get("RESULT_MESSAGE", {})

        print(f"  {S.W}{S.BD}  {'#':<4}{'MODULE':<28}{'STATUS':<14}{'CUSTOM MESSAGE'}{S.RST}")
        sep(66)

        for i, key in enumerate(MODULE_KEYS, 1):
            status = result_cfg.get(key, "SUCCESS")
            msg = result_msg.get(key, "")
            status_color = S.G if status == "SUCCESS" else S.R if status == "FAILED" else S.Y
            print(f"  {S.C}  {i:<4}{S.W}{MODULE_NAMES[key]:<28}{status_color}{S.BD}{status:<14}{S.DM}{msg or '(none)'}{S.RST}")

        print()
        sep()
        print(f"\n  {S.DM}  [#] Select module to change status")
        print(f"  {S.DM}  [M] Edit custom messages")
        print(f"  {S.DM}  [0] Back{S.RST}")

        choice = prompt("Action").upper()

        if choice == "0":
            return
        elif choice == "M":
            edit_result_messages(config)
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(MODULE_KEYS):
                    key = MODULE_KEYS[idx]
                    current = result_cfg.get(key, "SUCCESS")
                    print(f"\n  {S.DM}Current status: {current}{S.RST}")
                    print(f"  {S.DM}Options: SUCCESS / FAILED / PENDING{S.RST}")
                    new_status = prompt("New status").upper()
                    if new_status in VALID_STATUSES:
                        config["RESULT_CONFIG"][key] = new_status
                        success(f"{MODULE_NAMES[key]} set to {new_status}.")
                    else:
                        error("Invalid status. Must be SUCCESS, FAILED, or PENDING.")
                    wait()
            except ValueError:
                pass


def edit_result_messages(config):
    """Edit custom result messages."""
    while True:
        clear()
        header("RESULT MESSAGES", "Custom messages shown on module completion", color=S.G)
        print()

        result_msg = config.get("RESULT_MESSAGE", {})

        for i, key in enumerate(MODULE_KEYS, 1):
            msg = result_msg.get(key, "")
            print(f"  {S.C}  [{i}]{S.RST} {S.W}{MODULE_NAMES[key]}{S.RST}")
            print(f"       {S.DM}{msg or '(no custom message)'}{S.RST}\n")

        print(f"  {S.R}  [0]{S.RST} {S.DM}Back{S.RST}")
        sep()

        choice = prompt("Select module to edit message [0-7]")

        if choice == "0":
            return
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(MODULE_KEYS):
                key = MODULE_KEYS[idx]
                current = result_msg.get(key, "")
                print(f"\n  {S.DM}Current: {current or '(empty)'}{S.RST}")
                new_msg = prompt("New message (leave empty to clear)")
                config["RESULT_MESSAGE"][key] = new_msg
                success("Message updated.")
                wait()
        except ValueError:
            pass


# =====================================================================
# [ TIMING EDITOR ]
# =====================================================================
TIMING_DESCRIPTIONS = {
    "boot_progress": "Boot sequence progress bar duration (seconds)",
    "auth_connect": "Authentication connection delay",
    "auth_verify": "Credential verification delay",
    "auth_2fa": "Two-factor auth step delay",
    "auth_session_key": "Session key generation progress",
    "net_hop_duration": "Network hop simulation delay",
    "net_ecdhe": "ECDHE key exchange duration",
    "net_forward_secrecy": "Forward secrecy setup",
    "net_alliance": "Alliance network connection",
    "net_tunnel_progress": "Tunnel establishment progress",
    "scan_probe_duration": "Port scan probe duration",
    "scan_batch_duration": "Batch scan duration",
    "decrypt_layer_duration": "Decryption layer duration",
    "routing_validate": "Route validation time",
    "routing_aml": "AML compliance check",
    "routing_correspondent": "Correspondent bank routing",
    "bridge_ping": "Bridge node ping",
    "bridge_escrow_progress": "Escrow progress bar",
    "bridge_sync_progress": "Sync progress bar",
    "settlement_duration": "Final settlement duration",
}


def edit_timing(config):
    """Edit timing configuration."""
    while True:
        clear()
        header("TIMING SETTINGS", "All delays and durations (in seconds)", color=S.PURPLE)
        print()

        timing = config.get("TIMING", {})

        print(f"  {S.W}{S.BD}  {'#':<4}{'SETTING':<28}{'VALUE':<10}{'DESCRIPTION'}{S.RST}")
        sep(70)

        keys = list(timing.keys())
        for i, key in enumerate(keys, 1):
            val = timing[key]
            desc = TIMING_DESCRIPTIONS.get(key, "")
            print(f"  {S.C}  {i:<4}{S.W}{key:<28}{S.GOLD}{str(val):<10}{S.DM}{desc}{S.RST}")

        print()
        sep()
        print(f"\n  {S.DM}  [#] Select setting number to edit")
        print(f"  {S.DM}  [0] Back{S.RST}")

        choice = prompt("Action")

        if choice == "0":
            return
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(keys):
                key = keys[idx]
                current = timing[key]
                desc = TIMING_DESCRIPTIONS.get(key, "")
                print(f"\n  {S.DM}{desc}{S.RST}")
                print(f"  {S.DM}Current value: {current}{S.RST}")
                new_val = prompt(f"New value for '{key}' (positive number)")
                try:
                    num = float(new_val)
                    if num <= 0:
                        error("Value must be a positive number.")
                    else:
                        config["TIMING"][key] = num
                        success(f"'{key}' set to {num}.")
                except ValueError:
                    error("Invalid number.")
                wait()
        except ValueError:
            pass


# =====================================================================
# [ LOADING MESSAGES EDITOR ]
# =====================================================================
def edit_loading(config):
    """Edit loading messages and duration."""
    while True:
        clear()
        header("LOADING MESSAGES & DURATION", "Per-module loading phrases and timing", color=S.GOLD)
        print()

        messages = config.get("LOADING_MESSAGES", {})
        duration = config.get("LOADING_DURATION", {})

        for i, key in enumerate(MODULE_KEYS, 1):
            phrases = messages.get(key, [])
            dur = duration.get(key, 2.0)
            color = S.ORANGE if i <= 1 else S.C if i <= 2 else S.TEAL if i <= 3 else S.PURPLE if i <= 4 else S.GOLD if i <= 5 else S.B if i <= 6 else S.G
            print(f"  {color}{S.BD} [{i}]{S.RST}  {S.W}{S.BD}{MODULE_NAMES[key]}{S.RST}")
            print(f"        {S.DM}{len(phrases)} phrases | Duration: {dur}s{S.RST}\n")

        print(f"  {S.R}{S.BD} [0]{S.RST}  {S.DM}Back to Main Menu{S.RST}")
        sep()

        choice = prompt("Select module [0-7]")

        if choice == "0":
            return
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(MODULE_KEYS):
                edit_loading_detail(config, MODULE_KEYS[idx])
        except ValueError:
            pass


def edit_loading_detail(config, module_key):
    """Edit loading phrases for a specific module."""
    while True:
        clear()
        header(f"LOADING: {MODULE_NAMES[module_key].upper()}", color=S.GOLD)
        print()

        messages = config.get("LOADING_MESSAGES", {}).get(module_key, [])
        duration = config.get("LOADING_DURATION", {}).get(module_key, 2.0)

        print(f"  {S.W}{S.BD}  Duration: {S.GOLD}{duration}s{S.RST}")
        print()

        if not messages:
            info("No loading phrases configured.", prefix="EMPTY")
        else:
            print(f"  {S.W}{S.BD}  Loading Phrases:{S.RST}")
            sep(50)
            for i, msg in enumerate(messages, 1):
                print(f"  {S.C}  [{i:2d}]{S.RST} {S.DM}{msg}{S.RST}")

        print()
        sep()
        print(f"\n  {S.DM}  [#] Select phrase to edit")
        print(f"  {S.DM}  [A] Add new phrase")
        print(f"  {S.DM}  [R] Remove a phrase")
        print(f"  {S.DM}  [T] Set duration")
        print(f"  {S.DM}  [P] Preview loading animation")
        print(f"  {S.DM}  [0] Back{S.RST}")

        choice = prompt("Action").upper()

        if choice == "0":
            return
        elif choice == "A":
            new_phrase = prompt("New loading phrase")
            if new_phrase:
                if module_key not in config.get("LOADING_MESSAGES", {}):
                    config["LOADING_MESSAGES"][module_key] = []
                config["LOADING_MESSAGES"][module_key].append(new_phrase)
                success(f"Phrase added: '{new_phrase}'")
                wait()
        elif choice == "R":
            if not messages:
                error("No phrases to remove.")
                wait()
                continue
            num = prompt("Phrase number to remove")
            try:
                pidx = int(num) - 1
                if 0 <= pidx < len(messages):
                    removed = config["LOADING_MESSAGES"][module_key].pop(pidx)
                    success(f"Removed: '{removed}'")
                else:
                    error("Invalid phrase number.")
            except ValueError:
                error("Invalid input.")
            wait()
        elif choice == "T":
            print(f"\n  {S.DM}Current duration: {duration}s{S.RST}")
            new_dur = prompt("New duration (positive number, in seconds)")
            try:
                d = float(new_dur)
                if d <= 0:
                    error("Duration must be positive.")
                else:
                    config["LOADING_DURATION"][module_key] = d
                    success(f"Duration set to {d}s.")
            except ValueError:
                error("Invalid number.")
            wait()
        elif choice == "P":
            # Preview loading animation
            print(f"\n  {S.DM}Preview (showing phrases in sequence):{S.RST}\n")
            import time
            if messages:
                per_msg = duration / len(messages) if messages else 1
                for msg in messages:
                    print(f"  {S.C}[*]{S.RST} {msg}...")
                    time.sleep(min(per_msg, 0.5))
            else:
                info("No phrases to preview.")
            print(f"\n  {S.G}[Done]{S.RST} Total duration would be: {duration}s")
            wait()
        else:
            try:
                pidx = int(choice) - 1
                if 0 <= pidx < len(messages):
                    print(f"\n  {S.DM}Current: {messages[pidx]}{S.RST}")
                    new_text = prompt("New text (leave empty to cancel)")
                    if new_text:
                        config["LOADING_MESSAGES"][module_key][pidx] = new_text
                        success("Phrase updated.")
                    wait()
            except ValueError:
                pass


# =====================================================================
# [ MAIN MENU ]
# =====================================================================
def main_menu(config):
    """Display the main editor menu."""
    clear()
    header("GPSE CONFIGURATION EDITOR", "Terminal-based settings manager v1.0", color=S.C)
    print()

    menu_items = [
        ("1", "Module Tokens", "Edit access tokens for all 7 systems", S.ORANGE),
        ("2", "Result Configuration", "Set SUCCESS/FAILED/PENDING per module", S.G),
        ("3", "Result Messages", "Custom messages on module completion", S.TEAL),
        ("4", "Timing Settings", "All delays and duration values", S.PURPLE),
        ("5", "Loading Messages", "Per-module loading phrases & duration", S.GOLD),
    ]

    for num, name, desc, color in menu_items:
        print(f"  {color}{S.BD} [{num}]{S.RST}  {S.W}{S.BD}{name}{S.RST}")
        print(f"        {S.DM}{desc}{S.RST}\n")

    print(f"  {S.G}{S.BD} [6]{S.RST}  {S.W}{S.BD}Save & Exit{S.RST}")
    print(f"        {S.DM}Write changes to config.json and exit{S.RST}\n")
    print(f"  {S.R}{S.BD} [0]{S.RST}  {S.DM}Exit Without Saving{S.RST}\n")
    sep()

    choice = prompt("Select option [0-6]")
    return choice


# =====================================================================
# [ MAIN EXECUTION ]
# =====================================================================
def main():
    """Main editor entry point."""
    S.init()

    config = load_config()
    original = json.dumps(config, sort_keys=True)

    while True:
        choice = main_menu(config)

        if choice == "0":
            current = json.dumps(config, sort_keys=True)
            if current != original:
                if confirm("You have unsaved changes. Exit anyway?"):
                    clear()
                    info("Exited without saving.", prefix="EXIT")
                    print()
                    break
                else:
                    continue
            clear()
            info("No changes made. Exiting.", prefix="EXIT")
            print()
            break
        elif choice == "1":
            edit_module_tokens(config)
        elif choice == "2":
            edit_result_config(config)
        elif choice == "3":
            edit_result_messages(config)
        elif choice == "4":
            edit_timing(config)
        elif choice == "5":
            edit_loading(config)
        elif choice == "6":
            # Save & Exit
            clear()
            header("SAVE CONFIGURATION", color=S.G)
            print()
            info("Validating JSON structure...")

            try:
                json.dumps(config, indent=2, ensure_ascii=False)
                success("JSON validation passed.")
            except (TypeError, ValueError) as e:
                error(f"JSON validation failed: {e}")
                error("Cannot save. Please fix the configuration.")
                wait()
                continue

            print()
            if confirm("Write changes to config.json?"):
                if save_config(config):
                    success("Configuration saved successfully!")
                    print(f"\n  {S.DM}  File: {CONFIG_PATH}{S.RST}")
                else:
                    error("Failed to save configuration.")
                wait()
                break
        else:
            error("Invalid selection.")
            import time
            time.sleep(0.5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {S.R}[!] Editor terminated.{S.RST}")
        print(f"  {S.DM}Changes were NOT saved.{S.RST}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n  {S.R}[ERROR] {e}{S.RST}\n")
        sys.exit(1)
