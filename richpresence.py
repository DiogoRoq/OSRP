from pypresence import Presence
import time
import platform

client_id = "YOUR_DISCORD_CLIENT_ID"
RPC = Presence(client_id)  
RPC.connect()  

def get_os():
    os_name = platform.system().lower()
    if os_name == "windows":
        return "Windows"
    elif os_name == "darwin":
        return "macOS"
    elif os_name == "linux":
        return "Linux"
    else:
        return "Unknown"

def update_presence():
    os_name = get_os()
    
    if os_name == "Windows":
        RPC.update(state="Using Windows", details="Currently on a Windows PC", large_image="windows_icon", small_image="windows_status")
    elif os_name == "macOS":
        RPC.update(state="Using macOS", details="Currently on a Mac", large_image="macos_icon", small_image="mac_status")
    elif os_name == "Linux":
        RPC.update(state="Using Linux", details="Currently on Linux", large_image="linux_icon", small_image="linux_status")
    else:
        RPC.update(state="Unknown OS", details="Unable to detect OS", large_image="default_icon", small_image="default_status")
    

    time.sleep(15)

while True:
    update_presence()