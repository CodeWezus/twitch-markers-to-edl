import convert_csv_to_edl
from tkinter import Tk, filedialog, messagebox
from pathlib import Path

def main():

    # Create hidden root window for message box dialog
    root = Tk()
    root.withdraw()

    # Prompt user to select Twitch markers CSV file
    csv_path = filedialog.askopenfilename(
        title="Select Twitch Markers CSV File",
        filetypes=[("CSV files", "*.csv")]
    )

    if not csv_path:
        messagebox.showerror("Error", "No CSV file selected.")
        return
    
    # Prompt if user wants to apply DaVinci Resolve offset
    offset_choice = messagebox.askyesno(
        title="Apply Offset",
        message="Do you want to apply a 1-hour offset to the timestamps for DaVinci Resolve? (Timeline starts at 1:00:00:00)"
    )

    offset_hours = 1 if offset_choice else 0

    # Prompt user to select output EDL file path
    edl_file_path = filedialog.asksaveasfilename(
        title="Save EDL File",
        defaultextension=".edl",
        initialfile=Path(csv_path).stem + ".edl",
        filetypes=[("EDL files", "*.edl")],
    )

    if not edl_file_path:
        messagebox.showerror("Error", "No output EDL file selected.")
        return
    
    # Convert the CSV to EDL
    if edl_file_path:
        convert_csv_to_edl.convert_csv_to_edl(csv_path, edl_file_path, offset_hours)
    
if __name__ == "__main__":
    main()