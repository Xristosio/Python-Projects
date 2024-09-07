import tkinter as tk
import tkinter.ttk as ttk
import webbrowser
import mysql.connector
from PIL import Image, ImageTk, ImageDraw

# Define window size and title
window_width = 800
window_height = 600
window_title = "The Digitals"

# Create the main window
root = tk.Tk()
root.title(window_title)

# Set the window to the center of the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
root.configure(bg="white")

# Create a frame for the background
background_frame = tk.Frame(root, bg="white")
background_frame.pack(fill=tk.BOTH, expand=True)

# Load the icon image
try:
    image = Image.open("unnamed.jpg")
    icon_size_percentage = 0.30
    icon_width = int(window_width * icon_size_percentage)
    icon_height = int((icon_width / image.width) * image.height)
    image = image.resize((icon_width, icon_height))

    # Create the icon label
    icon_image = ImageTk.PhotoImage(image)
    icon_label = tk.Label(background_frame, image=icon_image, bg="white")
    icon_label.place(relx=0.5, rely=0.30, anchor=tk.CENTER)
    icon_label.image = icon_image
except FileNotFoundError:
    print("Error: Image 'unnamed.jpg' not found.")

# Create the search bar frame
search_bar_frame = ttk.Frame(
    background_frame,
    width=600,
    height=50,
    padding=10,
    relief="solid",
    borderwidth=1,
    style="Search.TFrame"
)
search_bar_frame.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

# Create the search entry
search_entry = ttk.Entry(search_bar_frame, width=40, font=("Arial", 16), style="Search.TEntry")
search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

# Create the search button to search the web
web_search_button = ttk.Button(search_bar_frame, text="Search Web", command=lambda: search_web(),
                               style="Search.TButton")
web_search_button.pack(side=tk.RIGHT, padx=10)

# Create the search button to search the database
db_search_button = ttk.Button(search_bar_frame, text="Search", command=lambda: search_db(), style="Search.TButton")
db_search_button.pack(side=tk.RIGHT, padx=10)


# Function to search the web
def search_web():
    search_term = search_entry.get()
    if search_term:
        webbrowser.open(f"https://www.google.com/search?q={search_term}")


# Create a text widget for displaying results from the database
results_text = tk.Text(background_frame, height=10, font=("Arial", 12), padx=10, pady=10)
results_text.place(relx=0.5, rely=0.70, anchor=tk.CENTER)


# Function to search the database
def search_db():
    search_term = search_entry.get()

    results_text.delete(1.0, tk.END)  # Clear previous results

    conn = mysql.connector.connect(
        host="database-nova.c7a6a2808nfy.us-west-2.rds.amazonaws.com",
        port=3306,
        user="admin",
        password="digitalsnova",
        database="nova"
    )

    cursor = conn.cursor()

    # Query to search in div_text with a pattern
    query = "SELECT * FROM nova_1 WHERE div_text LIKE %s"
    search_pattern = "%" + search_term + "%"

    cursor.execute(query, (search_pattern,))

    results = cursor.fetchall()

    if not results:
        results_text.insert(tk.END, "No results found.")
    else:
        results_content = "\n".join([str(row) for row in results])
        results_text.insert(tk.END, results_content)

    cursor.close()
    conn.close()


# Configure ttk styles
style = ttk.Style()
style.configure("Search.TFrame", background="#333399", borderwidth=0, bordercolor="#333399")
style.configure("Search.TEntry", borderwidth=0, bordercolor="#333399")
style.configure("Search.TButton", borderwidth=0, bordercolor="#333399")

# Start the main event loop
root.mainloop()
