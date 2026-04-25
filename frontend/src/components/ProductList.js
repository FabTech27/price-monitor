import { useEffect, useState } from "react";
import { getProducts } from "../services/api";

export default function ProductList({ onSelect, selected }) {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    getProducts().then(setProducts);
  }, []);

  return (
    <div>
      <h2 className="font-semibold mb-3">Productos</h2>

      <ul className="space-y-2">
        {products.map((p, i) => (
          <li
            key={i}
            onClick={() => onSelect(p.product_name)}
            className={`p-2 rounded cursor-pointer transition ${
              selected === p.product_name
                ? "bg-green-100 text-green-700 font-medium"
                : "hover:bg-gray-100"
            }`}
          >
            {p.product_name}
          </li>
        ))}
      </ul>
    </div>
  );
}