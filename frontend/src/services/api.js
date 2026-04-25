const BASE_URL = "http://127.0.0.1:8000";

const handleResponse = async (res) => {
  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || "Error en la petición");
  }
  return res.json();
};

export const getProducts = async () => {
  const res = await fetch(`${BASE_URL}/productos`);
  return handleResponse(res);
};

export const getPrices = async (product) => {
  const res = await fetch(`${BASE_URL}/precios/${encodeURIComponent(product)}?limit=20`);
  return handleResponse(res);
};