import { useEffect, useState } from 'react';
import axios from 'axios';
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid, Legend } from 'recharts';

interface Summary {
  total_nodes: number;
  total_data_mb: number;
  total_data_gb: number;
  avg_speed_mbps: number;
}

export default function Summary() {
  const [data, setData] = useState<Summary|null>(null);
  const [history, setHistory] = useState<Summary[]>([]);

  useEffect(() => {
    // Atualiza a cada 5s para simular dados ao vivo
    const fetchData = async () => {
      const res = await axios.get<Summary>('/network/summary');
      setData(res.data);
      setHistory(h => [...h.slice(-19), res.data]); // mantém últimos 20
    };
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  if (!data) return <p>Carregando resumo...</p>;

  const pieData = [
    { name: 'MB usados', value: data.total_data_mb },
    { name: 'GB usados', value: data.total_data_gb }
  ];

  return (
    <div className="grid grid-cols-2 gap-4 mb-6">
      <div className="p-4 bg-white shadow rounded">
        <h2 className="font-semibold mb-2">Nós ativos</h2>
        <p className="text-3xl">{data.total_nodes}</p>
      </div>
      <div className="p-4 bg-white shadow rounded">
        <h2 className="font-semibold mb-2">Velocidade média</h2>
        <p className="text-3xl">{data.avg_speed_mbps} Mbps</p>
      </div>
      <div className="col-span-2 p-4 bg-white shadow rounded">
        <h2 className="font-semibold mb-2">Consumo de dados</h2>
        <ResponsiveContainer width="100%" height={200}>
          <PieChart>
            <Pie data={pieData} dataKey="value" nameKey="name" innerRadius={50} outerRadius={80}>
              {pieData.map((_, i) => <Cell key={i} fill={i === 0 ? "#60A5FA" : "#34D399"} />)}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="col-span-2 p-4 bg-white shadow rounded">
        <h2 className="font-semibold mb-2">Histórico de Velocidade (Mbps)</h2>
        <ResponsiveContainer width="100%" height={180}>
          <BarChart data={history} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="total_nodes" label={{ value: 'Nós', position: 'insideBottom', offset: -5 }} />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="avg_speed_mbps" fill="#6366F1" name="Velocidade Média" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
