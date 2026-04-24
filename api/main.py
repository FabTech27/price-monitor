from fastapi import FastAPI, HTTPException, Query
from database.db import fetch_all
from typing import Optional
import logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Price Monitor API",
    description="API para el seguimiento de precios de libros y tendencias."
)

@app.get("/", tags=["General"])
def root():
    return {"message": "API funcionando correctamente"}

@app.get("/productos", tags=["Productos"])
def get_products(order: str = Query("asc", pattern="^(asc|desc|ASC|DESC)$")):
    """
    Lista todos los nombres de productos únicos.
    """
    # Nota: ORDER BY no se puede parametrizar con ?, por eso validamos con pattern en Query
    query = f"""
        SELECT DISTINCT product_name
        FROM price_history
        ORDER BY product_name {order}
    """
    try:
        return fetch_all(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {e}")

@app.get("/precios/{product_name}", tags=["Precios"])
def get_prices(
    product_name: str, 
    limit: int = Query(10, ge=1, le=100), 
    offset: int = Query(0, ge=0)
):
    """
    Obtiene el historial de precios de un producto con paginación.
    """
    query = """
        SELECT product_name, price, rating, date
        FROM price_history
        WHERE product_name = ?
        ORDER BY date DESC
        OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
    """
    try:
        results = fetch_all(query, (product_name, offset, limit))
        if not results:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return results
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")

@app.get("/tendencias", tags=["Análisis"])
def get_trends(
    min_price: float = Query(0, ge=0), 
    max_price: float = Query(1000, ge=0)
):
    """
    Calcula estadísticas por producto dentro de un rango de precio.
    """
    # 1. VALIDACIÓN DE LÓGICA DE NEGOCIO
    if min_price > max_price:
        logger.warning(f"Intento de búsqueda inválido: min={min_price}, max={max_price}")
        raise HTTPException(
            status_code=400, 
            detail="El precio mínimo (min_price) no puede ser mayor que el precio máximo (max_price)"
        )

    # 2. CONSULTA SQL
    query = """
        SELECT 
            product_name,
            AVG(price) as avg_price,
            MIN(price) as min_price,
            MAX(price) as max_price
        FROM price_history
        WHERE price BETWEEN ? AND ?
        GROUP BY product_name
    """
    try:
        results = fetch_all(query, (min_price, max_price))
        return results
    except Exception as e:
        logger.error(f"Error al calcular tendencias: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno al procesar los datos.")