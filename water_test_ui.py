import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np  # For generating sample sensor data

# Create main window
root = tk.Tk()
root.title("Water Testing App")
root.geometry("375x667")  # Fixed size like a mobile app
root.resizable(False, False)

# Load and set background image
bg_image = Image.open("backgroundblue.jpg")  # Replace with your actual image file
bg_image = bg_image.resize((375, 667))  # Resize to match window size
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=375, height=667)
canvas.pack(fill="both", expand=True)

# Set background image
canvas.create_image(187, 333, image=bg_photo, anchor="center")

# Load and place logo
logo_image = Image.open("safewaterlogo.png")  # Replace with your actual logo filename
logo_image = logo_image.resize((100, 100))  # Resize logo if needed
logo_photo = ImageTk.PhotoImage(logo_image)
canvas.create_image(187, 80, image=logo_photo, anchor="center")

# Title Text (Centered)
canvas.create_text(187, 160, text="SafeWater Monitor", font=("Helvetica", 20, "bold"), fill="black")

# Subtitle Text (Centered)
canvas.create_text(187, 200, text="Pure Water, Pure Peace\nSafeguarding Your Health, One Drop at a Time", 
                   font=("Helvetica", 14), fill="black")

# Function to open "Sensor Data" screen with a graph
def open_sensor_data_screen():
    data_window = Toplevel(root)
    data_window.title("Sensor Data")
    data_window.geometry("375x667")
    data_window.resizable(False, False)

    # Load background image for consistency
    data_bg_image = Image.open("backgroundblue.jpg")  
    data_bg_image = data_bg_image.resize((375, 667))
    data_bg_photo = ImageTk.PhotoImage(data_bg_image)

    # Canvas for background
    data_canvas = tk.Canvas(data_window, width=375, height=667)
    data_canvas.pack(fill="both", expand=True)
    data_canvas.create_image(187, 333, image=data_bg_photo, anchor="center")

    # Keep reference to avoid garbage collection
    data_window.bg_photo = data_bg_photo

    # Placeholder sensor data (replace this with actual sensor data)
    time = np.linspace(0, 10, 50)  # Simulating time in seconds
    sensor_values = np.sin(time) * 10 + 50  # Simulating some sensor readings

    # Create Matplotlib figure
    fig, ax = plt.subplots(figsize=(3.5, 2.5), dpi=100)  
    ax.plot(time, sensor_values, marker="o", linestyle="-", color="blue", label="pH Levels")
    ax.set_title("Sensor Data Over Time", fontsize=12, fontweight="bold")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("pH Level")
    ax.legend()
    ax.grid(True)

    # Embed Matplotlib graph in Tkinter
    canvas_graph = FigureCanvasTkAgg(fig, master=data_window)
    canvas_graph.draw()
    graph_widget = canvas_graph.get_tk_widget()
    graph_widget.place(x=20, y=150)  # Adjust position

    # Function to close the sensor data window
    def close_data_window():
        data_window.destroy()

    # Add "Back" button
    back_button = tk.Button(data_window, text="Back", command=close_data_window, font=("Helvetica", 14), bg="white")
    data_canvas.create_window(187, 600, window=back_button)  # Center the button

# Create Start Measurement Button (Opens Sensor Data Screen)
start_button = tk.Button(root, text="Start Measurement", font=("Helvetica", 14), bg="white", command=open_sensor_data_screen)
canvas.create_window(187, 300, window=start_button)  # Adjusted Y position

# Run Tkinter event loop
root.mainloop()




