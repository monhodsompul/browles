import asyncio
import random
import json
import os
from tabulate import tabulate
from pyppeteer import launch

config = json.load(open('./config.json'))

sources = [
  'https://webminer.pages.dev/'
]

# Function to clear the console
def clear_console():
    # Clear console command for Windows and Unix-based systems
    command = "cls" if os.name == "nt" else "clear"
    os.system(command)

def random_source():
    return random.choice(sources)

async def print_progress(msg):
    clear_console()
    
    table = []
    for algo, stats in msg.items():
        table.append([algo, stats['Hashrate'], stats['Shared']])

    print('* Versions:   browlesV1')
    print('* Author:     Rex1024/luckyynr')
    print(' ')
    print(tabulate(table, headers=['Algorithm', 'Hashrate', 'Shared']))

async def main():
    retries = 50
    while retries > 0:
        try:
            browser = await launch({
                "headless": True,
                "args": [
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--ignore-certificate-errors',
                    '--ignore-certificate-errors-spki-list',
                    '--window-position=0,0',
                    '--disable-dev-shm-usage'
                ],
                "ignoreHTTPSErrors": True
            })
            pages = {}
            source = random_source()

            for index, params in enumerate(config):
                query = '&'.join([f"{key}={value}" for key, value in params.items()])
                url = f"{source}?{query}"
                print(f"Browser Restart: {url}")
                page = await browser.newPage()
                await page.goto(url)
                pages[f"{params['algorithm']}_{index}"] = page

            while True:
                msg = {}
                for algo, page in pages.items():
                    try:
                        hashrate = await page.querySelectorEval('#hashrate', 'el => el.innerText')
                        shared = await page.querySelectorEval('#shared', 'el => el.innerText')
                        msg[algo] = {'Hashrate': hashrate or '0 H/s', 'Shared': int(shared) if shared else 0}
                    except Exception as e:
                        print(f"[{retries}] Miner Restart: {e}")
                        retries -= 1
                        break
                await print_progress(msg)
                await asyncio.sleep(6)

        except Exception as e:
            print(f"[{retries}] Miner Restart: {e}")
            retries -= 1

asyncio.get_event_loop().run_until_complete(main())
