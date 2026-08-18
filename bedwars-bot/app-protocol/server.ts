import { createServer } from 'node:http';
import { WebSocketServer, WebSocket } from 'ws';
import { randomBytes } from 'node:crypto';
import type { ControlMessage, Goal } from './messages';

const HOST = '127.0.0.1';
const PORT = Number(process.env.QYNL_PORT ?? 18791);
const token = randomBytes(24).toString('hex');
let client: WebSocket | null = null;
let lastHeartbeat = 0;
let stopped = true;
let goal: Goal = 'idle';

const http = createServer((req, res) => {
  if (req.url !== '/health') { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': 'application/json' });
  res.end(JSON.stringify({ ok: true, connected: !!client, stopped, goal }));
});

const wss = new WebSocketServer({ server: http, path: '/qynl' });
wss.on('connection', (socket, req) => {
  const auth = new URL(req.url ?? '', `http://${HOST}`).searchParams.get('token');
  if (auth !== token) { socket.close(1008, 'unauthorized'); return; }
  client?.close(4000, 'replaced');
  client = socket;
  stopped = true;
  lastHeartbeat = Date.now();
  socket.on('message', raw => {
    try {
      const m = JSON.parse(raw.toString());
      if (m.type === 'heartbeat') lastHeartbeat = Date.now();
      if (m.type === 'emergency_stop' || m.type === 'manual_takeover') stopped = true;
    } catch { /* malformed telemetry is ignored */ }
  });
  socket.on('close', () => { if (client === socket) client = null; });
});

setInterval(() => {
  if (client && Date.now() - lastHeartbeat > 5000) { stopped = true; client.close(4001, 'heartbeat timeout'); client = null; }
}, 1000).unref();

http.listen(PORT, HOST, () => console.log(`Qynl training IPC: ws://${HOST}:${PORT}/qynl`));
export const setGoal = (next: Goal) => { if (!stopped) goal = next; };
export const emergencyStop = () => { stopped = true; client?.send(JSON.stringify({ type: 'emergency_stop', requestId: randomBytes(8).toString('hex') })); };
export { token, PORT };
