# Current: Monolithic complexity
# Improved: Microservices architecture

Proposed Structure:
- Core_AI_Engine (minimal, always running)
- Protocol_Manager (loads/unloads protocols as needed)
- Resource_Arbitrator (dynamic allocation)
- Safety_Monitor (always active, minimal footprint)
- Data_Manager (handles storage/retrieval)