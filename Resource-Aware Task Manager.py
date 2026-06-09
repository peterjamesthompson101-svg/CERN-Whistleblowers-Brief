class AdaptiveResourceManager:
    def __init__(self, hardware_monitor, context_engine):
        self.hardware_monitor = hardware_monitor
        self.context_engine = context_engine
        self.task_registry = {}
        self.running_tasks = {}
        self.deferred_tasks = Queue()
        self.reflection_queue = Queue()
        self.resource_pools = {
            'critical': {'cpu': 0.3, 'memory': 0.4, 'npu': 0.2},
            'essential': {'cpu': 0.4, 'memory': 0.4, 'npu': 0.3},
            'background': {'cpu': 0.2, 'memory': 0.1, 'npu': 0.1},
            'reflection': {'cpu': 0.1, 'memory': 0.1, 'npu': 0.0}
        }
        
    def register_task(self, task_id, task_config):
        """
        Register a task with its resource profile and priority rules
        """
        self.task_registry[task_id] = {
            'function': task_config['function'],
            'base_priority': task_config.get('base_priority', 50),
            'resource_profile': self.calculate_resource_profile(task_config),
            'context_sensitivity': task_config.get('context_sensitivity', {}),
            'deferrable': task_config.get('deferrable', True),
            'max_deferral_time': task_config.get('max_deferral_time', 300),
            'reflection_analysis': task_config.get('reflection_analysis', True),
            'essential_override': task_config.get('essential_override', []),
            'performance_metrics': {
                'avg_execution_time': 0,
                'avg_cpu_usage': 0,
                'avg_memory_usage': 0,
                'success_rate': 1.0
            }
        }
    
    def calculate_dynamic_priority(self, task_id, current_context):
        """
        Calculate real-time priority based on context and system state
        """
        task = self.task_registry[task_id]
        
        # Base priority
        priority = task['base_priority']
        
        # Context adjustment
        context_boost = self.calculate_context_boost(task_id, current_context)
        priority += context_boost * 20
        
        # Resource availability adjustment
        resource_factor = self.calculate_resource_factor(task_id)
        priority *= resource_factor
        
        # Urgency factor (how long deferred)
        if task_id in self.deferred_tasks:
            urgency = self.calculate_urgency(task_id)
            priority += urgency * 10
        
        # Safety override (essential functions always high)
        if self.is_essential_in_context(task_id, current_context):
            priority = min(priority, 90)  # Cap at 90 for essential
        
        return max(1, min(100, priority))
    
    def calculate_context_boost(self, task_id, current_context):
        """
        Determine how important this task is in current context
        """
        task = self.task_registry[task_id]
        sensitivity = task['context_sensitivity']
        
        # Check for direct context match
        if current_context['primary'] in sensitivity:
            return sensitivity[current_context['primary']]
        
        # Check for secondary context relevance
        for secondary_context in current_context.get('secondary', []):
            if secondary_context in sensitivity:
                return sensitivity[secondary_context] * 0.7
        
        # Default low relevance
        return 0.1
    
    def is_essential_in_context(self, task_id, current_context):
        """
        Check if task is essential in current context (cannot be deferred)
        """
        task = self.task_registry[task_id]
        essential_contexts = task.get('essential_override', [])
        
        # Always essential contexts
        always_essential = ['crisis', 'emergency', 'safety_breach']
        
        return (current_context['primary'] in always_essential or 
                current_context['primary'] in essential_contexts)