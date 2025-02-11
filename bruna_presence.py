from pypresence import Presence
import time as std_time  # Use alias to avoid conflicts
import datetime
import random
import threading
import tkinter as tk
from tkinter import ttk
from datetime import timezone
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")  # Now loaded securely from .env

# ---------------------- Discord Rich Presence Setup ---------------------- #
RPC = Presence(CLIENT_ID)
RPC.connect()

# Fun statuses for when Bruna is NOT working
FUN_STATUSES = [
    {"state": "Bruna is not working", "details": "Just one more...for you sylus...❤️"},
    {"state": "Bruna is not working", "details": "Casual light smut reading time 😇"},
    {"state": "Bruna is not working", "details": "404: Motivation Not Found 😴"},
]

# Define working days (all days except Thursday and Friday) and working hours (8 AM to 5 PM GMT)
WORKING_DAYS = {"Monday", "Tuesday", "Wednesday", "Saturday", "Sunday"}
WORK_START_HOUR = 8   # 8 AM GMT
WORK_END_HOUR = 17    # 5 PM GMT

def get_status():
    """
    Determines current status based on the current UTC time.
    If it's a working day and within working hours, it returns the working status.
    Otherwise, it returns a random fun status.
    """
    now = datetime.datetime.now(timezone.utc)  # Get current UTC time
    day_name = now.strftime("%A")
    
    # If it's a working day and within working hours, use working status.
    if day_name in WORKING_DAYS and WORK_START_HOUR <= now.hour < WORK_END_HOUR:
        return {"state": "Bruna is working 👩‍💻", "details": "Unavailable 8 AM - 5 PM GMT"}
    
    # Otherwise, choose a random fun status.
    return random.choice(FUN_STATUSES)

# Global variables for manual override via the GUI
manual_override = False
manual_status = {"state": "N/A", "details": "N/A"}

def update_presence_loop():
    """
    Continuously updates the Discord Rich Presence every 30 seconds.
    Uses manual status if the override flag is active; otherwise, uses the scheduled status.
    """
    global manual_override, manual_status
    while True:
        status = manual_status if manual_override else get_status()

        try:
            RPC.update(
                state=status["state"],
                details=status["details"],
                large_image="your_large_image_key",  # Replace with your uploaded image key
                small_image="your_small_image_key",  # Replace with your uploaded image key
                start=int(std_time.time()),  # Current Unix timestamp
                buttons=[{"label": "Bruna's LinkedIn", "url": "https://www.linkedin.com/in/bruna"}]
            )
            print(f"Updated status: {status}")
        except Exception as e:
            print(f"Error updating status: {e}")
        std_time.sleep(30)

# ---------------------- GUI Setup with Tkinter ---------------------- #
def set_manual_status():
    """
    Reads the state and details from the text fields,
    sets the manual status, and activates the manual override.
    """
    global manual_override, manual_status
    state_text = state_entry.get().strip()
    details_text = details_entry.get().strip()
    if state_text and details_text:
        manual_status = {"state": state_text, "details": details_text}
        manual_override = True
        status_label.config(text="Manual override is active.")
    else:
        status_label.config(text="Please enter both a state and details.")

def reset_to_automatic():
    """
    Disables the manual override so that the automated status takes over.
    """
    global manual_override
    manual_override = False
    status_label.config(text="Automatic status is active.")

# Create the main Tkinter window
root = tk.Tk()
root.title("Discord Rich Presence Control")

# Create a frame to hold the widgets
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky="NSEW")

# Labels and entry fields for the manual status
ttk.Label(frame, text="State:").grid(row=0, column=0, sticky="W")
state_entry = ttk.Entry(frame, width=50)
state_entry.grid(row=0, column=1, pady=5)

ttk.Label(frame, text="Details:").grid(row=1, column=0, sticky="W")
details_entry = ttk.Entry(frame, width=50)
details_entry.grid(row=1, column=1, pady=5)

# Buttons to set manual status or revert to automatic mode
set_manual_btn = ttk.Button(frame, text="Set Manual Status", command=set_manual_status)
set_manual_btn.grid(row=2, column=0, pady=5)

reset_btn = ttk.Button(frame, text="Reset to Automatic", command=reset_to_automatic)
reset_btn.grid(row=2, column=1, pady=5)

# A label to display the current mode
status_label = ttk.Label(frame, text="Automatic status is active.")
status_label.grid(row=3, column=0, columnspan=2, pady=10)

# Start the update loop in a background thread (daemon so it closes with the GUI)
update_thread = threading.Thread(target=update_presence_loop, daemon=True)
update_thread.start()

# Start the Tkinter event loop
root.mainloop()
