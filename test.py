import ctypes
import subprocess
import screen_brightness_control as sbc
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def get_audio_endpoint():
    """Retrieves the IAudioEndpointVolume interface handling all pycaw version structures."""
    speaker = AudioUtilities.GetSpeakers()
    
    # 1. Check if newer pycaw helper exists directly on speaker object
    if hasattr(speaker, 'EndpointVolume'):
        return speaker.EndpointVolume
    
    # 2. Check modern wrapper where underlying IMMDevice is speaker.dev or speaker._dev
    raw_device = getattr(speaker, 'dev', getattr(speaker, '_dev', None))
    if raw_device is not None:
        interface = raw_device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        return interface.QueryInterface(IAudioEndpointVolume)
        
    # 3. Legacy pycaw direct activation
    interface = speaker.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return interface.QueryInterface(IAudioEndpointVolume)

def set_volume(percent: int):
    volume = get_audio_endpoint()
    scalar = max(0.0, min(1.0, percent / 100.0))
    volume.SetMasterVolumeLevelScalar(scalar, None)
    print(f"[Audio] Volume set to {percent}%")

def toggle_mute():
    volume = get_audio_endpoint()
    current_mute = volume.GetMute()
    volume.SetMute(not current_mute, None)
    print(f"[Audio] Muted: {not current_mute}")

def set_brightness(percent: int):
    level = max(0, min(100, int(percent)))
    sbc.set_brightness(level)
    print(f"[Display] Brightness set to {level}%")

def lock_workstation():
    print("[System] Locking PC via user32.dll...")
    ctypes.windll.user32.LockWorkStation()

def get_battery_info():
    cmd = "Get-CimInstance -ClassName Win32_Battery | Select-Object -ExpandProperty EstimatedChargeRemaining"
    result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
    charge = result.stdout.strip()
    if charge:
        print(f"[Subprocess] Battery remaining: {charge}%")
    else:
        print("[Subprocess] Desktop / AC power connected (no battery detected).")

if __name__ == "__main__":
    print("\n=== Member 1: Hardware Controller ===")
    print("1. Set Volume to 40%")
    print("2. Toggle Mute")
    print("3. Set Brightness to 70%")
    print("4. Check Battery via Subprocess")
    print("5. Lock Workstation")
    print("0. Exit")

    while True:
        choice = input("\nEnter choice (0-5): ").strip()
        if choice == "1":
            set_volume(40)
        elif choice == "2":
            toggle_mute()
        elif choice == "3":
            set_brightness(70)
        elif choice == "4":
            get_battery_info()
        elif choice == "5":
            lock_workstation()
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")