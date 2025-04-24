import tkinter as tk
from tkinter import Toplevel, messagebox
from PIL import Image, ImageTk
import requests
import time
import itertools
import webbrowser
from tkinterweb import HtmlFrame

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
    loading_screen = show_loading_screen()
    time.sleep(3)

    if not check_sensor_connection():
        loading_screen.destroy()
        messagebox.showerror("Sensor Error", "Sensor is not connected or not sending data!")
        return

    loading_screen.destroy()
    open_sensor_data_screen()

def open_placeholder_chart_window():
    chart_window = Toplevel(root)
    chart_window.title("Live Chart (Preview)")
    chart_window.geometry("400x350")
    chart_window.resizable(False, False)

    # Load and resize the image
    chart_image = Image.open("chart_placeholder.jpg").resize((380, 300))  # Adjust to fit your window
    chart_photo = ImageTk.PhotoImage(chart_image)

    # Display the image in a label
    image_label = tk.Label(chart_window, image=chart_photo)
    image_label.image = chart_photo  # Keep a reference!
    image_label.pack(pady=10)


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

    # Simulated chart preview image
    preview_img = Image.open("chart_placeholder.jpg").resize((340, 220))  # Use a screenshot of the chart
    preview_photo = ImageTk.PhotoImage(preview_img)
    chart_preview = tk.Label(data_window, image=preview_photo)
    chart_preview.image = preview_photo  # Prevent garbage collection
    chart_preview.place(x=18, y=150)

    # Button to open real chart in browser
    chart_button = tk.Button(data_window, text="Open Live Chart in Browser", font=("Glacial-Indifference", 12),
                             command=open_thingspeak_chart_window)
    data_canvas.create_window(187, 560, window=chart_button)

    back_button = tk.Button(data_window, text="Back", command=data_window.destroy,
                            font=("Glacial-Indifference", 14), bg="white")
    data_canvas.create_window(187, 600, window=back_button)

def open_thingspeak_chart_window():
    webbrowser.open("https://thingspeak.com/channels/2877004/charts/1?bgcolor=%23ffffff&color=%230077cc&dynamic=true&results=60&type=line&update=15")


# Main GUI
root = tk.Tk()
root.title("Water Testing App")
root.geometry("375x667")
root.resizable(False, False)

bg_image = Image.open("StevensRed.jpg").resize((375, 667))
bg_photo = ImageTk.PhotoImage(bg_image)
canvas = tk.Canvas(root, width=375, height=667)
canvas.pack(fill="both", expand=True)
canvas.create_image(187, 333, image=bg_photo, anchor="center")

logo_image = Image.open("safewaterlogo.png").resize((100, 100))
logo_photo = ImageTk.PhotoImage(logo_image)
canvas.create_image(187, 80, image=logo_photo, anchor="center")

canvas.create_text(187, 160, text="SafeWater Monitor", font=("Glacial-Indifference", 20, "bold"), fill="black")
canvas.create_text(187, 200, text="Pure Water, Pure Peace\nSafeguarding Your Health, One Drop at a Time",
                   font=("Glacial-Indifference", 12), fill="black", anchor="center", justify="center")

start_button = tk.Button(root, text="Start Measurement", font=("Glacial-Indifference", 16, "bold"),
                         fg="black", width=20, height=2, relief="ridge", bd=3, command=start_measurement)
canvas.create_window(187, 300, window=start_button)

chart_button = tk.Button(root, text="View Live Chart", font=("Glacial-Indifference", 14),
                         bg="white", command=open_thingspeak_chart_window)
canvas.create_window(187, 400, window=chart_button)

root.mainloop()
