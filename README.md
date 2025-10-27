FuzzX — Simple Web Fuzzer

Tiny, no-frills web fuzzer that tries paths from a wordlist against a target URL and prints status codes, response lengths and matched URLs. Optionally saves results to CSV.

Quickstart
# run
python3 fuzzx.py -u https://example.com -w /path/to/wordlist.txt

# save results
python3 fuzzx.py -u https://example.com -w wordlist.txt -s results.csv

Features

Uses a wordlist to probe paths (default: /usr/share/seclists/.../directory-list-2.3-medium.txt)

Colored terminal output for easy scanning (2xx green, 3xx cyan, 4xx yellow, other magenta)

Optional CSV output with status,length,url

Configurable request delay and timeout

Usage (flags)

-u, --url (required) — target URL

-w, --wordlist — path to wordlist (uses built-in default)

-d, --delay — delay between requests (seconds, default 0.1)

-T, --timeout — request timeout (seconds, default 6.0)

-s, --save — output CSV file

Requirements

Python 3

requests, colorama
Install with:

pip install requests colorama
