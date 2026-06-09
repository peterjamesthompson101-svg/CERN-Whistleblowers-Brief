class MemoryMatrixGame {
    constructor(userProfile, difficulty) {
        this.userProfile = userProfile;
        this.difficulty = this.calculate_initial_difficulty(userProfile, difficulty);
        this.gridSize = this.calculate_grid_size();
        this.patterns = [];
        this.currentRound = 1;
        this.aiOpponent = new AIMemoryOpponent(userProfile);
    }
    
    calculate_initial_difficulty(userProfile, baseDifficulty) {
        let difficulty = baseDifficulty;
        
        // Adjust for cognitive condition
        const condition = userProfile.cognitive_condition;
        const adjustments = {
            'dementia_early': 0.6,
            'dementia_moderate': 0.4,
            'dementia_advanced': 0.2,
            'alzheimers_early': 0.5,
            'alzheimers_moderate': 0.3,
            'normal_aging': 0.8
        };
        
        difficulty *= adjustments[condition] || 0.7;
        
        // Adjust for age
        const age = userProfile.age || 65;
        if (age > 80) difficulty *= 0.7;
        else if (age > 70) difficulty *= 0.8;
        else if (age > 60) difficulty *= 0.9;
        
        return Math.max(0.1, Math.min(1.0, difficulty));
    }
    
    calculate_grid_size() {
        // Start with small grid for cognitive impairment
        if (this.difficulty < 0.3) return { rows: 3, cols: 3 };
        if (this.difficulty < 0.5) return { rows: 4, cols: 4 };
        if (this.difficulty < 0.7) return { rows: 5, cols: 5 };
        return { rows: 6, cols: 6 };
    }
    
    generatePattern() {
        const patternLength = Math.floor(3 + (this.difficulty * 7));
        const pattern = [];
        
        for (let i = 0; i < patternLength; i++) {
            pattern.push({
                row: Math.floor(Math.random() * this.gridSize.rows),
                col: Math.floor(Math.random() * this.gridSize.cols),
                color: this.get_color_for_difficulty(),
                duration: this.get_duration_for_difficulty()
            });
        }
        
        this.patterns.push(pattern);
        return pattern;
    }
    
    get_color_for_difficulty() {
        // Simpler colors for lower difficulty
        const colorSets = {
            'easy': ['#FF6B6B', '#4ECDC4', '#FFD166'], // High contrast
            'medium': ['#FF6B6B', '#4ECDC4', '#FFD166', '#06D6A0', '#118AB2'],
            'hard': ['#FF6B6B', '#4ECDC4', '#FFD166', '#06D6A0', '#118AB2', 
                    '#073B4C', '#EF476F', '#7209B7']
        };
        
        if (this.difficulty < 0.4) return colorSets.easy;
        if (this.difficulty < 0.7) return colorSets.medium;
        return colorSets.hard;
    }
    
    get_duration_for_difficulty() {
        // Longer display for lower difficulty
        return 2000 - (this.difficulty * 1500);
    }
    
    async playTwoPlayerWithAI() {
        // AI makes its move
        const aiPattern = await this.aiOpponent.generateResponse(
            this.patterns,
            this.currentRound,
            this.difficulty
        );
        
        // Present both patterns (user's and AI's)
        const results = await this.comparePatterns(userPattern, aiPattern);
        
        // Update difficulty based on performance
        this.updateDifficulty(results);
        
        // Generate AI commentary
        const commentary = this.aiOpponent.generateCommentary(
            results,
            this.userProfile
        );
        
        return {
            results,
            commentary,
            newDifficulty: this.difficulty,
            aiPattern: aiPattern
        };
    }
}