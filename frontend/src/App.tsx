import { useEffect, useState } from 'react'
import './index.css'

interface System {
  operating_system: string
  processor: string
  cpu_percent: number
  memory: { percent: number }
}

interface Storage {
  percent: number
  free_bytes: number
}

interface Network {
  hostname: string
  local_ip: string | null
  interfaces: { name: string }[]
}

const API = 'http://localhost:8000/api'
const formatBytes = (bytes: number) => `${(bytes / 1024 ** 3).toFixed(1)} GB`

export default function App() {
  const [system, setSystem] = useState<System | null>(null)
  const [storage, setStorage] = useState<Storage | null>(null)
  const [network, setNetwork] = useState<Network | null>(null)
  const [error, setError] = useState('')

  const load = async () => {
    try {
      setError('')
      const [sRes, dRes, nRes] = await Promise.all([
        fetch(`${API}/system`),
        fetch(`${API}/storage`),
        fetch(`${API}/network`),
      ])
      if (![sRes, dRes, nRes].every((r) => r.ok)) throw new Error('Backend request failed')
      setSystem(await sRes.json())
      setStorage(await dRes.json())
      setNetwork(await nRes.json())
    } catch {
      setError('Could not connect to the backend. Start FastAPI and try again.')
    }
  }

  useEffect(() => {
    void load()
  }, [])

  return (
    <main>
      <header>
        <p className="eyebrow">TECHNICAL ASSISTANT</p>
        <h1>TechPilot</h1>
        <p>Understand your computer with clear, safe diagnostics.</p>
      </header>
      {error && <div className="error">{error}</div>}
      <section className="grid">
        <article>
          <span>CPU</span>
          <strong>{system ? `${system.cpu_percent}%` : '—'}</strong>
          <small>{system?.processor || 'Loading...'}</small>
        </article>
        <article>
          <span>Memory</span>
          <strong>{system ? `${system.memory.percent}%` : '—'}</strong>
          <small>Used memory</small>
        </article>
        <article>
          <span>Storage</span>
          <strong>{storage ? `${storage.percent}%` : '—'}</strong>
          <small>{storage ? `${formatBytes(storage.free_bytes)} free` : 'Loading...'}</small>
        </article>
        <article>
          <span>Network</span>
          <strong>{network ? 'Online' : '—'}</strong>
          <small>{network?.local_ip || 'Loading...'}</small>
        </article>
      </section>
      <section className="panel">
        <h2>System Health</h2>
        <p>{system?.operating_system || 'Collecting system information...'}</p>
        <button onClick={() => void load()}>Run Diagnostics</button>
      </section>
    </main>
  )
}