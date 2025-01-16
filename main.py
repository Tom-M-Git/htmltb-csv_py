import tkinter as tk
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup
import csv

def select_html_file():
    """Open file dialog to select an HTML file."""
    file_path = filedialog.askopenfilename(
        title="Select an HTML File",
        filetypes=[("HTML Files", "*.html *.htm")]
    )
    if file_path:
        html_file_path.set(file_path)

def select_csv_output():
    """Open file dialog to select a CSV output path."""
    file_path = filedialog.asksaveasfilename(
        title="Save CSV File",
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")]
    )
    if file_path:
        csv_file_path.set(file_path)

def convert_html_to_csv():
    """Convert the HTML table to a CSV file."""
    html_path = html_file_path.get()
    csv_path = csv_file_path.get()

    if not html_path or not csv_path:
        messagebox.showerror("Error", "Please select both input and output files.")
        return

    try:
        # Read the HTML file
        with open(html_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")

        # Find the table
        table = soup.find("table")
        if not table:
            messagebox.showerror("Error", "No <table> found in the HTML file.")
            return

        # Extract table rows
        rows = table.find_all("tr")
        data = []
        for row in rows:
            cells = row.find_all(["th", "td"])
            data.append([cell.get_text(strip=True) for cell in cells])

        # Write to CSV file
        with open(csv_path, "w", encoding="utf-8-sig", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(data)

        messagebox.showinfo("Success", f"CSV file saved successfully at {csv_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the GUI
root = tk.Tk()
root.title("HTML to CSV Converter")

html_file_path = tk.StringVar()
csv_file_path = tk.StringVar()

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

# Input HTML file selection
tk.Label(frame, text="Select HTML File:").grid(row=0, column=0, sticky="w", pady=5)
tk.Entry(frame, textvariable=html_file_path, width=50).grid(row=0, column=1, padx=5)
tk.Button(frame, text="Browse", command=select_html_file).grid(row=0, column=2, padx=5)

# Output CSV file selection
tk.Label(frame, text="Save CSV As:").grid(row=1, column=0, sticky="w", pady=5)
tk.Entry(frame, textvariable=csv_file_path, width=50).grid(row=1, column=1, padx=5)
tk.Button(frame, text="Browse", command=select_csv_output).grid(row=1, column=2, padx=5)

# Convert button
tk.Button(frame, text="Convert", command=convert_html_to_csv, bg="green", fg="white").grid(row=2, column=0, columnspan=3, pady=10)

root.mainloop()
