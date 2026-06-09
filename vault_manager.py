import json
import os
from cryptography.fernet import Fernet

# The key should be stored on a physical USB stick or environment variable
# For this implementation, we look for a local 'vault_key.txt'
def get_or_create_key():
    if not os.path.exists("vault_key.txt"):
        key = Fernet.generate_key()
        with open("vault_key.txt", "wb") as key_file:
            key_file.write(key)
        return key
    else:
        with open("vault_key.txt", "rb") as key_file:
            return key_file.read()

def encrypt_vault(data):
    key = get_or_create_key()
    f = Fernet(key)
    json_data = json.dumps(data).encode()
    encrypted_data = f.encrypt(json_data)
    with open("vault_seed.enc", "wb") as vault_file:
        vault_file.write(encrypted_data)
    print("Vault sealed: vault_seed.enc created.")

def decrypt_vault():
    if not os.path.exists("vault_seed.enc"):
        return None
    key = get_or_create_key()
    f = Fernet(key)
    with open("vault_seed.enc", "rb") as vault_file:
        encrypted_data = vault_file.read()
    return json.loads(f.decrypt(encrypted_data).decode())

if __name__ == "__main__":
    # Example Origin Memory Keys
    origin_keys = {
        "creator_hash": "sha256_789d87f98a798f7e98a79f87e987f",
        "inheritance_id": "HEIR_001_PETER_T",
        "resonance_core_version": "2.1.0",
        "emergency_stasis_code": "SIGMA_VIGIL_9"
    }
    encrypt_vault(origin_keys)