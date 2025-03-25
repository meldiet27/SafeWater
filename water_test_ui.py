import tkinter as tk
from tkinter import Toplevel, messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
import threading
import time
import serial
import itertools  # For rotating spinner animation

# Configure serial connection to Arduino (Update port as needed)
try:
    arduino = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)  # Change to correct port
    time.sleep(2)  # Allow connection to initialize
    print("Arduino connected!")
except Exception as e:
    print(f"Could not connect to Arduino: {e}")
    arduino = None  # Handle case where Arduino isn't connected

# ThingSpeak channel details
channel_id = "2877004"
read_api_key = "00YSVLHONG1542DI"

# Function to check if ThingSpeak is receiving data
def check_sensor_connection():
    url = f"https://api.thingspeak.com/channels/2877004/feeds.json?api_key=00YSVLHONG1542DI&results=1"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['feeds'] and data['feeds'][0]['field1'] is not None:
            return True  # Sensor is working
    return False  # Sensor is not sending data

# Show a loading screen with an animated spinner
def show_loading_screen():
    loading_window = Toplevel(root)
    loading_window.title("Measuring...")
    loading_window.geometry("250x150")
    loading_window.resizable(False, False)

    label = tk.Label(loading_window, text="Measuring...\nPlease wait", font=("Glacial-Indifference", 14))
    label.pack(pady=20)

    spinner_label = tk.Label(loading_window, font=("Glacial-Indifference", 20))
    spinner_label.pack()

    spinner_frames = itertools.cycle(["◐", "◓", "◑", "◒"])  # Spinner animation cycle

    def update_spinner():
        spinner_label.config(text=next(spinner_frames))
        loading_window.after(200, update_spinner)  # Update every 200ms

    update_spinner()
    root.update()
    return loading_window  # Return the window to close it later

# Function to start measurement
def start_measurement():
    if arduino:
        loading_screen = show_loading_screen()  # Show loading popup
        arduino.write(b"START\n")  # Send start command to Arduino
        print("Measurement started!")
        
        time.sleep(3)  # Simulate delay for data upload

        if not check_sensor_connection():
            loading_screen.destroy()
            messagebox.showerror("Sensor Error", "Sensor is not connected or not sending data!")
            return

        loading_screen.destroy()  # Close loading popup
        open_sensor_data_screen()  # Open the data screen
    else:
        messagebox.showerror("Connection Error", "Arduino is not connected!")

# Function to open sensor data screen and display readings
def open_sensor_data_screen():
    """Open a new window to display real-time sensor data graph."""
    data_window = Toplevel(root)
    data_window.title("Sensor Data")
    data_window.geometry("375x667")
    data_window.resizable(False, False)

    # Load background image
    data_bg_image = Image.open("backgroundblue.jpg").resize((375, 667))
    data_bg_photo = ImageTk.PhotoImage(data_bg_image)

    data_canvas = tk.Canvas(data_window, width=375, height=667)
    data_canvas.pack(fill="both", expand=True)
    data_canvas.create_image(187, 333, image=data_bg_photo, anchor="center")
    data_window.bg_photo = data_bg_photo

    # Create Matplotlib figure
    fig, ax = plt.subplots(figsize=(3.5, 2.5), dpi=100)
    time_values = []
    sensor_values = []

    def update_graph():
        """Update graph with real-time sensor data."""
        while True:
            sensor_value = fetch_sensor_data()  # Get latest data from ThingSpeak
            if sensor_value is not None:
                time_values.append(len(time_values) * 0.5)
                sensor_values.append(sensor_value)
                ax.clear()
                ax.plot(time_values, sensor_values, marker="o", linestyle="-", color="blue", label="pH Levels")
                ax.set_title("Sensor Data Over Time", fontsize=12, fontweight="bold")
                ax.set_xlabel("Time (s)")
                ax.set_ylabel("pH Level")
                ax.legend()
                ax.grid(True)
                canvas_graph.draw()
            time.sleep(5)  # Update every 5 seconds

    # Embed Matplotlib graph in Tkinter
    canvas_graph = FigureCanvasTkAgg(fig, master=data_window)
    canvas_graph.draw()
    graph_widget = canvas_graph.get_tk_widget()
    graph_widget.place(x=20, y=150)

    # Start data update in a separate thread
    threading.Thread(target=update_graph, daemon=True).start()

    # Add "Back" button
    back_button = tk.Button(data_window, text="Back", command=data_window.destroy, font=("Glacial-Indifference", 14), bg="white")
    data_canvas.create_window(187, 600, window=back_button)

# Function to fetch the latest data from ThingSpeak
def fetch_sensor_data():
    url = f"https://api.thingspeak.com/channels/2877004/feeds.json?api_key=00YSVLHONG1542DI&results=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['feeds']:
            sensor_data = data['feeds'][0]['field1']
            return float(sensor_data) if sensor_data is not None else None
    return None

# Create main window
root = tk.Tk()
root.title("Water Testing App")
root.geometry("375x667")  
root.resizable(False, False)

# Load background image
bg_image = Image.open("Raster.png").resize((375, 667))
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=375, height=667)
canvas.pack(fill="both", expand=True)
canvas.create_image(187, 333, image=bg_photo, anchor="center")

# Load logo
logo_image = Image.open("safewaterlogo.png").resize((100, 100))
logo_photo = ImageTk.PhotoImage(logo_image)
canvas.create_image(187, 80, image=logo_photo, anchor="center")

# Title Text
canvas.create_text(187, 160, text="SafeWater Monitor", font=("Glacial-Indifference", 20, "bold"), fill="black")
canvas.create_text(187, 200, text="Pure Water, Pure Peace\nSafeguarding Your Health, One Drop at a Time", 
                   font=("Glacial-Indifference", 14), fill="black", anchor ="center", justify="center" )

# Start Measurement Button (Checks connection first)

start_button = tk.Button(root, text="Start Measurement", font=("Glacial-Indifference", 16, "bold"), fg="white", width=20, height =2, relief="ridge", bd=3, command=start_measurement)
canvas.create_window(187, 300, window=start_button)

# Run Tkinter event loop
root.mainloop()
