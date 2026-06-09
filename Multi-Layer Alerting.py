Emergency_Response_Layers = {
    'Layer_1': {
        'condition': 'mild_concern',
        'action': 'increase_monitoring',
        'notification': 'internal_log_only'
    },
    'Layer_2': {
        'condition': 'moderate_concern',
        'action': 'gentle_intervention',
        'notification': 'primary_caregiver'
    },
    'Layer_3': {
        'condition': 'serious_concern',
        'action': 'direct_intervention',
        'notification': 'all_caregivers'
    },
    'Layer_4': {
        'condition': 'emergency',
        'action': ['auto_dial_911', 'unlock_doors', 'alert_emergency_contacts'],
        'notification': 'emergency_services'
    }
}