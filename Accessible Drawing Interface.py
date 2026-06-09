class InteractiveDrawingProgram:
    def __init__(self, user_profile):
        self.user_profile = user_profile
        self.canvas_config = self.initialize_canvas(user_profile)
        self.tools = self.initialize_tools(user_profile)
        self.coloring_books = self.load_coloring_books(user_profile)
        self.ai_assistant = DrawingAIAssistant()
        self.accessibility_features = self.setup_accessibility(user_profile)
        
    def initialize_canvas(self, user_profile):
        """
        Create canvas optimized for user's abilities
        """
        config = {
            'size': self.determine_canvas_size(user_profile),
            'background': self.select_background(user_profile),
            'grid': self.setup_grid(user_profile),
            'zoom': self.setup_zoom_controls(user_profile),
            'undo_redo': self.setup_undo_redo(user_profile)
        }
        
        # Adjust for cognitive conditions
        if user_profile.get('cognitive_condition'):
            condition = user_profile['cognitive_condition']
            if condition in ['dementia', 'alzheimers']:
                config['simplified_interface'] = True
                config['tool_count'] = 4  # Only basic tools
                config['auto_save'] = True
            elif condition == 'parkinsons':
                config['motion_stabilization'] = True
                config['larger_buttons'] = True
            elif condition == 'stroke_recovery':
                config['one_handed_mode'] = True
                config['adaptive_difficulty'] = True
        
        # Adjust for age
        if user_profile.get('age', 30) > 65:
            config['button_size'] = 'large'
            config['contrast_ratio'] = 'high'
            config['font_size'] = 'large'
        
        return config
    
    def initialize_tools(self, user_profile):
        """
        Initialize drawing tools based on user capabilities
        """
        tools = {
            'basic': {
                'pencil': {
                    'sizes': [1, 3, 5, 8],
                    'pressure_sensitive': False,
                    'stabilizer': True
                },
                'brush': {
                    'types': ['round', 'flat', 'watercolor'],
                    'sizes': [2, 5, 10, 20],
                    'transparency': True
                },
                'eraser': {
                    'sizes': [5, 10, 20, 40],
                    'shape': 'round'
                },
                'fill': {
                    'tolerance': 20,
                    'contiguous_only': True
                }
            },
            'shapes': {
                'rectangle': {
                    'fill': True,
                    'stroke': True,
                    'rounded_corners': True
                },
                'circle': {
                    'fill': True,
                    'stroke': True
                },
                'line': {
                    'arrowheads': True,
                    'dashed': True
                },
                'polygon': {
                    'sides': 3,
                    'regular': True
                }
            },
            'advanced': {
                'stamp': {
                    'categories': ['animals', 'nature', 'emotions', 'objects'],
                    'size_adjustable': True,
                    'rotate': True
                },
                'text': {
                    'fonts': self.select_accessible_fonts(user_profile),
                    'sizes': [12, 16, 24, 32, 48],
                    'colors': self.get_high_contrast_colors()
                },
                'gradient': {
                    'linear': True,
                    'radial': True,
                    'color_picker': 'advanced'
                }
            }
        }
        
        # Simplify tools for certain users
        if user_profile.get('age', 30) > 70:
            tools = self.simplify_tools_for_elderly(tools)
        
        if user_profile.get('cognitive_condition') in ['dementia', 'alzheimers']:
            tools = self.simplify_tools_for_dementia(tools)
        
        return tools
    
    def load_coloring_books(self, user_profile):
        """
        Load age-appropriate coloring books
        """
        coloring_books = {
            'elderly': {
                'themes': ['nature', 'animals', 'mandalas', 'memory_lane'],
                'complexity': 'low',
                'line_thickness': 'medium',
                'therapeutic': True,
                'examples': [
                    {
                        'title': 'Garden Memories',
                        'description': 'Beautiful garden scenes for reminiscence',
                        'pages': 12,
                        'preview_colors': ['pastel', 'vibrant']
                    },
                    {
                        'title': 'Animal Friends',
                        'description': 'Friendly animals with large coloring areas',
                        'pages': 8,
                        'preview_colors': ['natural', 'fantasy']
                    }
                ]
            },
            'children': {
                'themes': ['cartoons', 'fairytales', 'vehicles', 'animals'],
                'complexity': 'very_low',
                'line_thickness': 'thick',
                'educational': True,
                'examples': [
                    {
                        'title': 'Magical Forest',
                        'description': 'Friendly forest creatures',
                        'pages': 10,
                        'interactive': True  // Makes sounds when colored
                    },
                    {
                        'title': 'ABC Coloring',
                        'description': 'Learn letters while coloring',
                        'pages': 26,
                        'educational_value': 'alphabet_learning'
                    }
                ]
            },
            'therapeutic': {
                'themes': ['stress_relief', 'mindfulness', 'emotional_expression'],
                'complexity': 'variable',
                'line_thickness': 'variable',
                'guided': True,
                'examples': [
                    {
                        'title': 'Emotion Garden',
                        'description': 'Color based on your emotions',
                        'pages': 6,
                        'emotion_guided': True
                    },
                    {
                        'title': 'Calm Patterns',
                        'description': 'Repetitive patterns for mindfulness',
                        'pages': 8,
                        'breathing_guided': True
                    }
                ]
            }
        }
        
        # Select appropriate coloring books
        age = user_profile.get('age', 30)
        condition = user_profile.get('cognitive_condition')
        
        if age > 65 or condition in ['dementia', 'alzheimers']:
            return coloring_books['elderly']
        elif age < 12:
            return coloring_books['children']
        else:
            return coloring_books['therapeutic']
    
    def setup_accessibility(self, user_profile):
        """
        Setup accessibility features based on user needs
        """
        features = {
            'voice_control': False,
            'eye_tracking': False,
            'switch_control': False,
            'screen_reader': False,
            'high_contrast': False,
            'motion_reduction': False
        }
        
        # Enable features based on needs
        if user_profile.get('motor_impairment'):
            features['voice_control'] = True
            features['switch_control'] = True
        
        if user_profile.get('visual_impairment'):
            features['high_contrast'] = True
            features['screen_reader'] = True
        
        if user_profile.get('cognitive_condition') in ['adhd', 'autism']:
            features['motion_reduction'] = True
            features['simplified_interface'] = True
        
        return features