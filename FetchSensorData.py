from tkinter import ttk
from tkinterweb import HtmlFrame  # Make sure tkinterweb is installed

def open_sensor_data_screen():
    """Open a new window to display real-time sensor data graph and ThingSpeak chart."""
    data_window = Toplevel(root)
    data_window.title("Sensor Data")
    data_window.geometry("375x667")
    data_window.resizable(False, False)

    # Background
    data_bg_image = Image.open("backgroundblue.jpg").resize((375, 667))
    data_bg_photo = ImageTk.PhotoImage(data_bg_image)
    data_canvas = tk.Canvas(data_window, width=375, height=667)
    data_canvas.pack(fill="both", expand=True)
    data_canvas.create_image(187, 333, image=data_bg_photo, anchor="center")
    data_window.bg_photo = data_bg_photo

    # Create Notebook (tab view)
    notebook = ttk.Notebook(data_window)
    notebook.place(x=10, y=100, width=355, height=460)

    # ---------- Tab 1: Matplotlib Graph ----------
    graph_frame = tk.Frame(notebook)
    notebook.add(graph_frame, text="Live Plot")

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
                ax.plot(time_values, sensor_values, marker="o", linestyle="-", color="blue", label="pH Levels")
                ax.set_title("Sensor Data Over Time", fontsize=12, fontweight="bold")
                ax.set_xlabel("Time")
                ax.set_ylabel("Parts per Million (ppm)")
                ax.legend()
                ax.grid(True)
                canvas_graph.draw()
            time.sleep(5)

    canvas_graph = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas_graph.draw()
    canvas_graph.get_tk_widget().pack(fill="both", expand=True)

    threading.Thread(target=update_graph, daemon=True).start()

    # ---------- Tab 2: ThingSpeak Live Chart ----------
    chart_frame = tk.Frame(notebook)
    notebook.add(chart_frame, text="ThingSpeak Chart")

    url = "https://thingspeak.com/channels/2877004/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&type=line&update=15"
    html_view = HtmlFrame(chart_frame)
    html_view.load_website(url)
    html_view.pack(fill="both", expand=True)

    # Back button
    back_button = tk.Button(data_window, text="Back", command=data_window.destroy, font=("Glacial-Indifference", 14), bg="white")
    data_canvas.create_window(187, 600, window=back_button)
