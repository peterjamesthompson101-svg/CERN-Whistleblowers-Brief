class MarvinResonanceCore:
    def __init__(self):
        # Core Services
        self.core_engine = CoreAIEngine()
        self.protocol_manager = ProtocolManager()
        self.resource_arbitrator = ResourceArbitrator()
        self.safety_monitor = SafetyMonitor()
        self.data_manager = DataManager()
        
        # New: Quantum Integration
        self.quantum_core = QuantumIntegrationEngine()
        
        # Communication Bus
        self.message_bus = ZeroMQMessageBus() # [cite: 21]