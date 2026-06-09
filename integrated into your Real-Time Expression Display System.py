import random
import time

class GazeController:
    def __init__(self, display_engine):
        self.display = display_engine
        self.last_saccade_time = time.time()
        self.gaze_center = (0, 0)  # Relative offset from true center
        self.is_active = True

        # Saccade parameters
        self.min_interval = 1.5  # Seconds between shifts
        self.max_interval = 5.0
        self.saccade_magnitude = 15  # Pixels of max deviation

    def update_idle_gaze(self):
        """
        Periodically triggers a 'Saccade' to keep the eyes looking alive.
                """
        current_time = time.time()
        
        # Determine if it's time for a new micro-movement
        if current_time - self.last_saccade_time > random.uniform(self.min_interval, self.max_interval):
            self.trigger_saccade()
            self.last_saccade_time = current_time

    def trigger_saccade(self):
        """
        Calculates a new random offset for the pupils.
        """
        # Small random shift to simulate shifting focus
        dx = random.randint(-self.saccade_magnitude, self.saccade_magnitude)
        dy = random.randint(-self.saccade_magnitude // 2, self.saccade_magnitude // 2)
        
        self.gaze_center = (dx, dy)
        
        # Apply this offset to the 'eyes' layer in ExpressionDisplay
        self.display.layers['eyes'].set_offset(self.gaze_center)
        
        # Occasionally trigger a micro-blink with the saccade for realism
        if random.random() > 0.8:
            self.display.layers['eyes'].trigger_animation('micro_blink')

    def focus_on_user(self):
        """
        Resets gaze to center when the user is speaking. 
        Linked to the Social_Perception_Bridge.
        """
        self.gaze_center = (0, 0)
        self.display.layers['eyes'].set_offset(self.gaze_center)