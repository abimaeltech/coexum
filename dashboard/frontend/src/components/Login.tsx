import { useState } from 'react';
import axios from 'axios';

export default function Login({ onLogin }: { onLogin: () => void }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    try {
      const { data } = await axios.post('/auth/login', { username, password });
      localStorage.setItem('token', data.access_token);
      setError('');
      onLogin();
    } catch {
      setError('Usuário ou senha inválidos');
    }
  }

  return (
    <form onSubmit={handleSubmit} className="max-w-sm mx-auto mt-10 bg-white p-6 rounded shadow">
      <h2 className="text-xl font-bold mb-4">Login</h2>
      <input className="block w-full mb-2 p-2 border rounded" placeholder="Usuário" value={username} onChange={e => setUsername(e.target.value)} />
      <input className="block w-full mb-2 p-2 border rounded" type="password" placeholder="Senha" value={password} onChange={e => setPassword(e.target.value)} />
      {error && <p className="text-red-500">{error}</p>}
      <button className="bg-indigo-600 text-white px-4 py-2 rounded w-full" type="submit">Entrar</button>
    </form>
  );
}
