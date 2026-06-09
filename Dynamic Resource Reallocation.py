class DynamicResourceReallocator:
    def __init__(self, resource_manager, activity_profiles):
        self.resource_manager = resource_manager
        self.activity_profiles = activity_profiles
        self.current_allocation = {}
        self.allocation_history = []
        
    def reallocate_for_activity(self, activity_type, urgency=0.5):
        """
        Reallocate resources for new activity
        """
        # Get profile for activity
        profile = self.activity_profiles.get_profile(activity_type)
        
        # Adjust based on urgency
        if urgency > 0.8:  # High urgency
            profile = self.boost_essential_resources(profile, 1.2)
        
        # Apply allocation
        self.apply_allocation(profile['resource_allocation'])
        
        # Update task priorities
        self.update_task_priorities_for_profile(profile)
        
        # Log reallocation
        self.log_reallocation(activity_type, profile)
        
        return profile
    
    def apply_allocation(self, allocation):
        """
        Apply resource allocation to system
        """
        for resource_type, categories in allocation.items():
            for category, percentage in categories.items():
                # Convert percentage to absolute based on system capacity
                absolute = self.percentage_to_absolute(resource_type, percentage)
                
                # Apply limits
                self.set_resource_limit(resource_type, category, absolute)
                
                # Update current allocation tracking
                self.current_allocation[f"{resource_type}_{category}"] = absolute
        
        # Save to history
        self.allocation_history.append({
            'timestamp': time.time(),
            'allocation': allocation,
            'system_state': self.get_system_state()
        })
    
    def update_task_priorities_for_profile(self, profile):
        """
        Update task priorities based on activity profile
        """
        # Boost essential tasks
        for task_id in profile['essential_tasks']:
            if task_id in self.resource_manager.task_registry:
                current_priority = self.resource_manager.task_registry[task_id].get('effective_priority', 50)
                new_priority = min(95, current_priority + 20)  # Boost but don't max out
                self.resource_manager.task_registry[task_id]['effective_priority'] = new_priority
        
        # Reduce background tasks
        for task_id in profile['background_tasks']:
            if task_id in self.resource_manager.task_registry:
                current_priority = self.resource_manager.task_registry[task_id].get('effective_priority', 50)
                new_priority = max(10, current_priority - 15)  # Reduce but keep minimal
                self.resource_manager.task_registry[task_id]['effective_priority'] = new_priority
        
        # Defer reflection-only tasks
        for task_id in profile.get('reflection_only_tasks', []):
            if task_id in self.resource_manager.task_registry:
                # Mark for deferral
                self.resource_manager.task_registry[task_id]['defer_until_reflection'] = True
    
    def monitor_and_adjust(self):
        """
        Continuously monitor and adjust resource allocation
        """
        # Check system conditions
        system_state = self.get_system_state()
        
        # Adjust for thermal conditions
        if system_state['cpu_temp'] > 75:
            self.reduce_allocation_for_thermal(0.7)  # Reduce to 70%
        
        # Adjust for memory pressure
        if system_state['memory_used'] > 0.9:  # 90% memory used
            self.reduce_background_allocation(0.5)  # Cut background in half
        
        # Check for idle periods to run reflection
        if self.detect_idle_period():
            self.trigger_reflection_period()
    
    def trigger_reflection_period(self):
        """
        Trigger reflection period when system is idle
        """
        # Save current state
        previous_state = {
            'allocation': self.current_allocation.copy(),
            'active_tasks': list(self.resource_manager.running_tasks.keys())
        }
        
        # Switch to reflection profile
        reflection_profile = self.activity_profiles.get_profile('reflection_period')
        self.reallocate_for_activity('reflection_period')
        
        # Run reflection for limited time
        reflection_duration = self.calculate_optimal_reflection_duration()
        
        # Start reflection timer
        self.start_reflection_timer(reflection_duration, previous_state)
    
    def start_reflection_timer(self, duration, previous_state):
        """
        Start timer to return to previous state after reflection
        """
        def return_to_previous():
            # Restore previous allocation
            self.apply_allocation(previous_state['allocation'])
            
            # Restore task priorities
            self.restore_task_priorities(previous_state['active_tasks'])
            
            # Process any reflection results
            self.process_reflection_results()
        
        # Schedule return
        threading.Timer(duration, return_to_previous).start()