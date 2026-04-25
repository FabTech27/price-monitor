import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement);

export default function PriceChart({ data }) {
  if (!data || data.length === 0) return <p>No data</p>;

  const chartData = {
    labels: data.map(d =>
      new Date(d.date).toLocaleDateString()
    ),
    datasets: [
      {
        label: "Precio",
        data: data.map(d => d.price),
        borderColor: "#4CAF50",
        backgroundColor: "rgba(76, 175, 80, 0.2)",
        tension: 0.3,
        fill: true,
        pointRadius: 4
      }
    ]
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        display: true,
      },
    },
    scales: {
      y: {
        beginAtZero: false,
      },
    },
  };

  return <Line data={chartData} options={options} />;
}