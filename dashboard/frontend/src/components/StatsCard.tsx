type StatsCardProps = {
  totalNodes: number;
  avgCpu: number;
  avgMem: number;
};

export default function StatsCard({ totalNodes, avgCpu, avgMem }: StatsCardProps) {
  return (
    <div className="grid grid-cols-3 gap-4 my-6">
      <div className="bg-white shadow rounded p-4">
        <h2 className="text-sm text-gray-500">Nós ativos</h2>
        <p className="text-2xl font-bold">{totalNodes}</p>
      </div>
      <div className="bg-white shadow rounded p-4">
        <h2 className="text-sm text-gray-500">CPU média (%)</h2>
        <p className="text-2xl font-bold">{avgCpu.toFixed(1)}%</p>
      </div>
      <div className="bg-white shadow rounded p-4">
        <h2 className="text-sm text-gray-500">Memória média (%)</h2>
        <p className="text-2xl font-bold">{avgMem.toFixed(1)}%</p>
      </div>
    </div>
  );
}
