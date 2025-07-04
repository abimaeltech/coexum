import { useEffect, useState } from 'react';
import { getNodes } from './api';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export default function UsersByRegion() {
  const [data, setData] = useState<{ region: string, count: number }[]>([]);

  useEffect(() => {
    getNodes().then(nodes => {
      const regionCount: Record<string, number> = {};
      nodes.forEach(n => {
        // Corrige para aceitar region opcional
        const region = (n as any).region || 'Desconhecida';
        regionCount[region] = (regionCount[region] || 0) + 1;
      });
      setData(Object.entries(regionCount).map(([region, count]) => ({ region, count })));
    });
  }, []);

  return (
    <div className="bg-white shadow rounded p-4 mb-6">
      <h2 className="font-semibold mb-2">Usuários por Região</h2>
      <ResponsiveContainer width="100%" height={200}>
        <BarChart data={data}>
          <XAxis dataKey="region" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="count" fill="#6366F1" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
