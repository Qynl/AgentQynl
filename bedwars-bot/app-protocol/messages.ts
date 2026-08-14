export type AgentMode = 'MANUAL' | 'TRAINING' | 'PAUSED' | 'STOPPED';
export type Goal = 'idle' | 'fight' | 'defend' | 'gather' | 'attack_bed' | 'explore' | 'retreat' | 'recover';
export type ControlMessage =
  | { type: 'heartbeat'; requestId: string; timestamp: number }
  | { type: 'goal'; requestId: string; goal: Goal }
  | { type: 'pause'; requestId: string }
  | { type: 'resume'; requestId: string }
  | { type: 'manual_takeover'; requestId: string }
  | { type: 'emergency_stop'; requestId: string };
export const isGoal = (value: unknown): value is Goal => typeof value === 'string' && ['idle','fight','defend','gather','attack_bed','explore','retreat','recover'].includes(value);
export const newRequestId = () => crypto.randomUUID();
