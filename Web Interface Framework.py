class GamePortalInterface:
    def __init__(self):
        self.templates = self.load_templates()
        self.user_sessions = {}
        self.game_states = {}
        
    def generate_portal_homepage(self, user_profile):
        """
        Generate personalized game portal homepage
        """
        recommended_games = self.recommend_games(user_profile)
        
        portal_html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Marvin Cognitive Engagement Portal</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                {self.get_portal_css()}
            </style>
        </head>
        <body>
            <div class="portal-container">
                <header class="portal-header">
                    <h1>Welcome, {user_profile.get('name', 'Friend')}</h1>
                    <div class="user-stats">
                        <div class="stat">Cognitive Score: {user_profile.get('cognitive_score', '--')}</div>
                        <div class="stat">Games Played: {user_profile.get('games_played', 0)}</div>
                        <div class="stat">Today's Goal: {self.get_daily_goal(user_profile)}</div>
                    </div>
                </header>
                
                <div class="game-categories">
                    {self.generate_category_sections(recommended_games)}
                </div>
                
                <div class="current-session">
                    <h2>Continue Playing</h2>
                    {self.generate_continue_section(user_profile)}
                </div>
                
                <div class="ai-companion">
                    <h2>Play with Marvin</h2>
                    <div class="ai-status">
                        <p>Marvin is ready to play! Choose a two-player game below.</p>
                        <button onclick="startAICompanionSession()">Start AI Companion Session</button>
                    </div>
                </div>
            </div>
            
            <script>
                {self.get_portal_js()}
            </script>
        </body>
        </html>
        '''
        
        return portal_html
    
    def generate_game_interface(self, game_id, user_profile, game_mode='single'):
        """
        Generate specific game interface
        """
        game_config = self.games_registry.get_game_config(game_id)
        
        # Choose appropriate template based on cognitive needs
        if user_profile.get('cognitive_impairment'):
            template = self.get_accessible_template(game_id)
        else:
            template = self.get_standard_template(game_id)
        
        # Inject adaptive elements
        adaptive_settings = self.calculate_adaptive_settings(
            game_id, user_profile, game_mode
        )
        
        game_html = template.format(
            game_title=game_config['name'],
            game_description=game_config['description'],
            adaptive_settings=json.dumps(adaptive_settings),
            user_profile=json.dumps(user_profile),
            ai_config=json.dumps(self.get_ai_opponent_config(user_profile))
        )
        
        return game_html