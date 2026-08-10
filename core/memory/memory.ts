export type Experience = { id: string; timestamp: number; goal: string; observationSummary: string; action: string; outcome: string; reward: number };

export class MemoryStore {
  private experiences: Experience[] = [];
  add(experience: Experience) { if (this.experiences.length >= 5000) this.experiences.shift(); this.experiences.push(experience); }
  recent(limit = 20) { return this.experiences.slice(-limit); }
  best(limit = 20) { return [...this.experiences].sort((a,b)=>b.reward-a.reward).slice(0,limit); }
}
