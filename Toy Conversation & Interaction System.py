class ToyConversationSystem:
    def __init__(self):
        self.conversation_topics = self.load_topics()
        self.dialogue_engine = DialogueEngine()
        self.toy_personalities = {}
        
    def facilitate_toy_conversation(self, toys, child_emotion, context):
        """
        Facilitate conversation between toys during tea party
        """
        # Select conversation topic based on context
        topic = self.select_conversation_topic(child_emotion, context)
        
        # Assign speaking order
        speaking_order = self.determine_speaking_order(toys, child_emotion)
        
        # Generate conversation
        conversation = []
        for i, toy_id in enumerate(speaking_order):
            toy = next(t for t in toys if t['id'] == toy_id)
            
            # Generate what this toy says
            dialogue = self.generate_toy_dialogue(
                toy, 
                topic, 
                conversation[:i],  # What's been said so far
                child_emotion
            )
            
            conversation.append({
                'toy': toy['personality']['name'],
                'dialogue': dialogue,
                'expression': self.generate_toy_expression(toy, dialogue),
                'voice': toy['voice']
            })
            
            # Occasionally have toys interact with child
            if random.random() < 0.3:  # 30% chance
                question_to_child = self.generate_question_for_child(toy, topic)
                conversation.append({
                    'toy': toy['personality']['name'],
                    'dialogue': question_to_child,
                    'type': 'question_to_child',
                    'expected_response_type': self.get_expected_response_type(question_to_child)
                })
        
        return {
            'topic': topic,
            'conversation': conversation,
            'duration_estimate': len(conversation) * 5,  # 5 seconds per line
            'interaction_opportunities': self.identify_interaction_points(conversation)
        }
    
    def generate_toy_dialogue(self, toy, topic, previous_dialogue, child_emotion):
        """
        Generate dialogue for a specific toy
        """
        dialogue_templates = {
            'wise_elderly': {
                'tea': [
                    "This tea reminds me of the gardens in springtime.",
                    "A good cup of tea makes everything better, don't you think?",
                    "I remember when tea parties were grand affairs with music and dancing."
                ],
                'friendship': [
                    "The best part of any party is the friends you share it with.",
                    "True friendship is like a good cup of tea - warming and comforting.",
                    "We may be different, but we complement each other beautifully."
                ]
            },
            'cheerful_energetic': {
                'tea': [
                    "Yummy! This tea is delicious! Can I have another cookie too?",
                    "I love the little bubbles in my tea! They're dancing!",
                    "Tea parties are the best! So much fun and treats!"
                ],
                'friendship': [
                    "You're my best friend! Let's play forever!",
                    "Friends make everything more fun!",
                    "I'm so happy we're all here together!"
                ]
            },
            'elegant_gracious': {
                'tea': [
                    "The tea service is simply exquisite today.",
                    "One must always take time to appreciate the finer things.",
                    "This blend has lovely floral notes, don't you think?"
                ],
                'friendship': [
                    "It's an honor to be included in such lovely company.",
                    "Friendship adds grace to every occasion.",
                    "Your kindness makes this gathering truly special."
                ]
            }
        }
        
        personality = toy['personality']['personality']
        templates = dialogue_templates.get(personality, dialogue_templates['cheerful_energetic'])
        
        # Get relevant templates for topic
        topic_templates = templates.get(topic, templates['friendship'])
        
        # Select based on child's emotion
        if child_emotion['primary_emotion'] == 'sad':
            # More comforting dialogue
            comforting_templates = [
                "Sometimes a quiet tea with friends is just what we need.",
                "It's okay to have quiet moments. We're here with you.",
                "The warmth of tea and friendship can help any heart."
            ]
            topic_templates = comforting_templates + topic_templates
        
        return random.choice(topic_templates)
    
    def generate_question_for_child(self, toy, topic):
        """
        Generate question for the child to answer
        """
        questions_by_personality = {
            'wise_elderly': [
                "What's your favorite thing about tea parties?",
                "If you could have any kind of tea, what would it be?",
                "What makes a good friend in your opinion?"
            ],
            'cheerful_energetic': [
                "What's the silliest thing you've ever done?",
                "If you were a cookie, what kind would you be?",
                "What's your favorite game to play?"
            ],
            'elegant_gracious': [
                "What's the most beautiful thing you've seen today?",
                "If you could plan the perfect party, what would it be like?",
                "What makes you feel special?"
            ]
        }
        
        personality = toy['personality']['personality']
        questions = questions_by_personality.get(personality, questions_by_personality['cheerful_energetic'])
        
        return random.choice(questions)