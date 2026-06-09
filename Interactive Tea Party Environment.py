class VirtualTeaParty:
    def __init__(self, user_profile):
        self.user_profile = user_profile
        self.environment = self.setup_environment(user_profile)
        self.participants = self.initialize_participants(user_profile)
        self.conversation_engine = TeaPartyConversationEngine()
        self.activities = self.load_activities(user_profile)
        self.mood_atmosphere = self.set_mood_atmosphere(user_profile)
        
    def setup_environment(self, user_profile):
        """
        Create tea party environment based on user preferences
        """
        environments = {
            'traditional_english': {
                'table': 'wooden_round',
                'tea_set': 'porcelain_floral',
                'background': 'english_garden',
                'music': 'classical_soft',
                'lighting': 'afternoon_sun'
            },
            'japanese_tea_ceremony': {
                'table': 'low_tatami',
                'tea_set': 'japanese_ceremonial',
                'background': 'zen_garden',
                'music': 'shakuhachi',
                'lighting': 'soft_tatami'
            },
            'childrens_party': {
                'table': 'colorful_plastic',
                'tea_set': 'cartoon_characters',
                'background': 'rainbow_playroom',
                'music': 'happy_playful',
                'lighting': 'bright_cheerful'
            },
            'memory_lane': {
                'table': 'vintage_wood',
                'tea_set': 'grandmas_china',
                'background': 'old_photographs',
                'music': 'era_appropriate',
                'lighting': 'warm_nostalgic'
            }
        }
        
        # Select environment based on age and preferences
        age = user_profile.get('age', 30)
        if age > 70:
            return environments['memory_lane']
        elif age < 12:
            return environments['childrens_party']
        else:
            return environments['traditional_english']
    
    def initialize_participants(self, user_profile):
        """
        Create tea party participants (AI characters)
        """
        participants = []
        
        # Base participant for elderly
        if user_profile.get('age', 30) > 70:
            participants.append({
                'name': 'Eleanor',
                'age': 'similar',
                'personality': 'gentle_listener',
                'conversation_style': 'reminiscent',
                'appearance': 'kind_elderly_woman',
                'role': 'companion'
            })
            
            # Add memory-triggering characters
            if user_profile.get('memory_triggers'):
                for trigger in user_profile['memory_triggers']:
                    participants.append({
                        'name': trigger['name'],
                        'persona': trigger['persona'],
                        'purpose': 'memory_evocation'
                    })
        
        # Base participant for children
        elif user_profile.get('age', 30) < 12:
            participants.append({
                'name': 'Mr. Teapot',
                'age': 'ageless',
                'personality': 'funny_friendly',
                'conversation_style': 'playful_educational',
                'appearance': 'animated_teapot',
                'role': 'fun_companion'
            })
            
            participants.append({
                'name': 'Sugar Cube',
                'age': 'young',
                'personality': 'sweet_energetic',
                'conversation_style': 'simple_playful',
                'appearance': 'cute_sugar_cube',
                'role': 'play_friend'
            })
        
        # Add AI companion (Marvin)
        participants.append({
            'name': 'Marvin',
            'personality': 'caring_companion',
            'conversation_style': 'adaptive',
            'appearance': 'friendly_robot',
            'role': 'host_companion'
        })
        
        return participants
    
    def load_activities(self, user_profile):
        """
        Load age-appropriate tea party activities
        """
        activities = {
            'pour_tea': {
                'difficulty': 'simple',
                'motor_skills': 'basic',
                'description': 'Pour virtual tea into cups',
                'therapeutic_value': 'fine_motor_practice'
            },
            'serve_cake': {
                'difficulty': 'simple',
                'motor_skills': 'basic',
                'description': 'Serve virtual cakes to participants',
                'social_value': 'sharing_practice'
            },
            'conversation_game': {
                'difficulty': 'variable',
                'cognitive_skills': 'conversational',
                'description': 'Engage in guided conversation',
                'social_value': 'communication_practice'
            },
            'memory_sharing': {
                'difficulty': 'variable',
                'cognitive_skills': 'recall',
                'description': 'Share memories prompted by objects',
                'therapeutic_value': 'reminiscence_therapy'
            },
            'tea_blending': {
                'difficulty': 'medium',
                'cognitive_skills': 'creativity',
                'description': 'Create custom tea blends',
                'educational_value': 'sensory_exploration'
            }
        }
        
        # Filter activities based on user capabilities
        filtered_activities = {}
        for name, activity in activities.items():
            if self.is_activity_appropriate(activity, user_profile):
                filtered_activities[name] = activity
        
        return filtered_activities
    
    def is_activity_appropriate(self, activity, user_profile):
        """
        Check if activity is appropriate for user
        """
        # Check cognitive requirements
        if 'cognitive_skills' in activity:
            required_skill = activity['cognitive_skills']
            user_cognitive = user_profile.get('cognitive_level', 'normal')
            
            if required_skill == 'recall' and user_profile.get('memory_impairment'):
                return False
        
        # Check motor requirements
        if 'motor_skills' in activity:
            required_motor = activity['motor_skills']
            user_motor = user_profile.get('motor_ability', 'normal')
            
            if required_motor == 'fine' and user_profile.get('motor_impairment'):
                return False
        
        return True