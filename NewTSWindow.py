from tkinterweb import HtmlFrame  # Make sure tkinterweb is installed

def open_thingspeak_chart_window():
    """Open a new window to display the ThingSpeak live chart."""
    chart_window = Toplevel(root)
    chart_window.title("ThingSpeak Live Chart")
    chart_window.geometry("480x300")  # Adjust as needed
    chart_window.resizable(False, False)

    # Create and pack the web frame
    html_view = HtmlFrame(chart_window)
    html_view.pack(fill="both", expand=True)

    # Load the ThingSpeak chart
    url = "https://thingspeak.com/channels/2877004/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&type=line&update=15"
    html_view.load_website(url)
