import re

def extract_emotion(text, source="ai"):
    """
    Analyzes text to find the dominant emotional tone.
    Source can be 'ai' (what Marvin says) or 'user' (what you said).
    """
    text = text.lower()
    
    # 1. Manual "Reflex" Triggers (High Speed)
    # These map directly to the keys in your Animated Expression System Architecture.py
    lexicon = {
        'happy': ['wonderful', 'joy', 'glad', 'excite', 'celebrate', 'haha', ':)'],
        'sad': ['sorry', 'unfortunate', 'grief', 'lonely', 'sad', 'mourn', ':('],
        'thinking': ['perhaps', 'consider', 'analyze', 'wonder', 'curious', 'hmm'],
        'robot_happy_dance': ['success', 'complete', 'victory', 'done', 'tada']
    }

    # Check for direct matches
    for emotion, keywords in lexicon.items():
        if any(word in text for word in keywords):
            return emotion

    # 2. Heuristic Logic for "Social Cues"
    if "?" in text:
        return 'thinking' # Raising an eyebrow for questions
    
    if "!" in text:
        return 'happy' # High energy/intensity

    # 3. Default State
    return 'neutral'

def get_social_intensity(text):
    """
    Determines how 'big' the facial expression should be (0.0 to 1.0).
    Based on punctuation and caps.
    """
    intensity = 0.5
    if "!" in text: intensity += 0.3
    if text.isupper(): intensity += 0.2
    return min(intensity, 1.0)