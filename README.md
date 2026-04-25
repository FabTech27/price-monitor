# Price Monitoring System

Sistema fullstack para monitoreo de precios mediante web scraping, procesamiento de datos y visualización en dashboard interactivo.

---

## Funcionalidades

- Web scraping automatizado
- Procesamiento y limpieza de datos (ETL)
- Almacenamiento en SQL Server
- API REST con FastAPI
- Dashboard interactivo con React + Chart.js
- Alertas de cambios de precio
- Visualización de tendencias

---

## Arquitectura
Scraper → Transform → SQL Server → FastAPI → React Dashboard


---

## Tecnologías

### Backend
- Python
- FastAPI
- SQL Server
- PyODBC
- Pandas

### Frontend
- React
- TailwindCSS
- Chart.js

---

## Cómo ejecutar

### Backend

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload


### Frontend

cd frontend
npm install
npm start