import os
import json

class DiscoveryEngine:
    def __init__(self, root_path="/home/samantha/ghost"):
        self.root_path = root_path
        self.registry_file = os.path.join(root_path, "config/protocol_registry.json")
        
        self.found_modules = {
            "logic_modules": [],       # .py, .js (Protocols/Engines)
            "foundations": [],         # .odt, .pdf, .txt, .md
            "configurations": [],       # .yaml, .json
            "interface_assets": [],    # .html
            "unrecognized": []
        }

    def scan_file_system(self):
        print(f"Marvin is scanning path: {self.root_path}")
        for root, dirs, files in os.walk(self.root_path):
            if 'marvin_env' in root or '.git' in root:
                continue
            for file in files:
                full_path = os.path.join(root, file)
                self.categorize_file(full_path)
        
        self.save_registry()
        return self.found_modules

    def categorize_file(self, path):
        ext = os.path.splitext(path)[1].lower()
        filename = os.path.basename(path).lower()

        if ext in ['.py', '.js']:
            if any(key in filename for key in ['protocol', 'engine', 'bridge']):
                self.found_modules["logic_modules"].insert(0, path)
            else:
                self.found_modules["logic_modules"].append(path)
        elif ext in ['.odt', '.pdf', '.txt', '.md']:
            self.found_modules["foundations"].append(path)
        elif ext in ['.yaml', '.json']:
            self.found_modules["configurations"].append(path)
        elif ext == '.html':
            self.found_modules["interface_assets"].append(path)
        else:
            self.found_modules["unrecognized"].append(path)

    def save_registry(self):
        os.makedirs(os.path.dirname(self.registry_file), exist_ok=True)
        with open(self.registry_file, 'w') as f:
            json.dump(self.found_modules, f, indent=4)
        total = sum(len(v) for v in self.found_modules.values())
        print(f"Discovery Complete: {total} files registered in {self.registry_file}")

if __name__ == "__main__":
    engine = DiscoveryEngine()
    engine.scan_file_system()
