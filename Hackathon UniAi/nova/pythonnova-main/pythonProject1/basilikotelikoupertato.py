import tkinter as tk
import tkinter.ttk as ttk
import webbrowser
from PIL import Image, ImageTk, ImageDraw  # Προσθήκη του ImageDraw
# Define window size and title (only defined once)
window_width = 800

window_height = 600

window_title = "Google-Style Search Bar"

# Icon size percentage relative to window width

icon_size_percentage = 0.30  # 15% (μπορείτε να το προσαρμόσετε όπως επιθυμείτε)

# Create the main window

root = tk.Tk()

root.title(window_title)

# Calculate the center coordinates of the screen

screen_width = root.winfo_screenwidth()

screen_height = root.winfo_screenheight()

x_coordinate = (screen_width - window_width) // 2

y_coordinate = (screen_height - window_height) // 2

# Set the window position to the center of the screen

root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Set the background color of the main window to white

root.configure(bg="white")

# Create a frame for the background

background_frame = tk.Frame(root, bg="white")

background_frame.pack(fill=tk.BOTH, expand=True)

# Load the icon image

try:

    image = Image.open("unnamed.jpg")

    icon_width = int(window_width * icon_size_percentage)

    icon_height = int((icon_width / image.width) * image.height)

    image = image.resize((icon_width, icon_height))  # Resize the image proportionally

    # Create a rounded mask for the icon

    mask = Image.new("L", (icon_width, icon_height), 0)

    draw = ImageDraw.Draw(mask)

    draw.ellipse((0, 0, icon_width, icon_height), fill=255)

    image.putalpha(mask)

    icon_image = ImageTk.PhotoImage(image)

    # Create a label to display the icon image in the center of the window

    icon_label = tk.Label(background_frame, image=icon_image, bg="white")

    icon_label.place(relx=0.5, rely=0.30, anchor=tk.CENTER)  # Place in the center of the window

    # Make sure the image is not garbage collected

    icon_label.image = icon_image

except FileNotFoundError:

    print("Error: Image 'NOVA11.jpg' not found.")

# Create the search bar frame

search_bar_frame = ttk.Frame(background_frame, width=600, height=50, padding=10, relief="solid", borderwidth=1,
                             style="Search.TFrame")

search_bar_frame.place(relx=0.5, rely=0.45, anchor=tk.CENTER)  # Place near the bottom center of the window

# Create the search bar entry

search_entry = ttk.Entry(search_bar_frame, width=40, font=("Arial", 16), style="Search.TEntry")

search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

# Create the search button

search_button = ttk.Button(search_bar_frame, text="Search", command=lambda: search_web(), style="Search.TButton")

search_button.pack(side=tk.RIGHT, padx=10)


# Function to handle the search action

def search_web():
    search_term = search_entry.get()

    if search_term:
        webbrowser.open(f"https://www.google.com/search?q={search_term}")


# Set the style for the circular search bar frame

style = ttk.Style()

style.configure("Search.TFrame", background="#333399", borderwidth=0, bordercolor="#333399")

# Set the style for the circular search entry

style.configure("Search.TEntry", borderwidth=0, bordercolor="#333399")

# Set the style for the circular search button

style.configure("Search.TButton", borderwidth=0, bordercolor="#333399")

# Start the main event loop

root.mainloop()