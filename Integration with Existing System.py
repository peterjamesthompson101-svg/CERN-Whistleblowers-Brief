class ARMEIntegration:
    def __init__(self, marvin_core):
        self.marvin_core = marvin_core
        self.resource_manager = AdaptiveResourceManager(
            marvin_core.hardware_monitor,
            marvin_core.context_engine
        )
        self.scheduler = ContextAwareScheduler(self.resource_manager)
        self.orchestrator = ThreeLayerTaskOrchestrator(self.resource_manager)
        self.deferral_system = IntelligentDeferralSystem('deferred_tasks')
        self.reflection_engine = ReflectionEngine('reflection_data', {
            'behavioral': BehavioralAnalysisModule(),
            'performance': SystemPerformanceAnalysisModule(),
            'interaction': InteractionAnalysisModule()
        })
        
        # Register all existing tasks
        self.register_all_tasks()
        
    def register_all_tasks(self):
        """
        Register all system tasks with resource profiles
        """
        tasks = {
            # Tea party tasks
            'toy_recognition': {
                'function': self.marvin_core.toy_recognition.recognize_toys,
                'base_priority': 85,
                'context_sensitivity': {
                    'tea_party_active': 1.0,
                    'normal': 0.3,
                    'reflection_period': 0.1
                },
                'deferrable': True,
                'max_deferral_time': 300,
                'reflection_analysis': True,
                'essential_override': ['crisis_emergency']
            },
            
            'child_emotion_detection': {
                'function': self.marvin_core.emotion_recognizer.analyze,
                'base_priority': 90,
                'context_sensitivity': {
                    'tea_party_active': 1.0,
                    'creative_session': 0.8,
                    'crisis_emergency': 1.0,
                    'normal': 0.5
                },
                'deferrable': False,  # Never defer emotion detection
                'reflection_analysis': True
            },
            
            # Drawing program tasks
            'drawing_canvas_render': {
                'function': self.marvin_core.drawing_engine.render,
                'base_priority': 80,
                'context_sensitivity': {
                    'creative_session': 1.0,
                    'normal': 0.2
                },
                'deferrable': True,
                'max_deferral_time': 600
            },
            
            # Safety tasks
            'safety_monitoring': {
                'function': self.marvin_core.safety_monitor.check,
                'base_priority': 95,  # Always high
                'context_sensitivity': {
                    'crisis_emergency': 1.0,
                    'tea_party_active': 0.9,
                    'creative_session': 0.9,
                    'normal': 0.8,
                    'reflection_period': 0.8
                },
                'deferrable': False,  # Never defer safety
                'essential_override': ['all']  # Essential in all contexts
            }
        }
        
        for task_id, config in tasks.items():
            self.resource_manager.register_task(task_id, config)
    
    def execute_with_priority(self, task_id, input_data=None):
        """
        Execute task with priority management
        """
        # Check if task should be deferred
        current_context = self.scheduler.active_context
        
        if self.should_defer_task(task_id, current_context):
            # Defer with appropriate priority
            deferral_priority = self.calculate_deferral_priority(task_id, current_context)
            deferral_id = self.deferral_system.defer_task(
                task_id, 
                input_data,
                reason='context_not_optimal',
                estimated_importance=deferral_priority
            )
            return {'status': 'deferred', 'deferral_id': deferral_id}
        
        # Execute with appropriate resource allocation
        return self.orchestrator.execute_task(task_id, input_data)
    
    def run_system_cycle(self):
        """
        Main system cycle with adaptive resource management
        """
        # 1. Update context
        context = self.scheduler.update_context(
            self.marvin_core.get_sensor_data(),
            self.marvin_core.get_user_interaction(),
            self.marvin_core.get_system_state()
        )
        
        # 2. Check for deferred tasks that can resume
        resumable = self.deferral_system.check_resumption_conditions()
        for deferral_id in resumable:
            self.deferral_system.resume_task(deferral_id)
        
        # 3. Check if reflection should run
        if self.should_run_reflection():
            insights = self.reflection_engine.run_reflection_cycle()
            if insights:
                self.apply_reflection_insights(insights)
        
        # 4. Monitor and adjust resource allocation
        self.resource_manager.monitor_and_adjust()
        
        # 5. Log current state for future reflection
        self.log_system_state_for_reflection(context)