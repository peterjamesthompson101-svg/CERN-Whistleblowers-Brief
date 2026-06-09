class DrawingAIAssistant:
    def __init__(self):
        self.style_recommender = StyleRecommender()
        self.color_adviser = ColorAdviser()
        self.creative_companion = CreativeCompanion()
        self.emotional_responder = DrawingEmotionalResponder()
        
    def provide_assistance(self, drawing_context, user_profile):
        """
        Provide appropriate drawing assistance based on context
        """
        assistance = {
            'suggestions': [],
            'encouragement': [],
            'technical_help': [],
            'creative_ideas': []
        }
        
        # Check if user is struggling
        if self.detect_struggle(drawing_context):
            assistance['suggestions'].append(
                self.suggest_simplified_approach(drawing_context)
            )
            assistance['encouragement'].append(
                self.generate_encouragement(drawing_context, user_profile)
            )
        
        # Check if user might want creative ideas
        if self.detect_creative_block(drawing_context):
            assistance['creative_ideas'].append(
                self.suggest_creative_direction(drawing_context, user_profile)
            )
        
        # Provide color suggestions
        assistance['color_suggestions'] = self.color_adviser.suggest_colors(
            drawing_context, user_profile
        )
        
        # Provide style suggestions
        assistance['style_suggestions'] = self.style_recommender.suggest_style(
            drawing_context, user_profile
        )
        
        return assistance
    
    def detect_struggle(self, drawing_context):
        """
        Detect if user is struggling with drawing
        """
        indicators = [
            'frequent_erasing',
            'long_pauses',
            'repetitive_strokes',
            'abandoned_drawings',
            'frustrated_gestures'  # From camera if available
        ]
        
        return any(indicator in drawing_context for indicator in indicators)
    
    def suggest_simplified_approach(self, drawing_context):
        """
        Suggest simplified drawing approach
        """
        simplifications = {
            'complex_object': "Try breaking it down into basic shapes first",
            'perspective': "Don't worry about perfect perspective - focus on what you enjoy",
            'details': "Sometimes less is more. Try a simpler version first",
            'coloring': "You could try filling larger areas with one color first"
        }
        
        # Identify what user is trying to draw
        attempted_subject = self.identify_drawing_subject(drawing_context)
        
        if attempted_subject in simplifications:
            return simplifications[attempted_subject]
        else:
            return "Try starting with the biggest, simplest shapes first"
    
    def generate_encouragement(self, drawing_context, user_profile):
        """
        Generate personalized encouragement
        """
        encouragements = {
            'elderly': [
                "Your experience brings unique beauty to your art",
                "Every stroke tells a story - I love seeing yours",
                "Art is about expression, not perfection"
            ],
            'children': [
                "Wow, you're doing amazing!",
                "I love your creative choices!",
                "You're such a talented artist!"
            ],
            'therapeutic': [
                "Art is a wonderful way to express yourself",
                "There's no wrong way to create art",
                "I can see you putting your heart into this"
            ]
        }
        
        age = user_profile.get('age', 30)
        if age > 65:
            category = 'elderly'
        elif age < 13:
            category = 'children'
        else:
            category = 'therapeutic'
        
        return random.choice(encouragements[category])
    
    def celebrate_completion(self, drawing, user_profile):
        """
        Celebrate when user completes a drawing
        """
        celebration = {
            'expression': 'excited',
            'visual_effects': ['confetti', 'sparkles'],
            'message': self.generate_completion_message(drawing, user_profile),
            'suggest_next': self.suggest_next_activity(drawing, user_profile)
        }
        
        # Trigger Marvin's happy expression
        self.trigger_marvin_expression('happy', intensity=0.9)
        
        # Show fireworks
        self.trigger_visual_effect('fireworks')
        
        return celebration