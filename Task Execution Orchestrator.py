class ThreeLayerTaskOrchestrator:
    def __init__(self, resource_manager):
        self.resource_manager = resource_manager
        self.execution_layers = {
            'real_time': {
                'max_tasks': 3,
                'priority_threshold': 80,
                'tasks': {},
                'resources': {'cpu': 0.4, 'memory': 0.5}
            },
            'near_real_time': {
                'max_tasks': 5,
                'priority_threshold': 60,
                'tasks': {},
                'resources': {'cpu': 0.3, 'memory': 0.3}
            },
            'background': {
                'max_tasks': 10,
                'priority_threshold': 30,
                'tasks': {},
                'resources': {'cpu': 0.2, 'memory': 0.1}
            }
        }
        
    def execute_task(self, task_id, input_data=None):
        """
        Execute task in appropriate layer based on priority and resources
        """
        task = self.resource_manager.task_registry[task_id]
        priority = task.get('effective_priority', task['base_priority'])
        
        # Determine execution layer
        if priority >= self.execution_layers['real_time']['priority_threshold']:
            layer = 'real_time'
        elif priority >= self.execution_layers['near_real_time']['priority_threshold']:
            layer = 'near_real_time'
        else:
            layer = 'background'
        
        # Check if layer has capacity
        if not self.layer_has_capacity(layer):
            # Try to move to higher layer if possible
            layer = self.find_available_layer(priority)
            if not layer:
                # No capacity - defer task
                return self.defer_task(task_id, input_data)
        
        # Execute in selected layer
        return self.execute_in_layer(task_id, layer, input_data)
    
    def execute_in_layer(self, task_id, layer, input_data):
        """
        Execute task with layer-specific resource constraints
        """
        task_config = self.resource_manager.task_registry[task_id]
        
        # Create constrained execution environment
        constraints = self.execution_layers[layer]['resources']
        
        if layer == 'real_time':
            # Execute immediately with priority
            result = self.execute_realtime(task_config['function'], input_data, constraints)
            
        elif layer == 'near_real_time':
            # Execute with small delay
            result = self.execute_near_realtime(task_config['function'], input_data, constraints)
            
        else:  # background
            # Execute when resources available
            result = self.execute_background(task_config['function'], input_data, constraints)
        
        # Track execution
        self.track_execution_metrics(task_id, layer, result)
        
        return result
    
    def execute_realtime(self, task_function, input_data, constraints):
        """
        Execute with real-time constraints
        """
        # Apply CPU limiting
        with CPULimiter(constraints['cpu']):
            # Apply memory limiting
            with MemoryLimiter(constraints['memory'] * 1024):  # Convert to MB
                # Execute with timeout
                try:
                    result = task_function(input_data)
                    return {'status': 'success', 'result': result, 'layer': 'real_time'}
                except TimeoutError:
                    return {'status': 'timeout', 'layer': 'real_time', 'suggested': 'defer'}
                except Exception as e:
                    return {'status': 'error', 'error': str(e), 'layer': 'real_time'}
    
    def execute_background(self, task_function, input_data, constraints):
        """
        Execute in background with checkpointing
        """
        # Save input data to disk
        checkpoint_id = self.create_checkpoint(input_data)
        
        # Execute in low-priority thread
        def background_worker():
            try:
                # Load from checkpoint
                loaded_data = self.load_checkpoint(checkpoint_id)
                
                # Execute with aggressive limits
                with CPULimiter(constraints['cpu'] * 0.5):  # Use half of allocated
                    result = task_function(loaded_data)
                
                # Save result for later retrieval
                self.save_result(checkpoint_id, result)
                
                # Cleanup
                self.delete_checkpoint(checkpoint_id)
                
            except Exception as e:
                # Log error for reflection analysis
                self.log_background_error(checkpoint_id, str(e))
        
        # Start background thread
        thread = threading.Thread(target=background_worker, daemon=True)
        thread.start()
        
        return {
            'status': 'deferred',
            'checkpoint_id': checkpoint_id,
            'layer': 'background',
            'estimated_completion': self.estimate_completion_time(task_function)
        }