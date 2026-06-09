import subprocess

def check_hailo():
    try:
        result = subprocess.run(['hailortcli', 'scan'], capture_output=True, text=True)
        return "Device" in result.stdout
    except FileNotFoundError:
        return False

if check_hailo():
    print("AI Kit Found: Enabling 26 TOPS NPU for Whisper Acceleration.")
    # Integration logic for Hailo-optimized Whisper would be called here
else:
    print("AI Kit Not Found: Falling back to CPU-only processing.")