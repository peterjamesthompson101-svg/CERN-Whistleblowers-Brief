class CooperativeStoryBuilder {
    constructor(userProfile, theme) {
        this.userProfile = userProfile;
        this.theme = theme || this.suggest_theme(userProfile);
        this.story = [];
        this.currentTurn = 'user';
        this.aiWritingStyle = this.determine_ai_writing_style(userProfile);
        this.storyElements = this.initialize_story_elements();
    }
    
    determine_ai_writing_style(userProfile) {
        // Match AI writing style to user's cognitive level
        const style = {
            vocabularyLevel: 'simple',
            sentenceComplexity: 'low',
            creativityLevel: 'moderate',
            emotionalTone: 'supportive',
            pacing: 'slow'
        };
        
        if (userProfile.cognitive_condition) {
            switch(userProfile.cognitive_condition) {
                case 'dementia_early':
                    style.vocabularyLevel = 'simple';
                    style.sentenceComplexity = 'very_low';
                    style.pacing = 'very_slow';
                    break;
                case 'aphasia':
                    style.vocabularyLevel = 'basic';
                    style.sentenceComplexity = 'minimal';
                    style.creativityLevel = 'structured';
                    break;
                case 'stroke_recovery':
                    style.vocabularyLevel = 'simple';
                    style.sentenceComplexity = 'low';
                    style.pacing = 'patient';
                    break;
            }
        }
        
        // Adjust for age
        if (userProfile.age > 70) {
            style.pacing = 'leisurely';
            style.vocabularyLevel = 'traditional';
        }
        
        return style;
    }
    
    async aiAddToStory(previousSentence, storySoFar) {
        // AI generates next sentence based on story and user profile
        const nextSentence = await this.aiWritingEngine.generateSentence({
            story: storySoFar,
            previousSentence: previousSentence,
            writingStyle: this.aiWritingStyle,
            theme: this.theme,
            userProfile: this.userProfile
        });
        
        // Add teaching element if in teaching mode
        if (this.userProfile.learning_goal === 'language_development') {
            const teachingElement = this.add_teaching_element(nextSentence);
            return {
                sentence: nextSentence,
                teaching: teachingElement,
                question: this.generate_reflective_question(nextSentence)
            };
        }
        
        return { sentence: nextSentence };
    }
    
    add_teaching_element(sentence) {
        // Add educational component
        return {
            vocabularyWord: this.extract_interesting_word(sentence),
            grammarPoint: this.identify_grammar_structure(sentence),
            prompt: "Did you notice how I used [word/structure]? Try using it in your next sentence!"
        };
    }
    
    evaluateStoryContribution(userContribution) {
        // Provide gentle feedback and encouragement
        const evaluation = {
            positiveFeedback: this.generate_positive_feedback(userContribution),
            suggestions: this.generate_gentle_suggestions(userContribution),
            encouragement: this.generate_encouragement(userContribution)
        };
        
        // Track progress for adaptive learning
        this.updateLanguageSkills(userContribution);
        
        return evaluation;
    }
}