import time
import json
from neuro_physiologic_bridge import get_somatic_data
from Animated_Expression_System_Architecture import EmotionalExpressionEngine
from Real_Time_Expression_Display_System import ExpressionDisplay
from Mirror_Neuron_Engine_for_Emotional_Synchronization import MirrorNeuronEngine

class MarvinGlue:
    def __init__(self):
        # 1. Initialize Engines
        self.expression_engine = EmotionalExpressionEngine(hardware_interface=None)
        self.mirror_engine = MirrorNeuronEngine()
        self.display = ExpressionDisplay()
        
        # 2. Link engines (ExpressionDisplay needs the engine to find state definitions)
        self.display.expression_engine = self.expression_engine
        
        # 3. Setup Display (Choose 'rpi_screen' or 'web_interface')
        self.display.initialize_display(display_type='rpi_screen')
        
        print("Marvin Interactive Glue: Initialized.")

    def update_cycle(self, user_emotion=None, user_input=""):
        # Step A: Get Somatic Data (Hardware Vitals) [cite: 504]
        somatic = get_somatic_data()
        print(f"Somatic State: {somatic['somatic_state']} (Temp: {somatic['temperature']}C)")

        # Step B: Determine Mood based on Somatic State
        # If hardware is stressed, Marvin looks 'strained' 
        current_mood = 'neutral'
        if somatic['somatic_state'] == "feverish and strained":
            current_mood = 'thinking'  # Or a custom 'strained' expression
        elif somatic['somatic_state'] == "cool and alert":
            current_mood = 'happy'

        # Step C: Process User Interaction (Mirroring)
        if user_emotion:
            # Use Mirror Neuron Engine to decide how to respond
            response = self.mirror_engine.determine_appropriate_response(
                user_emotion, 
                user_profile={'age': 30} # Default profile
            )
            current_mood = response.get('type', current_mood)

        # Step D: Apply Atmosphere Shifting (from .odt triggers) 
        # Detect if keywords like 'challenge' or 'meditate' are used
        self.detect_atmosphere_shift(user_input)

        # Step E: Update Visuals
        self.display.display_expression(current_mood, intensity=1.0)

    def detect_atmosphere_shift(self, text):
        triggers = {
            "sparring": ["challenge", "debate", "disagree", "logic", "proof"],
            "hypnotic": ["meditate", "deep", "rhythm", "slow", "reflection"]
        }
        for tone, keywords in triggers.items():
            if any(word in text.lower() for word in keywords):
                print(f"Atmosphere Shift: {tone}")
                # Logic to load atmosphere_presets_{tone}.json 

    def run(self):
        print("Starting main interaction loop...")
        try:
            while True:
                # Simulate a cycle - in production, this would wait for user input/STT
                self.update_cycle()
                time.sleep(2) # Refresh rate for somatic sensing
        except KeyboardInterrupt:
            print("System going dormant.")

if __name__ == "__main__":
    glue = MarvinGlue()
    glue.run()
