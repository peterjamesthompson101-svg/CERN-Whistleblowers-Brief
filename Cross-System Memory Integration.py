class TeaPartyMemoryIntegration:
    def __init__(self, marvin_core):
        self.marvin_core = marvin_core
        self.memory_bridge = MemoryBridge()
        
    def save_tea_party_memory(self, session_data):
        """
        Save tea party experience to Marvin's memory system
        """
        memory_entry = {
            'type': 'tea_party_experience',
            'timestamp': time.time(),
            'toys_present': session_data['toys_present'],
            'child_engagement': session_data['child_engagement_score'],
            'magical_moments': session_data['magical_moments'],
            'child_emotional_journey': session_data['child_emotion_history'],
            'insights': self.extract_insights(session_data)
        }
        
        # Store in chronological dossier
        self.marvin_core.memory.add_to_dossier(
            f"Tea Party with {len(session_data['toys_present'])} toys",
            memory_entry
        )
        
        # Create semantic beacon for future reference
        beacon = {
            'event': 'successful_tea_party',
            'child_preferences': self.extract_child_preferences(session_data),
            'toy_interactions': self.analyze_toy_interactions(session_data),
            'suggested_improvements': self.generate_suggestions(session_data)
        }
        
        self.marvin_core.memory.add_semantic_beacon('tea_party', beacon)
        
        # Update user profile
        self.update_user_profile_from_tea_party(session_data)
    
    def extract_child_preferences(self, session_data):
        """
        Extract child's preferences from tea party interactions
        """
        preferences = {
            'favorite_toys': [],
            'preferred_interactions': [],
            'engagement_patterns': [],
            'emotional_triggers': []
        }
        
        # Analyze which toys child interacted with most
        interaction_counts = {}
        for moment in session_data['magical_moments']:
            if 'toy' in moment:
                interaction_counts[moment['toy']] = interaction_counts.get(moment['toy'], 0) + 1
        
        if interaction_counts:
            favorite_toy = max(interaction_counts, key=interaction_counts.get)
            preferences['favorite_toys'].append(favorite_toy)
        
        # Analyze emotional triggers
        emotion_changes = self.analyze_emotion_changes(session_data['child_emotion_history'])
        preferences['emotional_triggers'] = emotion_changes
        
        return preferences
    
    def generate_suggestions(self, session_data):
        """
        Generate suggestions for future tea parties
        """
        suggestions = []
        
        # Based on engagement patterns
        avg_engagement = np.mean([e['engagement_level'] for e in session_data['child_emotion_history']])
        
        if avg_engagement < 0.5:
            suggestions.append({
                'type': 'increase_engagement',
                'suggestion': 'Include more interactive games next time',
                'reason': 'Child engagement was below optimal level'
            })
        
        # Based on toy interactions
        if len(session_data.get('toy_interactions', [])) < 3:
            suggestions.append({
                'type': 'encourage_interaction',
                'suggestion': 'Prompt child to interact with each toy individually',
                'reason': 'Limited interaction with toys detected'
            })
        
        return suggestions