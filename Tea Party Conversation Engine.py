class TeaPartyConversationEngine:
    def __init__(self):
        self.conversation_topics = self.load_topics()
        self.prompt_generator = ConversationPromptGenerator()
        self.emotional_regulator = ConversationEmotionalRegulator()
        self.memory_trigger = MemoryTriggerEngine()
        
    def load_topics(self):
        """
        Load age-appropriate conversation topics
        """
        return {
            'elderly': {
                'reminiscence': [
                    "Tell me about your favorite childhood memory",
                    "What was the first concert you ever attended?",
                    "Describe your first job",
                    "What was school like when you were young?"
                ],
                'current_interests': [
                    "What do you enjoy doing these days?",
                    "Tell me about your family",
                    "What's your favorite season and why?"
                ],
                'wisdom_sharing': [
                    "What's the best advice you've ever received?",
                    "What life lesson would you share with younger people?"
                ]
            },
            'children': {
                'imagination': [
                    "If you could have any superpower, what would it be?",
                    "What would your perfect day look like?",
                    "If you were an animal, what would you be?"
                ],
                'playful': [
                    "What's the funniest thing that's happened to you?",
                    "What's your favorite silly joke?",
                    "If your toys could talk, what would they say?"
                ],
                'learning': [
                    "What's something new you learned recently?",
                    "What's your favorite thing about school?",
                    "What do you want to be when you grow up?"
                ]
            },
            'intergenerational': {
                'shared_experiences': [
                    "What's your favorite thing about each season?",
                    "What makes a good friend?",
                    "What's the best meal you've ever had?"
                ],
                'comparisons': [
                    "How is life different now than when you were young?",
                    "What games did you play as a child?"
                ]
            }
        }
    
    def generate_conversation_flow(self, user_profile, participants):
        """
        Generate a natural conversation flow for the tea party
        """
        # Select topic category based on user
        age = user_profile.get('age', 30)
        if age > 65:
            category = 'elderly'
        elif age < 13:
            category = 'children'
        else:
            category = 'intergenerational'
        
        # Create conversation structure
        conversation = {
            'opening': self.generate_opening(category),
            'main_topics': self.select_topics(category, 3),
            'questions_for_user': self.generate_questions(category, user_profile),
            'ai_responses': self.prepare_ai_responses(category),
            'closing': self.generate_closing(category)
        }
        
        # Add memory triggers for elderly
        if age > 70 and user_profile.get('memory_triggers'):
            conversation['memory_prompts'] = self.generate_memory_prompts(
                user_profile['memory_triggers']
            )
        
        return conversation
    
    def generate_memory_prompts(self, memory_triggers):
        """
        Generate prompts to trigger positive memories
        """
        prompts = []
        
        for trigger in memory_triggers:
            if trigger['type'] == 'object':
                prompts.append({
                    'trigger_object': trigger['object'],
                    'prompt': f"This {trigger['object']} reminds me of...",
                    'visual_cue': trigger.get('image'),
                    'sensory_cue': trigger.get('sensory_description')
                })
            elif trigger['type'] == 'topic':
                prompts.append({
                    'topic': trigger['topic'],
                    'prompt': f"Tell me about your experiences with {trigger['topic']}",
                    'guiding_questions': trigger.get('questions', [])
                })
        
        return prompts