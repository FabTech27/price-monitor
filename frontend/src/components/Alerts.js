export default function Alerts({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="bg-gray-100 p-3 rounded-md">
        ℹ️ No hay datos disponibles
      </div>
    );
  }

  if (data.length < 2) {
    return (
      <div className="bg-gray-100 p-3 rounded-md">
        📊 Solo hay un registro
      </div>
    );
  }

  const latest = data[0];
  const previous = data[1];
  const diff = latest.price - previous.price;

  const base = "p-3 rounded-md font-medium";

  if (diff < 0) {
    return <div className={`${base} bg-green-100 text-green-700`}>📉 Precio bajó</div>;
  }

  if (diff > 0) {
    return <div className={`${base} bg-red-100 text-red-700`}>📈 Precio subió</div>;
  }

  return <div className={`${base} bg-gray-100`}>➖ Precio igual</div>;
}