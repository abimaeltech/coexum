import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
});

export async function getStatus() {
  const { data } = await api.get<{ status: string }>('/status');
  return data;
}

export async function getNodes() {
  const { data } = await api.get<Array<{
    node_id: string;
    cpu_percent: number;
    memory_percent: number;
    boot_time: number;
  }>>('/nodes');
  return data;
}
