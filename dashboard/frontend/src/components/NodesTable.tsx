import { useEffect, useState } from 'react';
import { getNodes } from './api';

export default function NodesTable() {
  const [nodes, setNodes] = useState<any[]>([]);

  useEffect(() => {
    getNodes().then(setNodes);
  }, []);

  return (
    <div className="bg-white shadow rounded p-4">
      <h2 className="font-semibold mb-2">Detalhes dos Nós</h2>
      <table className="w-full table-auto">
        <thead>
          <tr>
            <th>ID</th>
            <th>CPU (%)</th>
            <th>RAM (%)</th>
            <th>Região</th>
            <th>Uptime</th>
          </tr>
        </thead>
        <tbody>
          {nodes.map(n => (
            <tr key={n.node_id}>
              <td>{n.node_id}</td>
              <td>{n.cpu_percent}</td>
              <td>{n.memory_percent}</td>
              <td>{n.region || '—'}</td>
              <td>{Math.round((Date.now()/1000 - n.boot_time)/3600)}h</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
