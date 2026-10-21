import sys

# Import functions from your tested modules
try:
    import test as m1
except ImportError:
    print("[Error] Could not find test.py (Member 1 module). Ensure it is in C:\\myproject")
    sys.exit(1)

try:
    import member3 as m3
except ImportError:
    print("[Error] Could not find member3.py (Member 3 module). Ensure it is in C:\\myproject")
    sys.exit(1)

def show_banner():
    print("=" * 50)
    print("      PROJECT AEGIS - UNIFIED OS ASSISTANT       ")
    print("=" * 50)
    print(" [HARDWARE CONTROLS - MEMBER 1]")
    print("  1. Set Volume (Prompt for %)")
    print("  2. Toggle Mute")
    print("  3. Set Brightness (Prompt for %)")
    print("  4. Check Battery Status")
    print("  5. Lock Workstation")
    print("-" * 50)
    print(" [WORKSPACE SESSIONS - MEMBER 3]")
    print("  6. Save Workspace Snapshot")
    print("  7. View Saved Workspace")
    print("  8. Restore Workspace Apps")
    print("-" * 50)
    print("  0. Exit")
    print("=" * 50)

def main():
    while True:
        show_banner()
        choice = input("Enter option (0-8): ").strip()

        # Hardware Controls (Member 1)
        if choice == "1":
            try:
                vol = int(input("Enter volume percentage (0-100): "))
                m1.set_volume(vol)
            except ValueError:
                print("Invalid number. Please enter a valid integer.")
        elif choice == "2":
            m1.toggle_mute()
        elif choice == "3":
            try:
                bri = int(input("Enter brightness percentage (0-100): "))
                m1.set_brightness(bri)
            except ValueError:
                print("Invalid number. Please enter a valid integer.")
        elif choice == "4":
            m1.get_battery_info()
        elif choice == "5":
            confirm = input("Are you sure you want to lock the PC? (y/n): ").strip().lower()
            if confirm == "y":
                m1.lock_workstation()

        # Workspace Controls (Member 3)
        elif choice == "6":
            m3.save_workspace()
        elif choice == "7":
            m3.view_saved_workspace()
        elif choice == "8":
            m3.restore_workspace()

        # Exit
        elif choice == "0":
            print("\nShutting down Project Aegis Console. Goodbye!")
            break
        else:
            print("\nInvalid selection. Choose a number between 0 and 8.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()