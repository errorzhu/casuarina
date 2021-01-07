from pyppeteer import launch
import asyncio
from bs4 import BeautifulSoup


async def main():
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto('https://worldwide.espacenet.com/')
    await page.waitForXPath('//*[@id="application-content"]/div/nav/div/div[2]/div/form/input')
    print("in")
    input_box = await page.querySelector('#application-content > div > nav > div')
    selector = await input_box.querySelector("input")
    await selector.type("A61K38/00")
    button = await input_box.querySelector("div:nth-child(3) > button")

    await button.click()
    await page.waitForXPath('//*[@id="more-options-selector--publication-list-header"]')
    html = await page.content()
    soup = BeautifulSoup(html, 'lxml')
    articles = soup.findAll('article', attrs={'data-qa': 'result_resultList'})
    print(len(articles))
    for article in articles:
        div = article.find('div', attrs={'aria-hidden': True})
        print(div.text)
        # for i,div in enumerate(divs):
        #     print(str(i)+div.text)

    await asyncio.sleep(5)

    # print(html)
    await browser.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
