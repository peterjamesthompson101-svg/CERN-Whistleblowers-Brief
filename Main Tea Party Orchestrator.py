class InteractiveTeaPartyOrchestrator:
    def __init__(self, user_profile):
        self.user_profile = user_profile
        self.toy_recognition = ToyRecognitionEngine()
        self.emotion_recognizer = ChildEmotionRecognizer()
        self.emotion_mirroring = EmotionMirroringSystem()
        self.ar_manager = ARTeaPartyManager()
        self.conversation_system = ToyConversationSystem()
        self.marvin_expression = EmotionalExpressionEngine()
        
        self.session_state = {
            'phase': 'setup',
            'toys_present': [],
            'child_emotion_history': [],
            'tea_party_progress': 0.0,
            'magical_moments': []
        }
        
    def run_tea_party(self):
        """
        Main tea party orchestration loop
        """
        print("🎪 Welcome to Marvin's Magical Tea Party! 🎪")
        
        # Phase 1: Setup
        self.phase_setup()
        
        # Phase 2: Welcome & Introductions
        self.phase_welcome()
        
        # Phase 3: Tea Serving
        self.phase_serve_tea()
        
        # Phase 4: Conversation & Games
        self.phase_conversation_games()
        
        # Phase 5: Magical Moments
        self.phase_magical_moments()
        
        # Phase 6: Farewell
        self.phase_farewell()
        
    def phase_setup(self):
        """
        Child sets up physical toys for tea party
        """
        print("📦 Setup Phase: Place your toys for the tea party!")
        
        # Marvin gives instructions
        self.marvin_speak("Welcome! Let's set up our tea party. Place your favorite toys around you so I can see them all!")
        self.marvin_expression.display_expression('excited', intensity=0.8)
        
        # Wait for toys to be placed
        toys_placed = False
        while not toys_placed:
            frame = self.get_camera_frame()
            toys = self.toy_recognition.initialize_childs_toys(frame)
            
            if len(toys) >= 1:  # At least one toy
                self.session_state['toys_present'] = toys
                toys_placed = True
                
                # Celebrate
                self.marvin_speak(f"Wonderful! I see {len(toys)} friends joining us!")
                self.marvin_expression.display_expression('happy', intensity=0.9)
                self.play_sound('magical_chime')
            else:
                self.marvin_speak("I don't see any toys yet. Place them in front of the camera!")
                time.sleep(2)
        
        # Create AR scene
        ar_scene = self.ar_manager.setup_tea_party_scene(
            toys, 
            self.get_child_position()
        )
        
        self.session_state['ar_scene'] = ar_scene
        
        # Introduce each toy
        for toy in toys:
            self.introduce_toy(toy)
    
    def introduce_toy(self, toy):
        """
        Have Marvin introduce each toy with personality
        """
        introduction = f"""
        Oh look! It's {toy['personality']['name']}! 
        {toy['personality']['name']} is a {toy['type']} who loves {random.choice(toy['personality']['favorite_topics'])}.
        """
        
        self.marvin_speak(introduction)
        
        # Add AR overlay
        self.ar_manager.add_toy_overlay(toy['id'], toy['personality'])
        
        # Toy "greets" back
        time.sleep(1)
        toy_greeting = self.generate_toy_greeting(toy)
        self.speak_as_toy(toy, toy_greeting)
        
        # Marvin responds
        time.sleep(0.5)
        self.marvin_speak("So lovely to have you with us!")
    
    def phase_welcome(self):
        """
        Welcome ceremony with magical elements
        """
        print("👋 Welcome Phase")
        
        # Marvin gives welcome speech
        welcome_speech = """
        Welcome, everyone, to our magical tea party! 
        Today is special because we're all here together.
        Let's begin with a sprinkle of magic...
        """
        
        self.marvin_speak(welcome_speech)
        
        # Magical animation
        self.play_animation('sparkle_effect', duration=3)
        self.play_sound('magical_transformation')
        
        # Each toy gets "magically transformed" with AR
        for toy in self.session_state['toys_present']:
            self.ar_manager.activate_magical_overlay(toy['id'])
            time.sleep(0.5)
        
        # Check child's reaction
        child_emotion = self.get_child_emotion()
        self.session_state['child_emotion_history'].append(child_emotion)
        
        # Mirror child's emotion
        mirrored_response = self.emotion_mirroring.generate_mirrored_response(
            child_emotion, 
            self.user_profile
        )
        
        # Apply Marvin's expression
        self.apply_expression_sequence(mirrored_response['expression_sequence'])
        
        # Speak response
        self.marvin_speak(mirrored_response['verbal_response'])
    
    def phase_serve_tea(self):
        """
        Interactive tea serving with AR
        """
        print("☕ Tea Serving Phase")
        
        self.marvin_speak("Now, let's serve the tea! Watch carefully...")
        
        # Demonstrate pouring tea
        self.ar_manager.demo_tea_pouring()
        
        # Encourage child to pour for toys
        self.marvin_speak("Now you try! Make a pouring motion toward a toy's cup.")
        
        # Wait for child interaction
        interaction_detected = False
        start_time = time.time()
        
        while not interaction_detected and (time.time() - start_time) < 60:  # 1 minute timeout
            frame = self.get_camera_frame()
            child_gesture = self.analyze_child_gesture(frame)
            
            if child_gesture.get('type') == 'pouring':
                # Find which toy they're pouring for
                toy_id = self.determine_target_toy(child_gesture)
                
                if toy_id:
                    interaction_detected = True
                    
                    # AR feedback
                    result = self.ar_manager.handle_pouring_interaction(
                        child_gesture, 
                        toy_id
                    )
                    
                    # Toy responds
                    toy = next(t for t in self.session_state['toys_present'] if t['id'] == toy_id)
                    toy_response = self.generate_toy_thank_you(toy)
                    self.speak_as_toy(toy, toy_response)
                    
                    # Marvin praises
                    self.marvin_speak("Perfect pouring! What a wonderful host you are!")
                    self.marvin_expression.display_expression('proud', intensity=0.8)
                    
                    # Record magical moment
                    self.session_state['magical_moments'].append({
                        'type': 'tea_poured',
                        'toy': toy['personality']['name'],
                        'timestamp': time.time()
                    })
            
            time.sleep(0.1)
        
        if not interaction_detected:
            self.marvin_speak("That's okay! Let me help. Watch as I pour tea for everyone!")
            self.ar_manager.auto_pour_tea(self.session_state['toys_present'])
    
    def phase_conversation_games(self):
        """
        Interactive conversation and games with toys
        """
        print("💬 Conversation Phase")
        
        # Start conversation between toys
        conversation = self.conversation_system.facilitate_toy_conversation(
            self.session_state['toys_present'],
            self.get_child_emotion(),
            {'phase': 'tea_party'}
        )
        
        self.marvin_speak("Listen! Our friends are having a conversation!")
        
        # Play out conversation
        for line in conversation['conversation']:
            if line.get('type') == 'question_to_child':
                # Pause for child to respond
                self.speak_as_toy_by_id(line['toy'], line['dialogue'])
                
                # Listen for child response
                child_response = self.listen_for_child_response(timeout=10)
                
                if child_response:
                    # Have toy respond to child
                    toy_response = self.generate_toy_response_to_child(
                        line['toy'], 
                        child_response,
                        line['expected_response_type']
                    )
                    self.speak_as_toy_by_id(line['toy'], toy_response)
                else:
                    # Gentle prompt
                    self.marvin_speak(f"What do you think, {self.user_profile.get('name', 'friend')}?")
            else:
                # Regular conversation line
                self.speak_as_toy_by_id(line['toy'], line['dialogue'])
                time.sleep(line.get('duration', 2))
        
        # Play tea party games
        self.play_tea_party_games()
    
    def phase_magical_moments(self):
        """
        Create special magical moments based on child's interactions
        """
        print("✨ Magical Moments Phase")
        
        # Check for accumulated magical energy
        magical_energy = len(self.session_state['magical_moments'])
        
        if magical_energy >= 3:
            # Big magical transformation
            self.marvin_speak("Wow! I can feel the magic building up! Everyone, hold on!")
            
            # Magical transformation sequence
            self.play_animation('full_transformation', duration=5)
            self.play_sound('orchestral_magical')
            
            # All toys get enhanced AR effects
            for toy in self.session_state['toys_present']:
                self.ar_manager.apply_magical_transformation(toy['id'])
            
            # Special celebration
            self.marvin_expression.display_expression('robot_happy_dance', intensity=1.0)
            self.marvin_speak("Look at that! Our tea party has become truly magical!")
            
            # Fireworks
            self.ar_manager.create_fireworks_show()
            
        elif magical_energy >= 1:
            # Small magical moment
            self.marvin_speak("I feel something magical happening!")
            
            # Sparkle effect on favorite toy
            favorite_toy = self.determine_favorite_toy()
            if favorite_toy:
                self.ar_manager.apply_sparkle_effect(favorite_toy['id'])
                self.play_sound('sparkle_twinkle')
                
                self.marvin_speak(f"Look! {favorite_toy['personality']['name']} is glowing with happiness!")
    
    def phase_farewell(self):
        """
        Farewell ceremony
        """
        print("👋 Farewell Phase")
        
        # Check child's emotion
        child_emotion = self.get_child_emotion()
        
        if child_emotion['primary_emotion'] in ['sad', 'reluctant']:
            self.marvin_speak("It looks like you're sad the party is ending. We can play again soon!")
            self.marvin_expression.display_expression('compassionate', intensity=0.8)
        else:
            self.marvin_speak("What a wonderful tea party that was!")
            self.marvin_expression.display_expression('happy', intensity=0.9)
        
        # Each toy says goodbye
        for toy in self.session_state['toys_present']:
            goodbye_message = self.generate_toy_goodbye(toy, child_emotion)
            self.speak_as_toy(toy, goodbye_message)
            time.sleep(1)
        
        # Final message from Marvin
        final_message = f"""
        Thank you for the lovely tea party, {self.user_profile.get('name', 'friend')}!
        You were a wonderful host.
        Remember, your friends are always here for another party.
        Until next time!
        """
        
        self.marvin_speak(final_message)
        
        # Wave goodbye animation
        self.marvin_expression.display_expression('content', intensity=0.7)
        self.play_animation('wave_goodbye', duration=3)
        
        # Save tea party memory
        self.save_tea_party_memory()