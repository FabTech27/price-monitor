import logging
import os
import sys
import argparse
from scrapper.scrapper import scrape_products
from processing.transform import clean_data
from database.db import insert_data

def setup_logging():
    """Configuración centralizada de logs."""
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/app.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

def get_valid_pages():
    """Modo Manual: Validación de entrada por terminal."""
    while True:
        try:
            pages = int(input("¿Cuántas páginas quieres scrapear? "))
            if pages > 0:
                return pages
            print("Por favor, ingresa un número mayor a 0.")
        except ValueError:
            print("Entrada inválida. Debes ingresar un número entero.")

def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    # --- 1. CONFIGURACIÓN DE ARGUMENTOS ---
    parser = argparse.ArgumentParser(description="Pipeline de Scraping de Libros")
    parser.add_argument(
        "--pages", 
        type=int, 
        help="Número de páginas a procesar (Modo Automatizado)"
    )
    args = parser.parse_args()

    # --- 2. SELECCIÓN DE MODO (AUTOMÁTICO VS MANUAL) ---
    if args.pages is not None:
        if args.pages > 0:
            pages = args.pages
            logger.info(f"Modo Automatizado: Procesando {pages} páginas desde argumentos.")
        else:
            logger.error("El argumento --pages debe ser mayor a 0. Abortando.")
            return
    else:
        logger.info("Modo Manual: No se detectaron argumentos.")
        pages = get_valid_pages()

    # --- 3. SCRAPING (Extracción) ---
    logger.info(f"Iniciando scraping de {pages} páginas...")
    try:
        def preview_item(name, price):
            logger.info(f"  - {name} | {price}")

        raw_data = scrape_products(pages=pages, on_item=preview_item)
        
        if not raw_data:
            logger.warning("No se encontraron productos. Finalizando ejecución.")
            return

        logger.info(f"Scraping completo — {len(raw_data)} productos obtenidos")
    
    except Exception as e:
        logger.error(f"Fallo crítico en el Scraping: {e}", exc_info=True)
        return

    # --- 4. TRANSFORM (Procesamiento) ---
    logger.info("Iniciando transformación de datos...")
    try:
        clean_df = clean_data(raw_data)
        
        if clean_df is None or clean_df.empty:
            logger.warning("La transformación resultó en un set de datos vacío.")
            return
            
        logger.info(f"Transform completo — {len(clean_df)} filas procesadas")
    
    except Exception as e:
        logger.error(f"Error durante la transformación de datos: {e}", exc_info=True)
        return

    # --- 5. DATABASE (Carga) ---
    logger.info("Iniciando carga en SQL Server...")
    try:
        insert_data(clean_df)
        logger.info("Pipeline finalizado exitosamente.")
    
    except Exception as e:
        logger.error(f"Error al insertar datos en la DB: {e}", exc_info=True)

if __name__ == "__main__":
    main()