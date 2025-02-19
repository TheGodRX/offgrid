import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import fitz  # PyMuPDF for PDFs
import pygame  # For video playback

# Folder where all resources are saved
BASE_DIR = "offline_survival_resources"

# Define categories and their corresponding directories
categories = {
    "Medical": os.path.join(BASE_DIR, "Medical"),
    "Weapons": os.path.join(BASE_DIR, "Weapons"),
    "Hunting": os.path.join(BASE_DIR, "Hunting"),
    "Farming": os.path.join(BASE_DIR, "Farming"),
    "Archive_Videos": os.path.join(BASE_DIR, "Archive_Videos"),
    "HOME": os.path.join(BASE_DIR, "HOME")
}

# Initialize pygame for video playback
pygame.init()

# Function to open a file
def open_file(file_path):
    try:
        if file_path.endswith(".pdf"):
            display_pdf(file_path)
        elif file_path.endswith((".mp4", ".avi", ".mov")):
            play_video(file_path)
        else:
            if os.name == 'nt':  # Windows
                os.startfile(file_path)
            elif os.name == 'posix':  # Linux
                subprocess.run(['xdg-open', file_path])
            else:
                raise OSError("Unsupported OS")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open file: {e}")

# Function to display a PDF in the interface (all pages)
def display_pdf(file_path):
    doc = fitz.open(file_path)
    pdf_width, pdf_height = 640, 480  # Dimensions for the page display area
    total_pages = len(doc)
    
    # Clear the canvas
    pdf_canvas.delete("all")
    
    # Display all pages
    for page_num in range(total_pages):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img_tk = ImageTk.PhotoImage(img)
        
        # Draw each page on the canvas at the appropriate position
        pdf_canvas.create_image(0, page_num * pdf_height, anchor=tk.NW, image=img_tk)
        pdf_canvas.image = img_tk  # Keep a reference to prevent garbage collection

    # Adjust the canvas size based on the number of pages
    pdf_canvas.config(scrollregion=pdf_canvas.bbox("all"))

# Function to play a video in the interface
def play_video(file_path):
    # Set up the pygame window for video display
    screen = pygame.display.set_mode((640, 480))  # Adjust as needed
    movie = pygame.movie.Movie(file_path)
    movie.set_display(screen)
    movie.play()

# Function to list files in a category
def list_files(category):
    file_listbox.delete(0, tk.END)
    category_dir = categories[category]
    if os.path.exists(category_dir):
        for root, _, files in os.walk(category_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_listbox.insert(tk.END, file_path)

# Function to handle file selection
def on_file_select(event):
    selected_file = file_listbox.get(file_listbox.curselection())
    open_file(selected_file)

# Function to handle category selection
def on_category_select(event):
    selected_category = category_combobox.get()
    list_files(selected_category)

# Create the main window
root = tk.Tk()
root.title("Survival Resources Interface")
root.geometry("800x600")

# Create a frame for the category selection
category_frame = ttk.Frame(root, padding="10")
category_frame.pack(fill=tk.X)

# Create a label for the category selection
category_label = ttk.Label(category_frame, text="Select Category:", font=("Arial", 14))
category_label.pack(side=tk.LEFT, padx=5, pady=5)

# Create a combobox for category selection
category_combobox = ttk.Combobox(category_frame, values=list(categories.keys()), font=("Arial", 14))
category_combobox.pack(side=tk.LEFT, padx=5, pady=5)
category_combobox.bind("<<ComboboxSelected>>", on_category_select)

# Create a frame for the file list
file_frame = ttk.Frame(root, padding="10")
file_frame.pack(fill=tk.BOTH, expand=True)

# Create a listbox for file display
file_listbox = tk.Listbox(file_frame, font=("Arial", 12), selectmode=tk.SINGLE)
file_listbox.pack(fill=tk.BOTH, expand=True)
file_listbox.bind("<<ListboxSelect>>", on_file_select)

# Create a frame for the footer
footer_frame = ttk.Frame(root, padding="10")
footer_frame.pack(fill=tk.X)

# Create a label for the footer
footer_label = ttk.Label(footer_frame, text="Survival Resources Interface v1.0", font=("Arial", 10))
footer_label.pack(side=tk.RIGHT, padx=5, pady=5)

# Create a canvas for displaying PDF pages
pdf_canvas = tk.Canvas(root, width=640, height=480, bg="black")
pdf_canvas.pack()

# Apply a custom style
style = ttk.Style()
style.theme_use('clam')
style.configure("TFrame", background="#282c34", foreground="white")
style.configure("TLabel", background="#282c34", foreground="white")
style.configure("TCombobox", background="#282c34", foreground="white")
style.configure("TButton", background="#282c34", foreground="white")

# Set the initial category
category_combobox.set("Medical")
list_files("Medical")

# Run the main loop
root.mainloop()
