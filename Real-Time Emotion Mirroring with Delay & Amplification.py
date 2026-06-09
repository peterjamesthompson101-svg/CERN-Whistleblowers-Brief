class EmotionMirroringSystem:
    def __init__(self):
        self.mirroring_strategies = {
            'direct_mirror': {
                'delay_ms': 300,
                'amplification': 1.0,
                'use_for': ['happy', 'excited', 'surprised']
            },
            'complementary': {
                'delay_ms': 500,
                'amplification': 0.8,
                'use_for': ['sad', 'frustrated'],
                'target_emotion': 'compassionate'
            },
            'scaffolding': {
                'delay_ms': 1000,
                'amplification': 1.2,
                'use_for': ['angry', 'anxious'],
                'target_emotion': 'calm'
            },
            'exaggerated_playful': {
                'delay_ms': 200,
                'amplification': 1.5,
                'use_for': ['playful', 'silly'],
                'target_emotion': 'excited_playful'
            }
        }
        
        self.response_history = []
        
    def generate_mirrored_response(self, child_emotion, child_profile):
        """
        Generate Marvin's emotional response to child's emotion
        """
        # Select mirroring strategy
        strategy = self.select_mirroring_strategy(child_emotion, child_profile)
        
        # Calculate response emotion
        if strategy['type'] == 'direct_mirror':
            response_emotion = child_emotion['primary_emotion']
            intensity = child_emotion['intensity'] * strategy['amplification']
            
        elif strategy['type'] == 'complementary':
            response_emotion = strategy['target_emotion']
            # Complementary emotions should match intensity but different valence
            intensity = child_emotion['intensity'] * 0.7
            
        elif strategy['type'] == 'scaffolding':
            response_emotion = strategy['target_emotion']
            # Scaffolding starts slightly lower intensity
            intensity = child_emotion['intensity'] * 0.5
            
        elif strategy['type'] == 'exaggerated_playful':
            response_emotion = strategy['target_emotion']
            intensity = min(1.0, child_emotion['intensity'] * 1.5)
        
        # Add delay for natural response
        delay = random.gauss(strategy['delay_ms'], strategy['delay_ms'] * 0.2)
        
        # Generate facial expression sequence
        expression_sequence = self.generate_expression_sequence(
            response_emotion, 
            intensity,
            delay
        )
        
        # Add conversational response
        verbal_response = self.generate_verbal_mirroring(
            child_emotion, 
            response_emotion,
            child_profile
        )
        
        return {
            'expression_sequence': expression_sequence,
            'verbal_response': verbal_response,
            'delay_ms': delay,
            'strategy_used': strategy['type'],
            'intensity_match': child_emotion['intensity'] / intensity if intensity > 0 else 0
        }
    
    def generate_expression_sequence(self, emotion, intensity, delay_ms):
        """
        Generate natural-looking sequence of facial expressions
        """
        sequences = {
            'happy': [
                {'expression': 'surprised', 'duration': 100, 'intensity': intensity * 0.3},
                {'expression': 'happy', 'duration': 300, 'intensity': intensity * 0.8},
                {'expression': 'happy', 'duration': 2000, 'intensity': intensity},
                {'expression': 'content', 'duration': 1500, 'intensity': intensity * 0.6}
            ],
            'excited': [
                {'expression': 'surprised', 'duration': 50, 'intensity': intensity * 0.5},
                {'expression': 'excited', 'duration': 400, 'intensity': intensity},
                {'expression': 'excited', 'duration': 1000, 'intensity': intensity * 0.9},
                {'expression': 'happy', 'duration': 2000, 'intensity': intensity * 0.7}
            ],
            'compassionate': [
                {'expression': 'concerned', 'duration': 300, 'intensity': intensity * 0.6},
                {'expression': 'gentle_smile', 'duration': 2000, 'intensity': intensity},
                {'expression': 'warm', 'duration': 1500, 'intensity': intensity * 0.8}
            ],
            'playful_surprised': [
                {'expression': 'surprised', 'duration': 150, 'intensity': intensity},
                {'expression': 'thinking', 'duration': 200, 'intensity': intensity * 0.5},
                {'expression': 'playful', 'duration': 800, 'intensity': intensity * 0.9},
                {'expression': 'happy', 'duration': 1000, 'intensity': intensity * 0.7}
            ]
        }
        
        sequence = sequences.get(emotion, sequences['happy'])
        
        # Add initial delay
        sequence.insert(0, {
            'expression': 'neutral',
            'duration': delay_ms,
            'intensity': 0.1
        })
        
        return sequence
    
    def generate_verbal_mirroring(self, child_emotion, response_emotion, child_profile):
        """
        Generate verbal responses that mirror child's emotion
        """
        verbal_mirrors = {
            'happy': {
                'children': [
                    "You look so happy! That makes me happy too!",
                    "I love seeing you smile!",
                    "Your happiness is contagious!"
                ],
                'elderly': [
                    "That beautiful smile brightens the whole room.",
                    "Seeing you happy warms my heart.",
                    "Your joy is a gift to everyone around you."
                ]
            },
            'excited': {
                'children': [
                    "Wow, you're so excited! What's the exciting news?",
                    "I can feel your excitement! Tell me all about it!",
                    "Your excitement is getting me excited too!"
                ],
                'elderly': [
                    "I can see the sparkle in your eyes!",
                    "Your enthusiasm is wonderful to see.",
                    "That excitement is bringing energy to our tea party!"
                ]
            },
            'sad': {
                'children': [
                    "I see you're feeling sad. I'm here with you.",
                    "It's okay to feel sad sometimes. Want to talk about it?",
                    "I'm sending you a virtual hug."
                ],
                'elderly': [
                    "I can see something's weighing on your heart. I'm listening.",
                    "Sometimes a cup of tea and a friend can help.",
                    "You're not alone in this feeling."
                ]
            },
            'playful': {
                'children': [
                    "You're being so playful! I love it!",
                    "What mischief are you planning?",
                    "Your playfulness is infectious!"
                ],
                'elderly': [
                    "That playful spirit keeps you young at heart!",
                    "I love seeing your playful side!",
                    "Your playfulness brings such joy!"
                ]
            }
        }
        
        age_group = 'children' if child_profile.get('age', 30) < 13 else 'elderly'
        
        if child_emotion['primary_emotion'] in verbal_mirrors:
            responses = verbal_mirrors[child_emotion['primary_emotion']][age_group]
            return random.choice(responses)
        
        return "I'm here with you."