import tkinter as tk
from tkinter import Toplevel, messagebox
from PIL import Image, ImageTk
import requests
import webbrowser

# ThingSpeak details
channel_id = "2877004"
read_api_key = "00YSVLHONG1542DI"
write_api_key = "3VI96UKBSDR2T4BC"

def send_start_command():
    url = "https://api.thingspeak.com/update"
    params = {
        "api_key": write_api_key,
        "field2": "START"
    }
    response = requests.get(url, params=params)
    print("Sent START command:", response.status_code, response.text)
    return response.status_code == 200

def start_measurement_sequence():
    success = send_start_command()
    if not success:
        messagebox.showerror("Error", "Failed to communicate with Arduino!")
        return
    open_thingspeak_chart()

def open_thingspeak_chart():
    chart_url = "https://thingspeak.com/channels/2877004/charts/1?bgcolor=%23ffffff&color=%230077cc&dynamic=true&results=60&type=line&update=15"
    webbrowser.open(chart_url)

# Tkinter main window setup
root = tk.Tk()
root.title("Water Testing App")
root.geometry("375x667")
root.resizable(False, False)
root.configure(bg="#9D1535")

logo_image = Image.open("safewaterlogo.png").resize((100, 100))
logo_photo = ImageTk.PhotoImage(logo_image)

canvas = tk.Canvas(root, width=375, height=667, bg="#9D1535", highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_image(187, 100, image=logo_photo, anchor="center")

title_label = tk.Label(root, text="SafeWater Monitor", font=("Montserrat", 26, "bold"),
                       fg="#949594", bg="#9D1535")
title_label.place(x=187, y=170, anchor="center")

subtitle_label = tk.Label(root, text="Pure Water, Pure Peace\nSafeguarding Your Health, One Drop at a Time",
                          font=("Montserrat", 16), fg="#949594", bg="#9D1535", anchor="center", justify="center")
subtitle_label.place(x=187, y=340, anchor="center")

start_button = tk.Button(root, text="View Live Chart", font=("Montserrat", 16, "bold"),
                         fg="#1E90FF", bg="#9D1535", width=20, height=2, relief="ridge", bd=3,
                         command=start_measurement_sequence)
canvas.create_window(187, 570, window=start_button)

canvas.image = logo_photo
root.mainloop()