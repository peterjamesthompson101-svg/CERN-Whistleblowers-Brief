class ContextAwareScheduler:
    def __init__(self, resource_manager):
        self.resource_manager = resource_manager
        self.context_history = deque(maxlen=100)
        self.context_transition_times = {}
        self.active_context = {
            'primary': 'normal',
            'secondary': [],
            'stability_score': 1.0,
            'duration': 0
        }
        
    def update_context(self, sensor_data, user_interaction, system_state):
        """
        Determine current context based on multiple inputs
        """
        new_context = {
            'primary': self.determine_primary_context(sensor_data, user_interaction),
            'secondary': self.determine_secondary_contexts(sensor_data, user_interaction),
            'stability_score': self.calculate_context_stability(),
            'duration': self.calculate_context_duration(),
            'transition_likelihood': self.calculate_transition_likelihood()
        }
        
        # Log context transition
        if new_context['primary'] != self.active_context['primary']:
            self.log_context_transition(self.active_context, new_context)
        
        self.active_context = new_context
        self.context_history.append(new_context)
        
        # Update task priorities based on new context
        self.adjust_task_priorities_for_context()
        
        return new_context
    
    def determine_primary_context(self, sensor_data, user_interaction):
        """
        Determine the primary operational context
        """
        # Check for safety emergencies
        if self.detect_safety_emergency(sensor_data):
            return 'crisis_emergency'
        
        # Check for user-engaged activities
        if user_interaction.get('activity_type') == 'tea_party':
            return 'tea_party_active'
        elif user_interaction.get('activity_type') == 'drawing':
            return 'creative_session'
        elif user_interaction.get('activity_type') == 'game_playing':
            return 'game_session'
        
        # Check for therapeutic states
        if sensor_data.get('user_emotional_state') in ['distressed', 'anxious']:
            return 'therapeutic_support'
        
        # Check for learning opportunities
        if self.detect_learning_opportunity(user_interaction):
            return 'learning_opportunity'
        
        # Default based on time and patterns
        return self.determine_default_context()
    
    def determine_secondary_contexts(self, sensor_data, user_interaction):
        """
        Determine secondary contexts that modify primary behavior
        """
        secondary_contexts = []
        
        # Add resource-aware contexts
        hardware_state = self.resource_manager.hardware_monitor.get_state()
        if hardware_state['cpu_temp'] > 70:
            secondary_contexts.append('thermal_throttling')
        if hardware_state['cpu_usage'] > 85:
            secondary_contexts.append('high_load')
        
        # Add user state contexts
        if sensor_data.get('user_attention_level', 0.5) < 0.3:
            secondary_contexts.append('low_attention')
        if sensor_data.get('user_engagement', 0.5) > 0.8:
            secondary_contexts.append('high_engagement')
        
        # Add environmental contexts
        if sensor_data.get('ambient_noise', 0) > 70:  # dB
            secondary_contexts.append('noisy_environment')
        if sensor_data.get('ambient_light', 0) < 20:  # lux
            secondary_contexts.append('low_light')
        
        return secondary_contexts
    
    def adjust_task_priorities_for_context(self):
        """
        Adjust all task priorities based on current context
        """
        for task_id in self.resource_manager.task_registry:
            new_priority = self.resource_manager.calculate_dynamic_priority(
                task_id, 
                self.active_context
            )
            
            # Update task's effective priority
            self.resource_manager.task_registry[task_id]['effective_priority'] = new_priority
            
            # If task is running and should be suspended
            if task_id in self.resource_manager.running_tasks:
                if self.should_suspend_task(task_id):
                    self.suspend_task_for_reflection(task_id)