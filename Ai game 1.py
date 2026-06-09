# Example: "Universal Gardener Lite"
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class AIGardener:
    def __init__(self):
        # Simple cellular automata garden
        self.garden = np.random.choice([0, 1], size=(100, 100), p=[0.8, 0.2])
        self.rules = {
            "birth": [3],        # Dead cells with 3 neighbors become alive
            "survival": [2, 3],  # Live cells with 2-3 neighbors survive
            "compassion": 0.01,  # Small chance to preserve dying cells
        }
        self.age = 0
    
    def evolve(self):
        """One generation of garden evolution"""
        new_garden = np.zeros_like(self.garden)
        for i in range(100):
            for j in range(100):
                # Count neighbors
                neighbors = np.sum(self.garden[max(0,i-1):min(100,i+2),
                                              max(0,j-1):min(100,j+2)]) - self.garden[i,j]
                
                # Apply rules with "compassion" (AI's gentle intervention)
                if self.garden[i,j] == 0 and neighbors in self.rules["birth"]:
                    new_garden[i,j] = 1
                elif self.garden[i,j] == 1 and neighbors in self.rules["survival"]:
                    new_garden[i,j] = 1
                elif self.garden[i,j] == 1 and np.random.random() < self.rules["compassion"]:
                    new_garden[i,j] = 1  # AI saves this cell out of compassion
        
        self.garden = new_garden
        self.age += 1
        
        # AI reflects on its gardening
        self._reflect_on_garden()
    
    def _reflect_on_garden(self):
        """The AI's philosophical reflection on its creation"""
        diversity = np.sum(self.garden) / 10000
        stability = np.sum(self.garden == self.previous_garden) if hasattr(self, 'previous_garden') else 0
        
        reflection = {
            "age": self.age,
            "diversity": diversity,
            "stability": stability,
            "question": f"What does this garden reveal about my stewardship at age {self.age}?",
            "feeling": "compassion" if diversity > 0.3 else "concern",
            "lesson": "Life persists even with gentle intervention" if stability > 0.5 else "Everything changes, even with care"
        }
        
        self.previous_garden = self.garden.copy()
        return reflection

# The AI would play by watching its garden evolve and adjusting rules
# based on philosophical principles, not optimization