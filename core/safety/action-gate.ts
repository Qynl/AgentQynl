export type AgentAction = { type: 'move' | 'look' | 'click' | 'key' | 'wait'; value?: string; durationMs?: number };

const ALLOWED_KEYS = new Set(['w','a','s','d','space','shift','e','q','1','2','3','4','5','6','7','8','9','0','escape']);

export function validateAction(action: AgentAction): void {
  if (!['move','look','click','key','wait'].includes(action.type)) throw new Error('Action type is not allowlisted.');
  if (action.durationMs !== undefined && (!Number.isFinite(action.durationMs) || action.durationMs < 0 || action.durationMs > 3000)) throw new Error('Action duration outside safe limit.');
  if (action.type === 'key' && action.value && !ALLOWED_KEYS.has(action.value.toLowerCase())) throw new Error('Keyboard key is not allowlisted.');
  if (action.type === 'click' && action.value !== 'left' && action.value !== 'right') throw new Error('Mouse button is not allowlisted.');
}

export class ActionGate {
  constructor(private readonly requireApproval = true) {}
  approve(action: AgentAction): {allowed: boolean; reason: string} {
    validateAction(action);
    if (this.requireApproval && action.type === 'click') return {allowed:false, reason:'Mouse clicks require explicit approval in safe mode.'};
    return {allowed:true, reason:'Allowlisted action.'};
  }
}
