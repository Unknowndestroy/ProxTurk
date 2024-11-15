import requests
import threading
from colored import fg, attr
import time
import sys

# Lock for not glitches/errors on printing.
print_lock = threading.Lock()

def slow_print(text, delay=0.02):
    with print_lock:
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

def check_proxy(proxy, proxies_list):
    try:
        # Test Link
        url = "http://www.google.com"
        response = requests.get(url, proxies={"http": f"http://{proxy}", "https": f"https://{proxy}"}, timeout=15)
        if response.status_code == 200:
            slow_print(f"{fg(2)}✔️ Correct Proxy:{attr(0)} {fg(4)}{proxy}{attr(0)}", 0.0012)
        else:
            slow_print(f"{fg(1)}❌ Incorrect Proxy:{attr(0)} {fg(4)}{proxy}{attr(0)}, {fg(5)}Proxy removed from proxies.txt{attr(0)}", 0.0009)
            proxies_list.remove(proxy)
    except requests.exceptions.RequestException:
        slow_print(f"{fg(1)}❌ Incorrect Proxy:{attr(0)} {fg(4)}{proxy}{attr(0)}, {fg(5)}Proxy removed from proxies.txt{attr(0)}", 0.0009)
        proxies_list.remove(proxy)

def load_proxies():
    with open('proxies.txt', 'r') as file:
        proxies = file.read().splitlines()
    return proxies

def main():
    proxies = load_proxies()
    slow_print(f"{fg(1)}C{fg(2)}h{fg(3)}e{fg(4)}c{fg(5)}k{fg(6)}i{fg(7)}n{fg(8)}g{fg(9)} {fg(10)}p{fg(11)}r{fg(12)}o{fg(13)}x{fg(14)}i{fg(15)}e{fg(16)}s...{attr(0)}", 0.01)



    # Creating list 
    proxy_list_copy = proxies.copy()

    threads = []
    for proxy in proxy_list_copy:
        t = threading.Thread(target=check_proxy, args=(proxy, proxies))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    slow_print(f"{fg(2)}{attr('bold')}Proxy check completed!{attr(0)}", 0.1)
    slow_print(f"{fg(6)}{attr('bold')}Remaining proxies:{attr(0)} {proxies}", 0.1)

    # Save the remaining proxies to proxies.txt
    with open('proxies.txt', 'w') as file:
        for proxy in proxies:
            file.write(proxy + '\n')

if __name__ == "__main__":
    main()
