import { useState } from "react";
import ProductList from "./components/ProductList";
import PriceChart from "./components/PriceChart";
import Alerts from "./components/Alerts";
import { getPrices } from "./services/api";

function App() {
  const [selected, setSelected] = useState(null);
  const [prices, setPrices] = useState([]);

  const handleSelect = async (product) => {
    setSelected(product);
    const data = await getPrices(product);
    setPrices(data);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      
      {/* Header */}
      <h1 className="text-2xl font-bold mb-6 flex items-center gap-2">
        📊 Price Monitor
      </h1>

      <div className="grid grid-cols-4 gap-6">

        {/* Sidebar */}
        <div className="col-span-1 bg-white rounded-xl shadow p-4 overflow-y-auto max-h-[80vh]">
          <ProductList onSelect={handleSelect} selected={selected} />
        </div>

        {/* Main */}
        <div className="col-span-3 bg-white rounded-xl shadow p-6">
          
          {!selected && (
            <p className="text-gray-500">
              Selecciona un producto para ver el análisis
            </p>
          )}

          {selected && (
            <>
              <h2 className="text-xl font-semibold mb-3">
                {selected}
              </h2>

              <Alerts data={prices} />

              <div className="mt-6">
                <PriceChart data={prices} />
              </div>
            </>
          )}
        </div>

      </div>
    </div>
  );
}

export default App;