class ToyInteractionTracker:
    def __init__(self):
        self.interaction_history = []
        self.toy_states = {}
        self.child_toy_interactions = []
        
    def track_child_toy_interactions(self, child_pose, toy_positions):
        """
        Track how child interacts with each toy
        """
        interactions = []
        
        for toy_id, toy_position in toy_positions.items():
            # Calculate distance between child's hands and toy
            for hand in ['left_hand', 'right_hand']:
                hand_position = child_pose.get(hand)
                if hand_position:
                    distance = self.calculate_distance(hand_position, toy_position)
                    
                    if distance < 50:  # pixels - toy is being touched
                        interaction = {
                            'toy_id': toy_id,
                            'hand': hand,
                            'interaction_type': self.determine_interaction_type(
                                child_pose, toy_position
                            ),
                            'duration': self.measure_interaction_duration(toy_id, hand),
                            'intensity': self.calculate_interaction_intensity(child_pose)
                        }
                        
                        interactions.append(interaction)
                        
                        # Update toy's emotional state based on interaction
                        self.update_toy_emotional_state(toy_id, interaction)
        
        return interactions
    
    def determine_interaction_type(self, child_pose, toy_position):
        """
        Determine type of interaction (hugging, moving, feeding, etc.)
        """
        # Analyze hand shape and movement
        hand_shape = self.analyze_hand_shape(child_pose)
        movement_pattern = self.analyze_movement_pattern(child_pose)
        
        if hand_shape == 'open_palm' and movement_pattern == 'patting':
            return 'petting'
        elif hand_shape == 'grasp' and movement_pattern == 'lifting':
            return 'picking_up'
        elif hand_shape == 'cup' and movement_pattern == 'moving_toward_mouth':
            return 'feeding'
        elif hand_shape == 'wrap' and movement_pattern == 'squeeze':
            return 'hugging'
        elif hand_shape == 'point' and movement_pattern == 'still':
            return 'pointing_at'
        
        return 'touching'
    
    def update_toy_emotional_state(self, toy_id, interaction):
        """
        Update toy's emotional state based on how child interacts with it
        """
        if toy_id not in self.toy_states:
            self.toy_states[toy_id] = {
                'happiness': 0.5,
                'energy': 0.5,
                'engagement': 0.5,
                'preferred_interactions': []
            }
        
        toy_state = self.toy_states[toy_id]
        
        # Adjust emotional state based on interaction
        if interaction['interaction_type'] in ['hugging', 'petting']:
            toy_state['happiness'] = min(1.0, toy_state['happiness'] + 0.1)
            toy_state['engagement'] = min(1.0, toy_state['engagement'] + 0.15)
        elif interaction['interaction_type'] == 'feeding':
            toy_state['energy'] = min(1.0, toy_state['energy'] + 0.2)
        
        # Record preferred interactions
        if interaction['duration'] > 2.0:  # Longer interactions indicate preference
            if interaction['interaction_type'] not in toy_state['preferred_interactions']:
                toy_state['preferred_interactions'].append(interaction['interaction_type'])
    
    def generate_toy_response(self, toy_id, interaction):
        """
        Generate how toy would respond to the interaction
        """
        toy_state = self.toy_states[toy_id]
        personality = self.get_toy_personality(toy_id)
        
        responses = {
            'hugging': {
                'high_happiness': [
                    "Oh, I love your hugs!",
                    "You give the best hugs!",
                    "Mmm, so cozy!"
                ],
                'medium_happiness': [
                    "That's a nice hug!",
                    "Thank you for the hug!",
                    "Hugs make everything better!"
                ]
            },
            'petting': {
                'wise_elderly': [
                    "A gentle pat always makes me feel cared for.",
                    "Your kind touch reminds me of sunny days."
                ],
                'cheerful_energetic': [
                    "Yay! Petting time!",
                    "This feels wonderful! Do it again!"
                ]
            },
            'feeding': [
                "Yummy! Thank you for the tea!",
                "This is delicious! You're a great host!",
                "Mmm, my favorite!"
            ]
        }
        
        # Select appropriate response
        happiness_level = 'high_happiness' if toy_state['happiness'] > 0.8 else 'medium_happiness'
        
        if interaction['interaction_type'] in responses:
            category_responses = responses[interaction['interaction_type']]
            
            if isinstance(category_responses, dict):
                # Has subcategories
                if happiness_level in category_responses:
                    response_list = category_responses[happiness_level]
                elif personality['personality'] in category_responses:
                    response_list = category_responses[personality['personality']]
                else:
                    response_list = list(category_responses.values())[0]
            else:
                response_list = category_responses
            
            return random.choice(response_list)
        
        return "Thank you for playing with me!"