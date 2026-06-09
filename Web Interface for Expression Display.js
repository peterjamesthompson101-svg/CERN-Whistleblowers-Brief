// Frontend expression display system
class WebExpressionDisplay {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.layers = {};
        this.currentExpression = 'neutral';
        this.animationLoop = null;
        
        this.initializeLayers();
        this.setupEventListeners();
    }
    
    initializeLayers() {
        this.layers = {
            background: new Layer('background', 0),
            face: new Layer('face', 1),
            eyes: new Layer('eyes', 2),
            mouth: new Layer('mouth', 3),
            eyebrows: new Layer('eyebrows', 4),
            accessories: new Layer('accessories', 5),
            effects: new Layer('effects', 6)
        };
    }
    
    setExpression(expressionName, intensity = 1.0) {
        const expression = EXPRESSION_LIBRARY[expressionName];
        
        if (!expression) {
            console.error(`Expression ${expressionName} not found`);
            return;
        }
        
        this.currentExpression = expressionName;
        
        // Clear previous animations
        this.stopAllAnimations();
        
        // Apply expression with intensity
        this.applyExpression(expression, intensity);
        
        // Start animation loop
        this.startAnimationLoop();
    }
    
    applyExpression(expression, intensity) {
        // Adjust expression parameters based on intensity
        const adjusted = this.adjustIntensity(expression, intensity);
        
        // Render each component
        this.renderFaceBase(adjusted.face);
        this.renderEyes(adjusted.eyes);
        this.renderMouth(adjusted.mouth);
        this.renderEyebrows(adjusted.eyebrows);
        
        // Add accessories
        if (adjusted.accessories) {
            this.renderAccessories(adjusted.accessories);
        }
        
        // Start animations
        this.startComponentAnimations(adjusted.animations);
    }
    
    renderEyes(eyeConfig) {
        // Draw eye shapes
        const leftEye = this.drawEye(
            'left',
            eyeConfig.shape,
            eyeConfig.position.left
        );
        
        const rightEye = this.drawEye(
            'right',
            eyeConfig.shape,
            eyeConfig.position.right
        );
        
        // Apply eye animations
        if (eyeConfig.animation) {
            this.animateEyes(leftEye, rightEye, eyeConfig.animation);
        }
        
        // Add tears if needed
        if (eyeConfig.teardrop) {
            this.renderTears(eyeConfig.teardrop);
        }
        
        // Add sparkles
        if (eyeConfig.sparkle) {
            this.addEyeSparkles(leftEye, rightEye);
        }
    }
    
    renderTears(teardropConfig) {
        // Create tear animation
        const tearAnimation = {
            startY: -20,
            endY: this.canvas.height + 20,
            speed: teardropConfig.speed || 2,
            count: teardropConfig.count || 1,
            size: teardropConfig.size || 'medium'
        };
        
        // Create tear particles
        for (let i = 0; i < tearAnimation.count; i++) {
            const tear = this.createTearParticle(tearAnimation);
            this.layers.effects.addParticle(tear);
        }
    }
    
    // Fireworks effect
    renderFireworks(count = 10) {
        for (let i = 0; i < count; i++) {
            setTimeout(() => {
                this.createFireworkBurst(
                    this.randomCanvasPosition(),
                    this.randomColor()
                );
            }, i * 200); // Staggered start
        }
    }
    
    // Robot dance animation
    renderRobotDance() {
        const dancePatterns = [
            'robot_wave',
            'robot_shuffle',
            'robot_spin',
            'robot_jump'
        ];
        
        // Sequence of dance moves
        const danceSequence = [
            { pattern: 'robot_wave', duration: 2000 },
            { pattern: 'robot_shuffle', duration: 1500 },
            { pattern: 'robot_spin', duration: 3000 },
            { pattern: 'robot_jump', duration: 1000 }
        ];
        
        this.executeDanceSequence(danceSequence);
    }
}

// WebSocket integration for real-time expression updates
class ExpressionWebSocket {
    constructor(serverUrl) {
        this.ws = new WebSocket(serverUrl);
        this.display = new WebExpressionDisplay('marvinFace');
        
        this.setupWebSocket();
    }
    
    setupWebSocket() {
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            switch (data.type) {
                case 'expression':
                    this.display.setExpression(data.expression, data.intensity);
                    break;
                    
                case 'effect':
                    this.display[`render${data.effect}`]();
                    break;
                    
                case 'dance':
                    this.display.renderRobotDance();
                    break;
                    
                case 'mirror_emotion':
                    this.display.mirrorUserEmotion(data.emotion);
                    break;
            }
        };
    }
    
    sendUserEmotion(emotion) {
        // Send user's detected emotion to server
        this.ws.send(JSON.stringify({
            type: 'user_emotion',
            emotion: emotion,
            timestamp: Date.now()
        }));
    }
}