import requests
import time
import csv
import argparse
from datetime import datetime
from colorama import init, Fore

init(autoreset=True)

LOG_FILE = "uptime_log.txt"
ERROR_FILE = "error_log.txt"
RETRIES = 2
TIMEOUT = 10

def log_to_file(message, file=LOG_FILE):
    with open(file, "a", encoding='utf-8') as f:
        f.write(message + "\n")

def check_website(url):
    attempt = 0
    while attempt <= RETRIES:
        try:
            start = time.time()
            response = requests.get(url, timeout=TIMEOUT)
            duration = round(time.time() - start, 2)

            if response.status_code == 200:
                msg = f"{Fore.GREEN}[{datetime.now()}] {url} is UP ✅ | {duration}s"
            else:
                msg = f"{Fore.YELLOW}[{datetime.now()}] {url} responded with status {response.status_code} ⚠️"

            print(msg)
            log_to_file(msg)
            return

        except requests.exceptions.RequestException as e:
            error_msg = f"{Fore.RED}[{datetime.now()}] {url} DOWN ❌ | Error: {str(e)}"
            print(error_msg)
            log_to_file(error_msg, ERROR_FILE)
            attempt += 1
            if attempt > RETRIES:
                log_to_file(f"Failed after {RETRIES} retries: {url}", ERROR_FILE)

def read_urls_from_csv(file_path):
    urls = []
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    urls.append(row[0].strip())
    except FileNotFoundError:
        print(Fore.RED + f"CSV file '{file_path}' not found.")
    return urls

def main():
    parser = argparse.ArgumentParser(description="Advanced Website Uptime Checker")
    parser.add_argument('-u', '--url', type=str, help="Single URL to check")
    parser.add_argument('-f', '--file', type=str, help="CSV file containing URLs")
    args = parser.parse_args()

    log_to_file(f"\n--- Website Check Started at {datetime.now()} ---")

    if args.url:
        check_website(args.url)

    elif args.file:
        urls = read_urls_from_csv(args.file)
        if urls:
            for url in urls:
                check_website(url)
        else:
            print(Fore.RED + "No valid URLs found in file.")
    else:
        print(Fore.YELLOW + "No URL or file provided. Use -u or -f option.")

    print(Fore.CYAN + "\n✅ Check complete. Logs saved in 'uptime_log.txt' and 'error_log.txt'.")

if __name__ == "__main__":
    main()
  
