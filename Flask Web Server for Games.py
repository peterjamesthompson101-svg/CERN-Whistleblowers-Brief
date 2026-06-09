from flask import Flask, render_template, jsonify, session, request
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

class GamePortalServer:
    def __init__(self):
        self.active_games = {}
        self.user_sessions = {}
        
    @app.route('/')
    def portal_home():
        """Main portal page"""
        user_id = session.get('user_id', 'guest')
        user_profile = self.load_user_profile(user_id)
        return render_template('portal_home.html', 
                             user_profile=user_profile,
                             games=self.get_available_games(user_profile))
    
    @app.route('/game/<game_id>')
    def game_page(game_id):
        """Individual game page"""
        user_id = session.get('user_id', 'guest')
        user_profile = self.load_user_profile(user_id)
        game_config = self.get_game_config(game_id)
        
        return render_template(f'games/{game_id}.html',
                             game_config=game_config,
                             user_profile=user_profile,
                             adaptive_settings=self.calculate_adaptive_settings(
                                 game_id, user_profile
                             ))
    
    @app.route('/api/game/start', methods=['POST'])
    def start_game():
        """API endpoint to start a game"""
        data = request.json
        game_id = data['game_id']
        user_id = session.get('user_id')
        game_mode = data.get('mode', 'single')
        
        # Initialize game
        game_instance = self.create_game_instance(
            game_id, user_id, game_mode
        )
        
        game_session_id = self.generate_session_id()
        self.active_games[game_session_id] = game_instance
        
        return jsonify({
            'session_id': game_session_id,
            'game_state': game_instance.initial_state,
            'instructions': game_instance.instructions
        })
    
    @socketio.on('game_move')
    def handle_game_move(data):
        """Handle real-time game moves"""
        session_id = data['session_id']
        move = data['move']
        
        if session_id in self.active_games:
            game = self.active_games[session_id]
            
            # Process user move
            result = game.process_move(move)
            
            # If two-player with AI, get AI response
            if game.mode == 'two_player_ai':
                ai_response = game.ai_opponent.generate_response(
                    game.state, move, game.user_profile
                )
                result['ai_move'] = ai_response
            
            # Emit updated game state
            emit('game_update', {
                'session_id': session_id,
                'game_state': game.state,
                'result': result
            })
            
            # Update learning models
            self.update_learning_models(game, move, result)
    
    @app.route('/api/adaptive_adjust', methods=['POST'])
    def adaptive_adjustment():
        """Endpoint for real-time difficulty adjustment"""
        data = request.json
        session_id = data['session_id']
        adjustment_type = data['type']
        
        if session_id in self.active_games:
            game = self.active_games[session_id]
            game.adjust_difficulty(adjustment_type)
            
            return jsonify({
                'new_difficulty': game.difficulty,
                'adjustment_made': adjustment_type
            })