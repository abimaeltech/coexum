export default function Header({ status }: { status: string }) {
  return (
    <header className="bg-indigo-600 text-white p-4">
      <h1 className="text-2xl font-bold">Coexum Dashboard</h1>
      <p className="mt-1">Status da rede: <span className="font-semibold">{status}</span></p>
    </header>
  );
}
