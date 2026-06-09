import pygame
import os
# Standardized imports for the Carer System
from Animated_Expression_System_Architecture import EmotionalExpressionEngine
from modules.expression_render_engine import ExpressionRenderEngine

class ExpressionDisplay:
    def __init__(self, fullscreen=False):
        self.expression_engine = EmotionalExpressionEngine()
        self.current_frame_data = self.expression_engine.expression_states['neutral']
        self.renderer = ExpressionRenderEngine(resolution=(800, 480), fullscreen=fullscreen)
        self.running = True

    def refresh(self):
        """Standard Pygame loop with no syntax tags."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
        
        self.renderer.render_frame(self.current_frame_data)

    def update_expression(self, emotion_key):
        """Updates the visual state based on Marvin's mood."""
        if emotion_key in self.expression_engine.expression_states:
            self.current_frame_data = self.expression_engine.get_current_expression(emotion_key)
