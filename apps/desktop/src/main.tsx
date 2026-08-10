import React, {useState} from 'react';
import {createRoot} from 'react-dom/client';
import './styles.css';

type Provider = 'NVIDIA_NIM' | 'OLLAMA' | 'OPENAI_COMPATIBLE';

function App() {
  const [running, setRunning] = useState(false);
  const [provider, setProvider] = useState<Provider>('NVIDIA_NIM');
  const [safeMode, setSafeMode] = useState(true);
  const [requireApproval, setRequireApproval] = useState(true);

  return <main className="app">
    <header><div><h1>QYNL</h1><span>Computer-use Minecraft agent</span></div><button className={running ? 'danger' : 'primary'} onClick={() => setRunning(!running)}>{running ? 'STOP AGENT' : 'START AGENT'}</button></header>
    <section className="grid">
      <aside className="panel nav"><b>CONTROL</b><button className="active">Dashboard</button><button>Memory</button><button>Learning</button><button>Settings</button><button>Safety</button></aside>
      <section className="panel content">
        <div className="status"><span className={running ? 'dot live' : 'dot'} /> {running ? 'Running' : 'Stopped'} <span className="muted">Minecraft control is {safeMode ? 'sandboxed' : 'restricted'}</span></div>
        <div className="preview"><div className="placeholder">Minecraft capture preview<br/><small>Screen capture will appear here when a game window is selected.</small></div></div>
        <div className="cards"><article><b>Goal</b><p>Survive and progress</p></article><article><b>Provider</b><select value={provider} onChange={e => setProvider(e.target.value as Provider)}><option value="NVIDIA_NIM">NVIDIA NIM</option><option value="OLLAMA">Ollama (local)</option><option value="OPENAI_COMPATIBLE">OpenAI-compatible</option></select></article><article><b>Actions</b><p>Keyboard + mouse only</p></article></div>
      </section>
      <aside className="panel settings"><h2>Safety</h2><label><input type="checkbox" checked={safeMode} onChange={e=>setSafeMode(e.target.checked)}/> Safe mode</label><label><input type="checkbox" checked={requireApproval} onChange={e=>setRequireApproval(e.target.checked)}/> Approve risky actions</label><hr/><h2>Agent</h2><label>Model endpoint<input placeholder="https://..." /></label><label>Model<input placeholder="vision model name" /></label><p className="hint">Credentials are never stored in source code. Tool permissions are allowlisted.</p></aside>
    </section>
  </main>
}

createRoot(document.getElementById('root')!).render(<React.StrictMode><App/></React.StrictMode>);
