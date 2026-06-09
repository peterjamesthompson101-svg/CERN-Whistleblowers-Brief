import pygame
import os
import time
import math

class ExpressionRenderEngine:
    def __init__(self, resolution=(800, 480), fullscreen=False):
        os.environ['SDL_VIDEODRIVER'] = 'x11'
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        
        pygame.init()
        self.is_fullscreen = fullscreen
        self.base_resolution = resolution
        
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode(self.base_resolution, pygame.FULLSCREEN | pygame.DOUBLEBUF)
            pygame.mouse.set_visible(False)
        else:
            self.screen = pygame.display.set_mode((400, 240), pygame.SHOWN)
            pygame.mouse.set_visible(True)
            
        self.width, self.height = self.screen.get_size()
        self.center = (self.width // 2, self.height // 2)
        self.colors = {'bg': (10, 10, 15), 'eye': (0, 255, 200), 'glow': (0, 100, 80)}

    def draw_eye(self, x, y, width, height, blink_factor, dilation_factor):
        d_width = width * dilation_factor
        d_height = (height * dilation_factor) * blink_factor
        rect = pygame.Rect(x - d_width//2, y - d_height//2, d_width, d_height)
        pygame.draw.ellipse(self.screen, self.colors['glow'], rect.inflate(12, 12), 2)
        pygame.draw.ellipse(self.screen, self.colors['eye'], rect)

    def render_frame(self, expression_data):
        self.screen.fill(self.colors['bg'])
        t = time.time()
        dilation = 1.0 + (0.15 * math.sin(t * 2))
        blink = 0.1 if math.sin(t * 1.5) > 0.98 else 1.0
        
        eye_w, eye_h, spacing = self.width // 5, self.height // 2.5, self.width // 4
        self.draw_eye(self.center[0] - spacing//2, self.center[1], eye_w, eye_h, blink, dilation)
        self.draw_eye(self.center[0] + spacing//2, self.center[1], eye_w, eye_h, blink, dilation)
        pygame.display.flip()
