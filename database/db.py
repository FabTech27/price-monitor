import pyodbc
import logging

logger = logging.getLogger(__name__)

def get_connection():
    """Establece la conexión con manejo de errores básico."""
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost;"
            "DATABASE=PriceMonitor;"
            "Trusted_Connection=yes;"
        )
        return conn
    except Exception as e:
        logger.error(f"Error al conectar a SQL Server: {e}")
        raise # Re-lanzamos el error para que el main sepa que no hubo conexión

def insert_data(df):
    """Inserta datos de forma masiva y eficiente."""
    if df.empty:
        return

    conn = get_connection()
    cursor = conn.cursor()
    # OPTIMIZACIÓN CLAVE: fast_executemany acelera la inserción de miles de filas
    cursor.fast_executemany = True

    try:
        # Preparamos los datos como una lista de tuplas (lo que espera executemany)
        values = [tuple(x) for x in df.to_numpy()]
        
        query = """
            INSERT INTO price_history (product_name, price, rating, date)
            VALUES (?, ?, ?, ?)
        """
        
        cursor.executemany(query, values)
        conn.commit()
        logger.info(f"Éxito: {len(df)} filas insertadas en la base de datos.")
        
    except Exception as e:
        conn.rollback() # Si algo falla, deshacemos los cambios
        logger.error(f"Error durante la inserción masiva: {e}", exc_info=True)
    finally:
        cursor.close()
        conn.close()

def fetch_all(query, params=None):
    """Consulta datos asegurando el cierre de la conexión."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return results

    except Exception as e:
        logger.error(f"Error al ejecutar consulta: {e}")
        return []
    finally:
        cursor.close()
        conn.close()