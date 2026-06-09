Interface_Modes = {
    'Level_1': {  # Severe cognitive impairment
        'buttons': 3,
        'text_size': 'extra_large',
        'voice_only': True,
        'auto_proceed': True
    },
    'Level_2': {  # Moderate impairment
        'buttons': 6,
        'text_size': 'large',
        'voice_primary': True,
        'simple_choices': True
    },
    'Level_3': {  # Mild impairment
        'buttons': 12,
        'text_size': 'medium',
        'mixed_interface': True,
        'guided_flow': True
    },
    'Level_4': {  # Caregiver/Professional
        'full_interface': True,
        'advanced_settings': True,
        'monitoring_dashboard': True
    }
}