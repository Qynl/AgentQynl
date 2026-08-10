export type ProviderConfig = {
  name: 'NVIDIA_NIM' | 'OLLAMA' | 'OPENAI_COMPATIBLE';
  baseUrl: string;
  model: string;
};

export interface VisionProvider {
  plan(input: { imageBase64: string; goal: string; state: Record<string, unknown> }): Promise<{
    reasoning: string;
    actions: Array<{ type: 'move' | 'look' | 'click' | 'key' | 'wait'; value?: string; durationMs?: number }>;
  }>;
}

export function validateProvider(config: ProviderConfig): void {
  if (!config.baseUrl.startsWith('http://') && !config.baseUrl.startsWith('https://')) throw new Error('Provider URL must use HTTP(S).');
  if (!/^[a-zA-Z0-9._:/-]+$/.test(config.model)) throw new Error('Invalid model identifier.');
}
