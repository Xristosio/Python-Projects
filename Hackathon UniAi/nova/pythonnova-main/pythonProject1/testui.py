import tkinter as tk
import tkinter.ttk as ttk
import mysql.connector
from PIL import Image, ImageTk

# Define window size and title
window_width = 800
window_height = 600
window_title = "Database Text Search App"

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

# Load the image to display above the search bar
try:
    top_image = Image.open("unnamed.jpg")  # Replace with your image name
    top_image = top_image.resize((int(window_width * 0.8), 150))  # Adjust size as needed
    top_image_tk = ImageTk.PhotoImage(top_image)

    top_image_label = tk.Label(background_frame, image=top_image_tk, bg="white")
    top_image_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    # Keep a reference to avoid garbage collection
    top_image_label.image = top_image_tk
except FileNotFoundError:
    print("Error: Image 'unnamed.jpg.jpg' not found.")

# Create the search bar frame
search_bar_frame = ttk.Frame(
    background_frame,
    width=600,
    height=50,
    padding=10,
    relief="solid",
    borderwidth=1,
    style="Search.TFrame",
)
search_bar_frame.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

# Create the search entry
search_entry = ttk.Entry(search_bar_frame, width=40, font=("Arial", 16), style="Search.TEntry")
search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

# Create the search button
search_button = ttk.Button(search_bar_frame, text="Search", command=lambda: search_db())
search_button.pack(side=tk.RIGHT, padx=10)

# Create a text widget for displaying results
results_text = tk.Text(background_frame, height=10, font=("Arial", 12), padx=10, pady=10)
results_text.place(relx=0.5, rely=0.70, anchor=tk.CENTER)  # Below the search bar, centered

# Function for searching in the database by text in div_text
def search_db():
    search_term = search_entry.get()  # Get the search term

    # Clear previous results
    results_text.delete(1.0, tk.END)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host="database-nova.c7a6a2808nfy.us-west-2.rds.amazonaws.com",
        port=3306,
        user="admin",
        password="digitalsnova",
        database="nova"
    )
    cursor = conn.cursor()

    # Query to search in div_text with a pattern
    query = "SELECT * FROM nova_1 WHERE div_text LIKE %s"  # Replace 'your_table' with your table name
    search_pattern = "%" + search_term + "%"  # Create a pattern for LIKE query
    cursor.execute(query, (search_pattern,))

    results = cursor.fetchall()  # Fetch results

    if not results:
        results_text.insert(tk.END, "No results found.")
    else:
        # Display results in the text widget
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
