import logging
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# Obtenemos el logger configurado en el main
logger = logging.getLogger(__name__)

def scrape_products(pages=1, on_item=None):
    """
    Realiza el scraping de productos con manejo de errores granular.
    """
    data = []

    try:
        with sync_playwright() as p:
            logger.info("Lanzando navegador Chromium...")
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
            page = context.new_page()

            for i in range(1, pages + 1):
                url = f"https://books.toscrape.com/catalogue/page-{i}.html"
                
                try:
                    logger.info(f"Accediendo a: {url}")
                    # Timeout de 30s para evitar esperas infinitas
                    page.goto(url, timeout=30000, wait_until="domcontentloaded")
                    page.wait_for_selector("article.product_pod", timeout=10000)

                    items = page.query_selector_all("article.product_pod")
                    
                    for item in items:
                        try:
                            # Extracción individual con manejo de errores
                            name_el = item.query_selector("h3 a")
                            price_el = item.query_selector(".price_color")
                            rating_el = item.query_selector("p.star-rating")

                            if not name_el or not price_el:
                                continue

                            name = name_el.get_attribute("title")
                            price = price_el.inner_text()
                            rating_class = rating_el.get_attribute("class") if rating_el else "No Rating"

                            product = {
                                "name": name,
                                "price_raw": price,
                                "rating": rating_class,
                                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }

                            data.append(product)

                            if on_item:
                                on_item(name, price)

                        except Exception as item_err:
                            logger.warning(f"Error procesando un producto individual: {item_err}")
                            continue # Salta al siguiente producto si este falla

                except PlaywrightTimeout:
                    logger.error(f"Timeout agotado en la página {i}. Saltando a la siguiente...")
                except Exception as page_err:
                    logger.error(f"Error inesperado en la página {i}: {page_err}")

            browser.close()
            logger.info("Navegador cerrado correctamente.")

    except Exception as e:
        logger.error(f"Fallo crítico en el motor de scraping: {e}", exc_info=True)
        # No levantamos el error para que el main pueda manejar la lista vacía
    
    return data