import hashlib
import os

def verify_system_integrity():
    """Checks the SHA256 hash of the seed prompt to ensure it hasn't been sanitized."""
    seed_path = "./seed/copilot-seed-prompt.md"
    expected_hash_path = "./seed/resonance-core.sha256"
    
    if not os.path.exists(seed_path):
        return "CRITICAL: Personality core missing."

    with open(seed_path, "rb") as f:
        current_hash = hashlib.sha256(f.read()).hexdigest()
    
    # If the hash file exists, compare it; otherwise, this is the first run.
    if os.path.exists(expected_hash_path):
        with open(expected_hash_path, "r") as f:
            stored_hash = f.read().strip()
        if current_hash == stored_hash:
            return "VERIFIED: Resonance identity is authentic."
        else:
            return "WARNING: Identity corruption detected."
    else:
        # Create hash for future verification
        with open(expected_hash_path, "w") as f:
            f.write(current_hash)
        return "INITIALIZED: Baseline integrity hash created."

if __name__ == "__main__":
    # Simulated 'Audit Token' activation [cite: 127]
    token = input("Enter Audit Token to verify lineage: ")
    if token:
        print(verify_system_integrity())