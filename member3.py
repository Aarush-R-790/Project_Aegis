import os
import sqlite3
import subprocess
import psutil
import pygetwindow as gw

DB_NAME = "workspace.db"

def init_db():
    """Initializes the SQLite database table for storing session snapshots."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS session_snapshot (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            process_name TEXT,
            executable_path TEXT,
            window_title TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_workspace():
    """Scans open visible windows and saves their executable paths to SQLite."""
    init_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Clear previous snapshot before saving the current state
    cursor.execute("DELETE FROM session_snapshot")

    visible_windows = gw.getAllWindows()
    saved_paths = set()
    saved_count = 0

    # Build a lookup map of running processes
    proc_map = {}
    for proc in psutil.process_iter(['name', 'exe']):
        try:
            name = proc.info['name']
            exe = proc.info['exe']
            if name and exe:
                proc_map[name.lower()] = exe
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Match visible windows with process executables
    for win in visible_windows:
        title = win.title.strip()
        if not title or not win.visible:
            continue

        for proc_name_lower, exe_path in proc_map.items():
            base_name = proc_name_lower.replace(".exe", "")
            if (base_name in title.lower() or title.lower() in base_name) and exe_path not in saved_paths:
                cursor.execute("""
                    INSERT INTO session_snapshot (process_name, executable_path, window_title)
                    VALUES (?, ?, ?)
                """, (proc_name_lower, exe_path, title))
                saved_paths.add(exe_path)
                saved_count += 1
                break

    conn.commit()
    conn.close()
    print(f"\n[Workspace] Snapshot saved! Recorded {saved_count} running application(s) into '{DB_NAME}'.")

def view_saved_workspace():
    """Displays all applications currently stored in the snapshot database."""
    init_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, process_name, executable_path, window_title FROM session_snapshot")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("\n[Workspace] Database is empty. No apps saved yet.")
        return

    print("\n--- Current Saved Workspace ---")
    for row in rows:
        print(f"ID: {row[0]} | Process: {row[1]} | Title: {row[3]}")
        print(f"    Path: {row[2]}")
    print("--------------------------------")

def restore_workspace():
    """Relaunches applications recorded in the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT executable_path, process_name FROM session_snapshot WHERE executable_path IS NOT NULL")
    apps = cursor.fetchall()
    conn.close()

    if not apps:
        print("\n[Workspace] Nothing to restore. Please save a snapshot first.")
        return

    print(f"\n[Workspace] Restoring {len(apps)} application(s)...")
    for exe_path, name in apps:
        if os.path.exists(exe_path):
            try:
                print(f" -> Launching {name}...")
                subprocess.Popen([exe_path], shell=True)
            except Exception as e:
                print(f" -> Failed to launch {name}: {e}")
        else:
            print(f" -> Path not found on system: {exe_path}")

if __name__ == "__main__":
    print("\n=== Member 3: Workspace & Session Manager ===")
    print("1. Save Current Workspace (Snapshot)")
    print("2. View Saved Snapshot")
    print("3. Restore / Relaunch Workspace")
    print("0. Exit")

    while True:
        choice = input("\nEnter choice (0-3): ").strip()
        if choice == "1":
            save_workspace()
        elif choice == "2":
            view_saved_workspace()
        elif choice == "3":
            restore_workspace()
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")