import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial
import threading
import time

# Set up serial connection (Adjust 'COM4' based on your port)
arduino = serial.Serial(port='/dev/cu.wlan-debug', baudrate=115200, timeout=0.1)

def read_sensor_data():
    """Read real-time sensor data from Arduino."""
    try:
        arduino.write(bytes("read", 'utf-8'))  # Send request to Arduino
        time.sleep(0.05)  # Allow Arduino time to respond
        data = arduino.readline().decode().strip()
        if data:
            return float(data)
        return None
    except Exception as e:
        print(f"Error reading sensor data: {e}")
        return None

# Create main window
root = tk.Tk()
root.title("Water Testing App")
root.geometry("375x667")  # Fixed size like a mobile app
root.resizable(False, False)

# Load and set background image
bg_image = Image.open("backgroundblue.jpg")  # Replace with actual image
bg_image = bg_image.resize((375, 667))
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=375, height=667)
canvas.pack(fill="both", expand=True)
canvas.create_image(187, 333, image=bg_photo, anchor="center")

# Load and place logo
logo_image = Image.open("safewaterlogo.png")  # Replace with actual logo filename
logo_image = logo_image.resize((100, 100))
logo_photo = ImageTk.PhotoImage(logo_image)
canvas.create_image(187, 80, image=logo_photo, anchor="center")

# Title Text
canvas.create_text(187, 160, text="SafeWater Monitor", font=("Helvetica", 20, "bold"), fill="black")
canvas.create_text(187, 200, text="Pure Water, Pure Peace\nSafeguarding Your Health, One Drop at a Time", 
                   font=("Helvetica", 14), fill="black")

def open_sensor_data_screen():
    """Open a new window to display real-time sensor data graph."""
    data_window = Toplevel(root)
    data_window.title("Sensor Data")
    data_window.geometry("375x667")
    data_window.resizable(False, False)

    # Load background image
    data_bg_image = Image.open("backgroundblue.jpg")
    data_bg_image = data_bg_image.resize((375, 667))
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
            sensor_value = read_sensor_data()
            if sensor_value is not None:
                time_values.append(len(time_values) * 0.5)  # Timestamp (in seconds)
                sensor_values.append(sensor_value)
                ax.clear()
                ax.plot(time_values, sensor_values, marker="o", linestyle="-", color="blue", label="pH Levels")
                ax.set_title("Sensor Data Over Time", fontsize=12, fontweight="bold")
                ax.set_xlabel("Time (s)")
                ax.set_ylabel("pH Level")
                ax.legend()
                ax.grid(True)
                canvas_graph.draw()
            time.sleep(0.5)

    # Embed Matplotlib graph in Tkinter
    canvas_graph = FigureCanvasTkAgg(fig, master=data_window)
    canvas_graph.draw()
    graph_widget = canvas_graph.get_tk_widget()
    graph_widget.place(x=20, y=150)

    # Start data update in a separate thread
    threading.Thread(target=update_graph, daemon=True).start()

    # Add "Back" button
    back_button = tk.Button(data_window, text="Back", command=data_window.destroy, font=("Helvetica", 14), bg="white")
    data_canvas.create_window(187, 600, window=back_button)

# Create Start Measurement Button
start_button = tk.Button(root, text="Start Measurement", font=("Helvetica", 14), bg="white", command=open_sensor_data_screen)
canvas.create_window(187, 300, window=start_button)

# Run Tkinter event loop
root.mainloop()




