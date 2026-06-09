class ActivityResourceProfiles:
    def __init__(self):
        self.profiles = {
            'tea_party_active': {
                'description': 'Interactive tea party with toys',
                'essential_tasks': [
                    'toy_recognition',
                    'child_emotion_detection',
                    'marvin_expression_render',
                    'ar_overlay_render',
                    'voice_interaction'
                ],
                'background_tasks': [
                    'behavioral_analysis_full',
                    'conversation_analysis',
                    'system_performance_logging',
                    'long_term_memory_update'
                ],
                'resource_allocation': {
                    'cpu': {'essential': 0.6, 'background': 0.2, 'reflection': 0.0},
                    'memory': {'essential': 0.7, 'background': 0.2, 'reflection': 0.0},
                    'npu': {'essential': 0.8, 'background': 0.1, 'reflection': 0.0}
                },
                'deferral_rules': {
                    'allow_deferral': True,
                    'max_deferral_time': 600,  # 10 minutes
                    'resumption_triggers': ['user_idle', 'activity_end']
                }
            },
            
            'creative_session': {
                'description': 'Drawing/coloring activity',
                'essential_tasks': [
                    'drawing_canvas_render',
                    'tool_interaction',
                    'color_palette_management',
                    'basic_ai_assistance'
                ],
                'background_tasks': [
                    'drawing_pattern_analysis',
                    'creative_style_learning',
                    'progress_tracking',
                    'therapeutic_benefit_analysis'
                ],
                'resource_allocation': {
                    'cpu': {'essential': 0.5, 'background': 0.3, 'reflection': 0.1},
                    'memory': {'essential': 0.6, 'background': 0.3, 'reflection': 0.0},
                    'npu': {'essential': 0.4, 'background': 0.3, 'reflection': 0.1}
                }
            },
            
            'crisis_emergency': {
                'description': 'Safety emergency detected',
                'essential_tasks': [
                    'safety_monitoring',
                    'emergency_response',
                    'alert_generation',
                    'user_state_assessment'
                ],
                'background_tasks': [],  # No background tasks during crisis
                'resource_allocation': {
                    'cpu': {'essential': 0.9, 'background': 0.0, 'reflection': 0.0},
                    'memory': {'essential': 0.9, 'background': 0.0, 'reflection': 0.0},
                    'npu': {'essential': 0.8, 'background': 0.0, 'reflection': 0.0}
                },
                'deferral_rules': {
                    'allow_deferral': False,
                    'max_deferral_time': 0,
                    'resumption_triggers': []
                }
            },
            
            'reflection_period': {
                'description': 'System idle, running reflection tasks',
                'essential_tasks': [
                    'system_health_monitoring',
                    'resource_cleanup'
                ],
                'background_tasks': [
                    'behavioral_analysis_full',
                    'performance_analysis',
                    'learning_model_updates',
                    'data_compression',
                    'storage_optimization'
                ],
                'resource_allocation': {
                    'cpu': {'essential': 0.2, 'background': 0.7, 'reflection': 0.1},
                    'memory': {'essential': 0.3, 'background': 0.6, 'reflection': 0.1},
                    'npu': {'essential': 0.1, 'background': 0.3, 'reflection': 0.4}
                }
            }
        }
        
    def get_profile(self, activity_type):
        """
        Get resource profile for specific activity
        """
        return self.profiles.get(activity_type, self.profiles['normal'])
    
    def adjust_profile_for_conditions(self, profile, system_conditions):
        """
        Adjust profile based on current system conditions
        """
        adjusted_profile = profile.copy()
        
        # Reduce resource allocation if thermal throttling
        if system_conditions.get('thermal_throttling'):
            for resource in adjusted_profile['resource_allocation']:
                for category in adjusted_profile['resource_allocation'][resource]:
                    adjusted_profile['resource_allocation'][resource][category] *= 0.7
        
        # Reduce background tasks if low memory
        if system_conditions.get('memory_pressure'):
            # Move some background tasks to reflection-only
            if len(adjusted_profile['background_tasks']) > 2:
                moved_tasks = adjusted_profile['background_tasks'][2:]
                adjusted_profile['background_tasks'] = adjusted_profile['background_tasks'][:2]
                adjusted_profile.setdefault('reflection_only_tasks', []).extend(moved_tasks)
        
        return adjusted_profile