import pandas as pd
import logging

logger = logging.getLogger(__name__)

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

def clean_data(data):
    """
    Transforma los datos crudos en un DataFrame limpio y tipado.
    """
    if not data:
        logger.warning("No hay datos para transformar.")
        return pd.DataFrame()

    try:
        df = pd.DataFrame(data)
        
        # 1. Limpieza de PRECIO
        # Usamos errors='coerce' para que si algo no es convertible a número, ponga NaN en lugar de fallar
        if "price_raw" in df.columns:
            logger.info("Limpiando columna de precios...")
            df["price"] = (
                df["price_raw"]
                .str.replace("£", "", regex=False)
                .str.replace("Â", "", regex=False) # A veces vienen caracteres extraños de encoding
                .str.strip()
            )
            df["price"] = pd.to_numeric(df["price"], errors='coerce')
        else:
            logger.error("No se encontró la columna 'price_raw' en los datos.")

        # 2. Limpieza de RATING
        if "rating" in df.columns:
            logger.info("Mapeando ratings...")
            # Extraemos la última palabra (ej: 'star-rating Three' -> 'Three')
            df["rating_clean"] = df["rating"].str.split().str[-1]
            df["rating_num"] = df["rating_clean"].map(RATING_MAP)
            
            # Si el mapeo falla, podemos asignar un valor por defecto o dejarlo en 0
            df["rating_num"] = df["rating_num"].fillna(0).astype(int)
        
        # 3. MANEJO DE VALORES NULOS (Data Cleaning crítico)
        rows_before = len(df)
        df = df.dropna(subset=["price", "name"]) # Si no tiene nombre o precio, la fila no sirve para BI
        rows_after = len(df)
        
        if rows_before > rows_after:
            logger.warning(f"Se eliminaron {rows_before - rows_after} filas con datos inválidos.")

        # 4. Formateo Final
        # Seleccionamos solo las columnas necesarias y renombramos si es necesario
        df_final = df[["name", "price", "rating_num", "date"]].copy()
        df_final.rename(columns={"rating_num": "rating"}, inplace=True)

        logger.info("Transformación completada exitosamente.")
        return df_final

    except Exception as e:
        logger.error(f"Error crítico en la transformación: {e}", exc_info=True)
        return pd.DataFrame() # Devolvemos un DF vacío para no romper el flujo del main