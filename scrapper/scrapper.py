from playwright.sync_api import sync_playwright
from datetime import datetime

def scrape_products(pages=1, on_item=None):
    data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for i in range(1, pages + 1):
            url = f"https://books.toscrape.com/catalogue/page-{i}.html"
            page.goto(url)
            page.wait_for_selector("article.product_pod")

            items = page.query_selector_all("article.product_pod")

            for item in items:
                name = item.query_selector("h3 a").get_attribute("title")
                price = item.query_selector(".price_color").inner_text()
                rating_class = item.query_selector("p.star-rating").get_attribute("class")

                data.append({
                    "name": name,
                    "price_raw": price,
                    "rating": rating_class,
                    "date": datetime.now()
                })

                if on_item:
                    on_item(name, price)

        browser.close()

    return data