from pypresence import Presence
import time


client_id = "1332530522798297192"
RPC = Presence(client_id)
RPC.connect()
RPC.update(state="Rich Presence is working!", details="Details", large_image="large", small_image="small", large_text="Large Text", small_text="Small Text", start=time.time())

while True:
    time.sleep(15)