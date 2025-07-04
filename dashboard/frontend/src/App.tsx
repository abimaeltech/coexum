import './App.css'
import Summary from './components/Summary';
import NetworkMap from './components/NetworkMap';

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow p-4">
        <h1 className="text-2xl font-bold">Coexum Live Monitor</h1>
      </header>
      <main className="p-4">
        <Summary />
        <NetworkMap />
      </main>
    </div>
  )
}

export default App
