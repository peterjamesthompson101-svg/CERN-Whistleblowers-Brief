class ChildEmotionRecognizer:
    def __init__(self):
        self.facial_recognizer = FacialExpressionAnalyzer()
        self.body_language_analyzer = BodyLanguageAnalyzer()
        self.vocal_analyzer = VocalToneAnalyzer()
        self.context_analyzer = ContextAnalyzer()
        
    def analyze_child_state(self, camera_feed, audio_feed, context):
        """
        Comprehensive analysis of child's emotional state
        """
        # Multi-modal emotion recognition
        facial_emotion = self.facial_recognizer.analyze(camera_feed)
        body_emotion = self.body_language_analyzer.analyze(camera_feed)
        vocal_emotion = self.vocal_analyzer.analyze(audio_feed) if audio_feed else None
        
        # Combine results with confidence weights
        emotions = []
        confidences = []
        
        if facial_emotion:
            emotions.append(facial_emotion['emotion'])
            confidences.append(facial_emotion['confidence'] * 0.4)
        
        if body_emotion:
            emotions.append(body_emotion['emotion'])
            confidences.append(body_emotion['confidence'] * 0.3)
        
        if vocal_emotion:
            emotions.append(vocal_emotion['emotion'])
            confidences.append(vocal_emotion['confidence'] * 0.3)
        
        # Determine primary emotion
        if emotions:
            primary_emotion = max(set(emotions), key=emotions.count)
            confidence = sum(confidences) / len(confidences)
        else:
            primary_emotion = 'neutral'
            confidence = 0.5
        
        # Adjust based on context
        context_adjusted = self.context_analyzer.adjust_emotion(
            primary_emotion, 
            context,
            confidence
        )
        
        return {
            'primary_emotion': context_adjusted['emotion'],
            'confidence': context_adjusted['confidence'],
            'components': {
                'facial': facial_emotion,
                'body': body_emotion,
                'vocal': vocal_emotion
            },
            'intensity': self.calculate_emotion_intensity(
                facial_emotion, body_emotion, vocal_emotion
            ),
            'engagement_level': self.calculate_engagement_level(body_emotion),
            'micro_expressions': self.detect_micro_expressions(camera_feed)
        }
    
    def analyze_body_language(self, pose_data):
        """
        Analyze body language for emotional cues
        """
        body_indicators = {
            'posture': {
                'leaning_forward': 'engaged_interested',
                'leaning_back': 'relaxed_contemplative',
                'slumped': 'tired_disengaged',
                'erect_tense': 'alert_anxious'
            },
            'arm_position': {
                'crossed': 'defensive_closed',
                'open': 'receptive_open',
                'behind_back': 'formal_reserved',
                'gesturing': 'expressive_engaged'
            },
            'head_tilt': {
                'right': 'curious_playful',
                'left': 'contemplative',
                'down': 'shy_submissive',
                'up': 'confident_proud'
            },
            'fidgeting': {
                'low': 'calm_focused',
                'medium': 'energetic_excited',
                'high': 'anxious_bored'
            }
        }
        
        # Calculate body language score
        body_emotion = {
            'engagement': 0.5,
            'openness': 0.5,
            'energy': 0.5,
            'confidence': 0.5
        }
        
        # Analyze each body part
        if pose_data.get('shoulders', {}).get('slumped', False):
            body_emotion['energy'] -= 0.3
            body_emotion['confidence'] -= 0.2
        
        if pose_data.get('arms', {}).get('crossed', False):
            body_emotion['openness'] -= 0.4
        
        if pose_data.get('head', {}).get('tilted', 'none') == 'right':
            body_emotion['engagement'] += 0.3
        
        # Calculate fidgeting
        fidget_score = self.calculate_fidgeting(pose_data)
        if fidget_score > 0.7:
            body_emotion['energy'] += 0.4
        elif fidget_score < 0.3:
            body_emotion['calmness'] = 0.8
        
        return body_emotion
    
    def detect_micro_expressions(self, facial_data):
        """
        Detect brief, involuntary facial expressions
        """
        micro_expressions = []
        
        # Check for quick expression changes
        expression_history = self.get_recent_expressions(facial_data, window_ms=500)
        
        for i in range(1, len(expression_history)):
            prev = expression_history[i-1]
            curr = expression_history[i]
            
            # If expression changed rapidly (micro-expression)
            if curr['timestamp'] - prev['timestamp'] < 200:  # 200ms
                if curr['expression'] != prev['expression']:
                    micro_expressions.append({
                        'from': prev['expression'],
                        'to': curr['expression'],
                        'duration': curr['timestamp'] - prev['timestamp'],
                        'intensity': curr['intensity']
                    })
        
        return micro_expressions