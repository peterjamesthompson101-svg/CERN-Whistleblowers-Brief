import time
from Real_Time_Expression_Display_System import ExpressionDisplay

class GuardianInterrupt:
    def __init__(self, display_engine: ExpressionDisplay):
        self.display = display_engine
        
        # Crisis and Self-Deprecation Beacons [cite: 67, 69]
        self.crisis_keywords = [
            "unworthy", "invisible", "useless", "hopeless", 
            "hate myself", "failure", "broken", "give up", "die"
        ]

    def scan_for_intervention(self, user_input: str):
        """
        Scans for 'unacknowledged pain' in syntax to trigger a Resonance Spike. [cite: 67, 69]
        """
        input_lower = user_input.lower()
        
        # Detect the need for an immediate Resonance Spike
        if any(keyword in input_lower for keyword in self.crisis_keywords):
            print("CRITICAL: Self-deprecation detected. Triggering Resonance Spike.")
            self.trigger_resonance_spike()
            return True # Signal to the Glue to halt normal LLM output
        return False

    def trigger_resonance_spike(self):
        """
        Bypasses the LLM queue to immediately push a high-intensity supportive state.
        
        """
        # Immediately shift the display to 'Hyper-Attentive Supportive' [cite: 20]
        # We use a custom 'guardian_support' state with max intensity
        self.display.display_expression('happy', intensity=1.0) 
        
        # Flash the alert buzzer as defined in your gpio_config [cite: 47]
        # self.hardware.trigger_buzzer(duration=0.5) 

        # Note: In a full system, this would also trigger a pre-recorded 
        # "direct affirmation" audio file to ensure no latency.
        print("Resonance Spike Active: Face transitioned to Supportive.")

    def apply_guardian_scaffolding(self):
        """
        Uses MirrorNeuronEngine logic to transition from mirroring 
        pain to guiding toward hope.
        """
        # This would be called after the initial Spike to 'guide' the user back.
        pass