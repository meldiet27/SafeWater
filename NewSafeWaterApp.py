import tkinter as tk
from tkinter import Toplevel, messagebox, ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
import threading
import time
import serial
import itertools
from tkinterweb import HtmlFrame

# Configure serial connection to Arduino
try:
    arduino = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)  # Change to correct port
    time.sleep(2)
    print("Arduino connected!")
except Exception as e:
    print(f"Could not connect to Arduino: {e}")
    arduino = None

# ThingSpeak channel details
channel_id = "2877004"
read_api_key = "00YSVLHONG1542DI"

def check_sensor_connection():
    url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json?api_key={read_api_key}&results=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['feeds'] and data['feeds'][0]['field1'] is not None:
            return True
    return False

def show_loading_screen():
    loading_window = Toplevel(root)
    loading_window.title("Measuring...")
    loading_window.geometry("250x150")
    loading_window.resizable(False, False)

    label = tk.Label(loading_window, text="Measuring...\nPlease wait", font=("Glacial-Indifference", 14))
    label.pack(pady=20)

    spinner_label = tk.Label(loading_window, font=("Glacial-Indifference", 20))
    spinner_label.pack()

    spinner_frames = itertools.cycle(["\u25d0", "\u25d3", "\u25d1", "\u25d2"])

    def update_spinner():
        spinner_label.config(text=next(spinner_frames))
        loading_window.after(200, update_spinner)

    update_spinner()
    root.update()
    return loading_window

def start_measurement():
    if arduino:
        loading_screen = show_loading_screen()
        arduino.write(b"START\n")
        print("Measurement started!")
        time.sleep(3)

        if not check_sensor_connection():
            loading_screen.destroy()
            messagebox.showerror("Sensor Error", "Sensor is not connected or not sending data!")
            return

        loading_screen.destroy()
        open_sensor_data_screen()
    else:
        messagebox.showerror("Connection Error", "Arduino is not connected!")

def open_sensor_data_screen():
    data_window = Toplevel(root)
    data_window.title("Sensor Data")
    data_window.geometry("375x667")
    data_window.resizable(False, False)

    data_bg_image = Image.open("backgroundblue.jpg").resize((375, 667))
    data_bg_photo = ImageTk.PhotoImage(data_bg_image)
    data_canvas = tk.Canvas(data_window, width=375, height=667)
    data_canvas.pack(fill="both", expand=True)
    data_canvas.create_image(187, 333, image=data_bg_photo, anchor="center")
    data_window.bg_photo = data_bg_photo

    fig, ax = plt.subplots(figsize=(3.5, 2.5), dpi=100)
    time_values = []
    sensor_values = []

    def update_graph():
        while True:
            sensor_value = fetch_sensor_data()
            if sensor_value is not None:
                time_values.append(len(time_values) * 0.5)
                sensor_values.append(sensor_value)
                ax.clear()
                ax.plot(time_values, sensor_values, marker="o", linestyle="-", color="blue", label="ppm")
                ax.set_title("Sensor Data Over Time", fontsize=12, fontweight="bold")
                ax.set_xlabel("Time")
                ax.set_ylabel("Parts per Million (ppm)")
                ax.legend()
                ax.grid(True)
                canvas_graph.draw()
            time.sleep(5)

    canvas_graph = FigureCanvasTkAgg(fig, master=data_window)
    canvas_graph.draw()
    graph_widget = canvas_graph.get_tk_widget()
    graph_widget.place(x=20, y=150)

    threading.Thread(target=update_graph, daemon=True).start()

    chart_button = tk.Button(data_window, text="Open ThingSpeak Chart", font=("Glacial-Indifference", 12), command=open_thingspeak_chart_window)
    data_canvas.create_window(187, 560, window=chart_button)

    back_button = tk.Button(data_window, text="Back", command=data_window.destroy, font=("Glacial-Indifference", 14), bg="white")
    data_canvas.create_window(187, 600, window=back_button)

def open_thingspeak_chart_window():
    chart_window = Toplevel(root)
    chart_window.title("ThingSpeak Live Chart")
    chart_window.geometry("480x300")
    chart_window.resizable(False, False)

    html_view = HtmlFrame(chart_window)
    html_view.pack(fill="both", expand=True)

    url = "https://thingspeak.com/channels/2877004/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&type=line&update=15"
    html_view.load_website(url)

def fetch_sensor_data():
    url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json?api_key={read_api_key}&results=1"
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

bg_image = Image.open("Raster.png").resize((375, 667))
bg_photo = ImageTk.PhotoImage(bg_image)
canvas = tk.Canvas(root, width=375, height=667)
canvas.pack(fill="both", expand=True)
canvas.create_image(187, 333, image=bg_photo, anchor="center")

logo_image = Image.open("safewaterlogo.png").resize((100, 100))
logo_photo = ImageTk.PhotoImage(logo_image)
canvas.create_image(187, 80, image=logo_photo, anchor="center")

canvas.create_text(187, 160, text="SafeWater Monitor", font=("Glacial-Indifference", 20, "bold"), fill="black")
canvas.create_text(187, 200, text="Pure Water, Pure Peace\nSafeguarding Your Health, One Drop at a Time",
                   font=("Glacial-Indifference", 14), fill="black", anchor ="center", justify="center")

start_button = tk.Button(root, text="Start Measurement", font=("Glacial-Indifference", 16, "bold"), fg="white", width=20, height=2, relief="ridge", bd=3, command=start_measurement)
canvas.create_window(187, 300, window=start_button)

chart_button = tk.Button(root, text="View Live Chart", font=("Glacial-Indifference", 14), bg="white", command=open_thingspeak_chart_window)
canvas.create_window(187, 400, window=chart_button)

root.mainloop()
