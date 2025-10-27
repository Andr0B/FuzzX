#!/usr/bin/env python3

import argparse
from pathlib import Path
import requests
import time
from colorama import Fore, Style, init
import csv

init(autoreset=True)

BANNER = r"""
 _        ____ ____  \ /
|_  | |     /	 /    x
|   |_|~   /__  /__  / \
"""

print(BANNER)

DEFAULT_WORDLIST = "/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt"
DEFAULT_DELAY = 0.1
DEFAULT_TIMEOUT = 6.0

parser = argparse.ArgumentParser(description="Webb Fuzzer")
parser.add_argument("-u", "--url", required=True, help="Target Url")
parser.add_argument("-w", "--wordlist",
                    default=DEFAULT_WORDLIST,
                    help="Path to wordlist file")
parser.add_argument("-d", "--delay",
                    type=float,
                    default=DEFAULT_DELAY,
                    help="Min delay between requests (s)")
parser.add_argument("-T", "--timeout",
                    type=float,
                    default=DEFAULT_TIMEOUT,
                    help="Request timeout (s)")
parser.add_argument("-s", "--save", help="Output file name (CSV)")

args = parser.parse_args()

wordlist = args.wordlist
base = args.url.rstrip("/")

if not Path(wordlist).exists():
    print("Wordlist not found:", wordlist)
    print("Tip: pass -w /path/to/wordlist.txt")
    exit(2)

if not base.startswith(("http://", "https://")):
    base = "http://" + base
    print("Note: prepending http:// to URL; pass full scheme to avoid this message.")

session = requests.Session()
out_fh = None
csv_writer = None

print(Fore.LIGHTYELLOW_EX + f"TARGET: {args.url}" + Style.RESET_ALL + "\n")
try:
    if args.save:
        out_fh = open(args.save, "w", encoding="utf-8", errors="ignore", newline="")
        csv_writer = csv.writer(out_fh)
        csv_writer.writerow(["status", "length", "url"])  # header

    with open(wordlist, "r", encoding="utf-8", errors="ignore") as wordlist_file:
        for raw in wordlist_file:
            word = raw.strip()
            if not word:
                continue
            if word.startswith("#"):
                continue
            fragment = word.lstrip("/")
            full_url = f"{base}/{fragment}"
            try:
                response = session.get(full_url, timeout=args.timeout, allow_redirects=True)
                code = response.status_code
                length = len(response.content or b"")

                if 200 <= code < 300:
                    color = Fore.GREEN
                elif 300 <= code < 400:
                    color = Fore.CYAN
                elif 400 <= code < 500:
                    color = Fore.YELLOW
                else:  
                    color = Fore.MAGENTA

                print(color + f"{code:3} " + Style.RESET_ALL + f"{length:6} {full_url}")

                if csv_writer:
                    csv_writer.writerow([code, length, full_url])
                    out_fh.flush()

            except requests.RequestException as e:
                print(f"ERR     ----   {full_url}   ({e})")

            time.sleep(args.delay)

except KeyboardInterrupt:
    print("\nInterrupted by user — exiting.")

except FileNotFoundError:
    print("Wordlist not found:", wordlist)
    exit(2)

finally:
    session.close()
    if out_fh:
        out_fh.close()

