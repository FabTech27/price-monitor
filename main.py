from scrapper.scrapper import scrape_products
from processing.transform import clean_data
from database.db import insert_data

def main():
    try:
        pages = int(input("¿Cuántas páginas quieres scrapear? "))
        if pages < 1:
            raise ValueError
    except ValueError:
        print("Ingresa un número válido mayor a 0.")
        return

    # --- SCRAPING ---
    print(f"\nIniciando scraping de {pages} páginas...")

    def preview_item(name, price):
        print(f"  - {name} | {price}")

    try:
        raw_data = scrape_products(pages=pages, on_item=preview_item)
        if not raw_data:
            print("No se encontraron productos.")
            return
    except Exception as e:
        print(f"Error durante el scraping: {e}")
        return

    print(f"Scraping completo — {len(raw_data)} productos obtenidos")

    # --- TRANSFORM ---
    print(f"\nTransformando datos...")
    clean_df = clean_data(raw_data)
    print(f"Transform completo — {len(clean_df)} filas procesadas")
    print("\nPreview:")
    print(clean_df.head())


    # --- BASE DE DATOS ---
    insert_data(clean_df)
    print("Datos guardados en SQL Server")

if __name__ == "__main__":
    main()