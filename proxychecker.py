import requests
import threading
import time
import sys
import logging
from colored import fg, attr
from queue import Queue
from concurrent.futures import ThreadPoolExecutor

# Setup logging
logging.basicConfig(filename='proxy_check.log', level=logging.ERROR)

# Lock for printing without glitches/errors.
print_lock = threading.Lock()

def slow_print(text, delay=0.02):
with print_lock:
for char in text:
sys.stdout.write(char)
sys.stdout.flush()
time.sleep(delay)
print()

def check_proxy(proxy, output_queue):
try:
url = "http://www.google.com"
response = requests.get(url, proxies={"http": f"http://{proxy}", "https": f"https://{proxy}"}, timeout=10)
if response.status_code == 200:
slow_print(f"{fg(2)}✔️ Correct Proxy:{attr(0)} {fg(4)}{proxy}{attr(0)}", 0.0012)
output_queue.put(proxy) # Add valid proxy to queue
else:
slow_print(f"{fg(1)}❌ Incorrect Proxy:{attr(0)} {fg(4)}{proxy}{attr(0)}, {fg(5)}Proxy removed from proxies.txt{attr(0)}", 0.0009)
except requests.exceptions.RequestException as e:
logging.error(f"Proxy check failed for {proxy}: {e}")
slow_print(f"{fg(1)}❌ Incorrect Proxy:{attr(0)} {fg(4)}{proxy}{attr(0)}, {fg(5)}Proxy removed from proxies.txt{attr(0)}", 0.0009)

def load_proxies():
with open('proxies.txt', 'r') as file:
proxies = file.read().splitlines()
return proxies

def main():
proxies = load_proxies()
slow_print(f"{fg(1)}C{fg(2)}h{fg(3)}e{fg(4)}c{fg(5)}k{fg(6)}i{fg(7)}n{fg(8)}g{fg(9)} {fg(10)}p{fg(11)}r{fg(12)}o{fg(13)}x{fg(14)}i{fg(15)}e{fg(16)}s...{attr(0)}", 0.01)

# Queue for thread-safe collection of valid proxies
proxy_queue = Queue()

# Use ThreadPoolExecutor for better thread management
with ThreadPoolExecutor(max_workers=20) as executor:
executor.map(lambda proxy: check_proxy(proxy, proxy_queue), proxies)

# Collect valid proxies from the queue
valid_proxies = []
while not proxy_queue.empty():
valid_proxies.append(proxy_queue.get())

slow_print(f"{fg(2)}{attr('bold')}Proxy check completed!{attr(0)}", 0.1)
slow_print(f"{fg(6)}{attr('bold')}Remaining proxies:{attr(0)} {valid_proxies}", 0.1)

# Save the remaining proxies to proxies.txt
with open('proxies.txt', 'w') as file:
for proxy in valid_proxies:
file.write(proxy + 'n')

if __name__ == "__main__":
main()