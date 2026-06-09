# In your marvin_main.py
from marvin_social_glue import MarvinSocialGlue
from marvin_empathy import extract_emotion, get_social_intensity

glue = MarvinSocialGlue()

def handle_ai_response(user_input):
    # 1. Get the AI's text response (from your Llama-cpp or OpenAI call)
    ai_text = llm.generate_response(user_input)
    
    # 2. Extract the 'Social Cue'
    detected_emotion = extract_emotion(ai_text, source="ai")
    intensity = get_social_intensity(ai_text)
    
    # 3. Process through the Mirror Neuron Engine (Mirroring/Scaffolding)
    # This uses your logic to decide if Marvin should match you or lead you.
    social_decision = glue.mirror_engine.determine_appropriate_response(
        user_emotion=detected_emotion,
        user_profile={'age': 30} # Pull this from identity_stack_26TPOS.json
    )
    
    # 4. Update the physical "Face" on the RPi Screen
    glue.display.display_expression(
        social_decision['type'], 
        intensity=social_decision['intensity']
    )
    
    # 5. Finally, speak the text (TTS)
    speak(ai_text)