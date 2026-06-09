import time
import numpy as np
import pyaudio
import sys
import os

# Adds the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Ensure you have renamed the file to include underscores
from Mirror_Neuron_Engine_for_Emotional_Synchronization import MirrorNeuronEngine
# Note: You may also need to ensure 'Real_Time_Expression_Display_System' is available
try:
    from Real_Time_Expression_Display_System import ExpressionDisplay
except ImportError:
    print("Warning: ExpressionDisplay module not found. Visuals may be disabled.")
    ExpressionDisplay = None

class SocialPerceptionBridge:
    def __init__(self, display_engine):
        self.display = display_engine
        self.mirror_engine = MirrorNeuronEngine()
        
        # Audio Sensing Parameters
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.THRESHOLD = 500  
        
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
        
        self.is_user_speaking = False
        print("Social Perception Bridge: Online and Listening...")

    def monitor_audio_cues(self):
        try:
            data = np.frombuffer(self.stream.read(self.CHUNK, exception_on_overflow=False), dtype=np.int16)
            peak = np.average(np.abs(data))
            
            if peak > self.THRESHOLD:
                if not self.is_user_speaking:
                    self.on_speech_start()
                    self.is_user_speaking = True
            else:
                if self.is_user_speaking:
                    self.on_speech_end()
                    self.is_user_speaking = False
        except Exception as e:
            print(f"Perception Error: {e}")

    def on_speech_start(self):
        print("User detected. Transitioning to 'Attentive' state.")
        if self.display:
            self.display.display_expression('thinking', intensity=0.4)

    def on_speech_end(self):
        print("User finished. Transitioning to 'Processing' state.")
        if self.display:
            self.display.display_expression('thinking', intensity=0.8)

    def run_bridge(self):
        while True:
            self.monitor_audio_cues()
            time.sleep(0.01)

if __name__ == "__main__":
    # Test block
    if ExpressionDisplay:
        disp = ExpressionDisplay()
        disp.initialize_display(display_type='rpi_screen')
    else:
        disp = None
    
    bridge = SocialPerceptionBridge(disp)
    bridge.run_bridge()
