class ExpressionDisplay:
    def __init__(self):
        self.canvas = None
        self.animation_queue = []
        self.active_effects = []
        self.render_engine = ExpressionRenderEngine()
        
    def initialize_display(self, display_type='rpi_screen'):
        """
        Initialize display based on available hardware
        """
        if display_type == 'rpi_screen':
            self.setup_rpi_framebuffer()
        elif display_type == 'web_interface':
            self.setup_web_canvas()
        elif display_type == 'external_monitor':
            self.setup_hdmi_output()
        
        # Create expression layers
        self.create_expression_layers()
    
    def create_expression_layers(self):
        """
        Create layered canvas for complex expressions
        """
        self.layers = {
            'background': Layer(z_index=0, opacity=1.0),
            'face_base': Layer(z_index=1, opacity=1.0),
            'eyes': Layer(z_index=2, opacity=1.0),
            'mouth': Layer(z_index=3, opacity=1.0),
            'eyebrows': Layer(z_index=4, opacity=1.0),
            'accessories': Layer(z_index=5, opacity=0.8),
            'effects': Layer(z_index=6, opacity=0.6),
            'overlay': Layer(z_index=7, opacity=1.0)
        }
    
    def display_expression(self, expression_name, intensity=1.0, duration=None):
        """
        Display an emotional expression with specified intensity
        """
        expression = self.expression_engine.expression_states[expression_name]
        
        # Adjust expression based on intensity
        adjusted_expression = self.adjust_intensity(expression, intensity)
        
        # Render each layer
        self.render_face_base(adjusted_expression)
        self.render_eyes(adjusted_expression['eyes'])
        self.render_mouth(adjusted_expression['mouth'])
        self.render_accessories(adjusted_expression.get('accessories', []))
        
        # Apply animations
        self.apply_animations(adjusted_expression['animation'])
        
        # Schedule expression duration
        if duration:
            self.schedule_expression_change(duration, 'neutral')
    
    def render_eyes(self, eye_config):
        """
        Render animated eyes with emotion-specific properties
        """
        # Eye shapes
        shapes = {
            'wide_open': self.draw_wide_eyes(),
            'drooping': self.draw_droopy_eyes(),
            'squinted': self.draw_squinted_eyes(),
            'pixel_hearts': self.draw_heart_eyes(),
            'wide_stars': self.draw_starry_eyes()
        }
        
        # Eye animations
        animations = {
            'gentle_bounce': self.animate_bounce(amplitude=2, frequency=0.5),
            'worried_glance': self.animate_glance(rate=0.3, range=20),
            'processing_pulse': self.animate_pulse(speed=0.5, intensity=0.3),
            'sparkle_burst': self.animate_sparkle(count=15, duration=1.0),
            'dance_sync': self.animate_dance(beat_detected=True)
        }
        
        # Apply shape and animation
        eye_shape = shapes.get(eye_config['shape'], shapes['wide_open'])
        eye_animation = animations.get(eye_config['animation'])
        
        self.layers['eyes'].draw(eye_shape)
        self.layers['eyes'].animate(eye_animation)
        
        # Add tears if specified
        if eye_config.get('teardrop'):
            self.render_teardrop(eye_config['teardrop'])
    
    def render_teardrop(self, teardrop_config):
        """
        Render animated teardrops
        """
        tear_properties = {
            'size': teardrop_config.get('size', 'medium'),
            'flow_speed': teardrop_config.get('flow', 'slow_drip'),
            'count': teardrop_config.get('count', 1),
            'transparency': 0.7,
            'reflection': True
        }
        
        # Create tear animation path
        tear_path = self.calculate_tear_path(tear_properties)
        
        # Draw tears on effects layer
        for i in range(tear_properties['count']):
            tear = self.draw_teardrop(
                position=tear_path['start'][i],
                size=tear_properties['size']
            )
            
            self.layers['effects'].add_object(
                tear,
                animation=self.animate_teardrop_fall(tear_path['path'][i])
            )
    
    def render_accessories(self, accessories):
        """
        Render emotional accessories (sparkles, fireworks, etc.)
        """
        accessory_renderers = {
            'sparkles': self.render_sparkles,
            'fireworks': self.render_fireworks,
            'confetti': self.render_confetti,
            'raindrops': self.render_raindrops,
            'disco_lights': self.render_disco_lights,
            'thought_bubbles': self.render_thought_bubbles,
            'robot_arms': self.render_robot_arms
        }
        
        for accessory in accessories:
            if accessory in accessory_renderers:
                accessory_renderers[accessory]()
    
    def render_fireworks(self):
        """
        Render celebratory fireworks animation
        """
        fireworks_config = {
            'count': random.randint(5, 15),
            'types': ['burst', 'fountain', 'willow', 'peony'],
            'colors': ['#FF6B6B', '#4ECDC4', '#FFD166', '#06D6A0', '#118AB2'],
            'duration': 3.0,
            'sound_effect': 'fireworks_pop' if self.has_audio else None
        }
        
        # Create multiple firework bursts
        for i in range(fireworks_config['count']):
            firework_type = random.choice(fireworks_config['types'])
            color = random.choice(fireworks_config['colors'])
            
            self.create_firework_burst(
                type=firework_type,
                color=color,
                position=self.random_screen_position(),
                delay=i * 0.2
            )
    
    def render_robot_arms(self):
        """
        Render dancing robot arms animation
        """
        arm_config = {
            'segments': 3,
            'joint_angles': [30, -20, 45],  # Degrees for each joint
            'dance_pattern': 'robot_disco',
            'beat_sync': True,
            'glow_effect': True
        }
        
        # Create left and right arms
        left_arm = self.create_robot_arm(
            side='left',
            base_position=(100, 300),
            config=arm_config
        )
        
        right_arm = self.create_robot_arm(
            side='right',
            base_position=(700, 300),
            config=arm_config
        )
        
        # Animate arms in sync
        animation = self.create_robot_dance_animation(
            left_arm=left_arm,
            right_arm=right_arm,
            pattern=arm_config['dance_pattern']
        )
        
        self.layers['accessories'].add_animation(animation)