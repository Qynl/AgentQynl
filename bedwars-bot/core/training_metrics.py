"""Local training metrics for private BedWars bot evaluation."""
from dataclasses import dataclass

@dataclass
class FightMetrics:
    hits:int=0; misses:int=0; damage_dealt:float=0; damage_taken:float=0
    longest_combo:int=0; deaths:int=0; objectives:int=0; disengages:int=0

    def register_hit(self, damage:float, combo:int):
        self.hits+=1; self.damage_dealt+=max(0.0,damage); self.longest_combo=max(self.longest_combo,combo)
    def register_miss(self): self.misses+=1
    def register_damage_taken(self, damage:float): self.damage_taken+=max(0.0,damage)
    def register_death(self): self.deaths+=1
    def register_objective(self): self.objectives+=1
    def register_disengage(self): self.disengages+=1

    @property
    def accuracy(self):
        total=self.hits+self.misses
        return self.hits/total if total else 0.0

    def snapshot(self):
        return {"hits":self.hits,"misses":self.misses,"accuracy":round(self.accuracy,4),"damage_dealt":self.damage_dealt,"damage_taken":self.damage_taken,"longest_combo":self.longest_combo,"deaths":self.deaths,"objectives":self.objectives,"disengages":self.disengages}
