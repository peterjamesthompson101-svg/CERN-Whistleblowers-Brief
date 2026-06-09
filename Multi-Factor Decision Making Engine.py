class AIOpponentLearningEngine:
    def __init__(self):
        self.learning_policies = self.initialize_learning_policies()
        self.performance_history = {}
        self.user_model = UserBehaviorModel()
        self.outcome_strategies = OutcomeStrategyManager()
        
    def determine_game_strategy(self, game_context, user_profile):
        """
        Determine AI strategy based on multiple factors
        """
        strategy = {
            'skill_level': self.calculate_ai_skill_level(game_context, user_profile),
            'outcome_goal': self.determine_outcome_goal(game_context, user_profile),
            'learning_focus': self.identify_learning_focus(user_profile),
            'emotional_tone': self.determine_emotional_tone(game_context),
            'adaptation_rate': self.calculate_adaptation_rate(user_profile)
        }
        
        # Apply learning policies
        for policy in self.learning_policies:
            if policy['condition'].evaluate(game_context, user_profile):
                strategy = policy['action'].apply(strategy)
        
        return strategy
    
    def calculate_ai_skill_level(self, game_context, user_profile):
        """
        Calculate appropriate AI skill level for this game
        """
        base_skill = user_profile.get('current_skill_level', 0.5)
        
        # Adjust based on age
        age = user_profile.get('age', 30)
        if age > 70:
            base_skill *= 0.7  # Reduce difficulty for elderly
        elif age < 18:
            base_skill *= 0.8  # Reduce for children
        
        # Adjust based on cognitive condition
        if user_profile.get('cognitive_condition'):
            condition = user_profile['cognitive_condition']
            adjustments = {
                'dementia_early': 0.6,
                'dementia_moderate': 0.4,
                'dementia_advanced': 0.2,
                'adhd': 0.9,  # ADHD often benefits from challenge
                'stroke_recovery': 0.5,
                'depression': 0.7
            }
            base_skill *= adjustments.get(condition, 0.8)
        
        # Adjust based on emotional state
        emotional_state = user_profile.get('emotional_state', 'neutral')
        if emotional_state == 'frustrated':
            base_skill *= 0.6  # Reduce difficulty to prevent more frustration
        elif emotional_state == 'bored':
            base_skill *= 1.2  # Increase challenge
        
        # Adjust based on learning goals
        learning_goal = user_profile.get('learning_goal')
        if learning_goal == 'build_confidence':
            base_skill *= 0.7
        elif learning_goal == 'develop_resilience':
            base_skill *= 1.1
        
        return min(max(base_skill, 0.1), 0.95)  # Keep within bounds
    
    def determine_outcome_goal(self, game_context, user_profile):
        """
        Determine whether AI should win, lose, or draw
        """
        # Extract factors
        arrogance_level = user_profile.get('arrogance_level', 0.5)
        competitiveness = user_profile.get('competitiveness', 0.5)
        recent_losses = user_profile.get('recent_losses', 0)
        mood = user_profile.get('mood', 'neutral')
        
        # Decision matrix
        if arrogance_level > 0.8:
            # Arrogant users benefit from occasional losses
            if recent_losses < 2:
                return 'win'  # Bring them down a notch
            else:
                return 'lose'  # Prevent excessive frustration
        
        elif competitiveness > 0.7:
            # Competitive users enjoy challenge
            win_probability = 0.6  # Mostly win, but not always
            if random.random() < win_probability:
                return 'win'
            else:
                return 'lose'
        
        elif mood in ['sad', 'depressed', 'anxious']:
            # Users in negative mood need encouragement
            if random.random() < 0.3:
                return 'win'
            else:
                return 'lose'  # Let them win to boost mood
        
        elif user_profile.get('learning_goal') == 'teaching':
            # Teaching mode: AI demonstrates strategies
            return 'draw'  # Demonstrate without crushing
        
        elif user_profile.get('age', 30) > 75:
            # Elderly: focus on engagement, not competition
            if random.random() < 0.4:
                return 'win'
            else:
                return 'lose'
        
        else:
            # Default: balanced approach
            outcomes = ['win', 'lose', 'draw']
            weights = [0.4, 0.4, 0.2]  # 40% win, 40% lose, 20% draw
            return random.choices(outcomes, weights=weights)[0]
    
    def execute_outcome_strategy(self, game_state, strategy, user_profile):
        """
        Execute the chosen outcome strategy during gameplay
        """
        if strategy['outcome_goal'] == 'win':
            return self.play_to_win(game_state, strategy['skill_level'])
        
        elif strategy['outcome_goal'] == 'lose':
            return self.play_to_lose_elegantly(game_state, user_profile)
        
        elif strategy['outcome_goal'] == 'draw':
            return self.play_for_draw(game_state, strategy['skill_level'])
        
        elif strategy['outcome_goal'] == 'teach':
            return self.play_teaching_mode(game_state, user_profile)
    
    def play_to_lose_elegantly(self, game_state, user_profile):
        """
        Lose in a way that feels natural and maintains engagement
        """
        # Don't make it obvious - vary the "mistakes"
        mistake_types = [
            'strategic_error',  # Make suboptimal strategic choice
            'tactical_error',   # Make poor tactical move
            'oversight',        # Miss an obvious opportunity
            'overconfidence',   # Take unnecessary risk
            'defensive_error'   # Fail to defend properly
        ]
        
        # Choose mistake based on user's skill level
        user_skill = user_profile.get('game_skill', 0.5)
        if user_skill < 0.3:
            # Novice: Make obvious but believable mistakes
            mistake = random.choice(['oversight', 'defensive_error'])
        elif user_skill < 0.7:
            # Intermediate: Make subtle strategic errors
            mistake = random.choice(['strategic_error', 'tactical_error'])
        else:
            # Advanced: Make very subtle errors
            mistake = 'strategic_error'
        
        # Execute the mistake
        move = self.generate_mistake_move(game_state, mistake)
        
        # Add commentary if in teaching mode
        if user_profile.get('learning_goal') == 'teaching':
            commentary = self.generate_teaching_commentary(mistake)
            return {'move': move, 'commentary': commentary}
        
        return {'move': move}
    
    def play_teaching_mode(self, game_state, user_profile):
        """
        Play in a way that demonstrates strategies and concepts
        """
        # Choose teaching focus
        teaching_focus = self.identify_teaching_opportunity(game_state, user_profile)
        
        # Make move that demonstrates the concept
        demonstration_move = self.generate_demonstration_move(
            game_state, teaching_focus
        )
        
        # Generate explanation
        explanation = self.generate_teaching_explanation(
            teaching_focus, demonstration_move
        )
        
        return {
            'move': demonstration_move,
            'teaching_focus': teaching_focus,
            'explanation': explanation,
            'question': self.generate_reflective_question(teaching_focus)
        }