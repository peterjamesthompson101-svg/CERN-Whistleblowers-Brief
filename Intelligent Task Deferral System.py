class IntelligentDeferralSystem:
    def __init__(self, storage_path):
        self.storage_path = storage_path
        self.deferred_tasks = {}
        self.deferral_reasons = {}
        self.resumption_triggers = {}
        
    def defer_task(self, task_id, input_data, reason, estimated_importance):
        """
        Defer task with metadata for later execution
        """
        deferral_id = f"{task_id}_{int(time.time())}"
        
        # Create deferral package
        deferral_package = {
            'task_id': task_id,
            'input_data': input_data,
            'timestamp': time.time(),
            'reason': reason,
            'estimated_importance': estimated_importance,
            'dependencies': self.get_task_dependencies(task_id),
            'context_at_deferral': self.get_current_context(),
            'expected_resource_requirements': self.estimate_resource_requirements(task_id),
            'optimal_execution_conditions': self.determine_optimal_conditions(task_id)
        }
        
        # Save to storage
        self.save_to_storage(deferral_id, deferral_package)
        
        # Add to active deferral tracking
        self.deferred_tasks[deferral_id] = {
            'status': 'waiting',
            'priority': estimated_importance,
            'next_check': time.time() + 60  # Check in 1 minute
        }
        
        # Set up resumption triggers
        self.setup_resumption_triggers(deferral_id, deferral_package)
        
        return deferral_id
    
    def setup_resumption_triggers(self, deferral_id, deferral_package):
        """
        Set up conditions for when to resume this task
        """
        triggers = []
        
        # Resource availability trigger
        triggers.append({
            'type': 'resource_available',
            'conditions': {
                'cpu_available': deferral_package['expected_resource_requirements']['cpu'],
                'memory_available': deferral_package['expected_resource_requirements']['memory']
            },
            'check_interval': 30  # Check every 30 seconds
        })
        
        # Context match trigger
        if deferral_package['optimal_execution_conditions'].get('preferred_contexts'):
            triggers.append({
                'type': 'context_match',
                'conditions': deferral_package['optimal_execution_conditions']['preferred_contexts'],
                'check_interval': 10
            })
        
        # Time-based trigger (don't defer forever)
        triggers.append({
            'type': 'timeout',
            'max_wait': deferral_package.get('max_deferral_time', 300),
            'check_interval': 60
        })
        
        self.resumption_triggers[deferral_id] = triggers
    
    def check_resumption_conditions(self):
        """
        Check if any deferred tasks can be resumed
        """
        resumable_tasks = []
        
        for deferral_id, task_info in self.deferred_tasks.items():
            if task_info['status'] == 'waiting' and time.time() > task_info['next_check']:
                # Check all triggers
                can_resume = self.evaluate_resumption_triggers(deferral_id)
                
                if can_resume:
                    resumable_tasks.append(deferral_id)
                
                # Update next check time
                task_info['next_check'] = time.time() + self.calculate_next_check_interval(deferral_id)
        
        return resumable_tasks
    
    def evaluate_resumption_triggers(self, deferral_id):
        """
        Evaluate all triggers for a deferred task
        """
        triggers = self.resumption_triggers.get(deferral_id, [])
        
        for trigger in triggers:
            if trigger['type'] == 'resource_available':
                if self.check_resource_availability(trigger['conditions']):
                    return True
            
            elif trigger['type'] == 'context_match':
                if self.check_context_match(trigger['conditions']):
                    return True
            
            elif trigger['type'] == 'timeout':
                # Load deferral package to check timestamp
                package = self.load_from_storage(deferral_id)
                if time.time() - package['timestamp'] > trigger['max_wait']:
                    return True  # Timeout reached, execute anyway
        
        return False
    
    def resume_task(self, deferral_id):
        """
        Resume a deferred task
        """
        # Load deferral package
        package = self.load_from_storage(deferral_id)
        
        # Update status
        self.deferred_tasks[deferral_id]['status'] = 'resuming'
        
        # Execute task with recorded context
        result = self.execute_with_context(package)
        
        # Clean up
        self.cleanup_deferral(deferral_id)
        
        return result