import { useEffect, useRef, useState } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import { getNodes } from './api';

type Node = { id: string };
type Link = { source: string; target: string };

export default function NetworkMap() {
  const fgRef = useRef<any>(null); // valor inicial null para evitar erro TS2554
  const [data, setData] = useState<{ nodes: Node[]; links: Link[] }>({ nodes: [], links: [] });

  useEffect(() => {
    (async () => {
      const nodes = await getNodes();
      const nodeList = nodes.map(n => ({ id: n.node_id }));
      // criar links arbitrários para exemplo (ou faça fetch de /topology)
      const links: Link[] = nodeList.flatMap((n, i) =>
        nodeList.slice(i + 1).map(m => ({ source: n.id, target: m.id }))
      );
      setData({ nodes: nodeList, links });
    })();
  }, []);

  return (
    <div className="bg-white shadow rounded h-96">
      <ForceGraph2D
        ref={fgRef}
        graphData={data}
        nodeAutoColorBy="id"
        linkDirectionalParticles={2}
        linkDirectionalParticleSpeed={0.005}
      />
    </div>
  );
}
