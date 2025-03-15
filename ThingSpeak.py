import tkinter as tk
import requests

# ThingSpeak channel details
channel_id = "2877004"
write_api_key = "YOUR_WRITE_API_KEY"
read_api_key = "YOUR_READ_API_KEY"

# Function to send data to ThingSpeak
def send_data():
    field1_data = entry_field1.get()
    field2_data = entry_field2.get()
    url = f"https://api.thingspeak.com/update?api_key={write_api_key}&field1={field1_data}&field2={field2_data}"
    response = requests.post(url)
    if response.status_code == 200:
        status_label.config(text="Data sent successfully!")
    else:
        status_label.config(text="Error sending data.")

# Function to read data from ThingSpeak
def read_data():
   url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json?api_key={read_api_key}&results=1"
   response = requests.get(url)
   if response.status_code == 200:
       data = response.json()
       if data['feeds']:
            field1_value = data['feeds'][0]['field1']
            field2_value = data['feeds'][0]['field2']
            data_label.config(text=f"Field 1: {field1_value}, Field 2: {field2_value}")
       else:
           data_label.config(text="No data available.")
   else:
       data_label.config(text="Error reading data.")

# Tkinter window setup
window = tk.Tk()
window.title("ThingSpeak Interface")

# Widgets
label_field1 = tk.Label(window, text="Field 1:")
label_field1.grid(row=0, column=0)
entry_field1 = tk.Entry(window)
entry_field1.grid(row=0, column=1)

label_field2 = tkasinger.Label(window, text="Field 2:")
label_field2.grid(row=1, column=0)
entry_field2 = tk.Entry(window)
entry_field2.grid(row=1, column=1)

send_button = tk.Button(window, text="Send Data", command=send_data)
send_button.grid(row=2, column=0, columnspan=2)

read_button = tk.Button(window, text="Read Data", command=read_data)
read_button.grid(row=3, column=0, columnspan=2)

status_label = tk.Label(window, text="")
status_label.grid(row=4, column=0, columnspan=2)

data_label = tk.Label(window, text="")
data_label.grid(row=5, column=0, columnspan=2)

window.mainloop()