import csv
from datetime import timedelta # For working with time durations
from tkinter import messagebox # For GUI file dialog
from pathlib import Path # For handling file paths

# Convert Twitch marker timestamps (HH:MM:SS) into DaVinic Resolve EDL timecodes (HH:MM:SS:FF) 
def convert_timestamp_to_timecode(timestamp: str, offset_hours: int) -> str:
    
    hours, minutes, seconds = map(int, timestamp.strip().split(':'))

    # Calculate total seconds from the timestamp with offset
    total_seconds = hours * 3600 + minutes * 60 + seconds + (offset_hours * 3600)

    # Convert total seconds to HH:MM:SS format
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Return timecode formatted as HH:MM:SS starting at frame 00
    return f"{hours:02}:{minutes:02}:{seconds:02}:00" 

# Function that reads a CSV file and converts it to an EDL for
def convert_csv_to_edl(csv_path, edl_path, offset_hours):
    try:
        # Open the CSV file and read its contents
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            
            # Put all csv rows into a list
            rows = list(reader)

            if 'Timestamp' in rows[0][0]:
                 rows = rows[1:]  # Skip header row if present

            title = Path(csv_path).stem  # Use the CSV filename as the EDL title

            # Initialize the EDL content with the title and frame count mode for DaVinci Resolve
            edl_lines = [
                "EDL",
                "Title: Timeline 1",
                "FCM: NON-DROP-FRAME\n"
            ]

            # Loop through each marker in the CSV and create EDL entry
            for i, row in enumerate(rows):
                time, user_type, username, marker_title = row

                csv_time = convert_timestamp_to_timecode(time, offset_hours)
                edl_time = csv_time[:-2] + "01"  # Setting marker duration to 1 frame

                # Formatting the EDL line according to DaVinci Resolve specifications
                edl_lines.append(f"{i:03}  001      V    C        {csv_time} {edl_time} {csv_time} {edl_time}  ")
                edl_lines.append(f" |C:ResolveColorBlue |M:{marker_title} by {username} [{user_type}] |D:1\n")

            # Write the EDL content to the output file
            with open(edl_path, 'w', encoding='utf-8') as edlfile:
                edlfile.write('\n'.join(edl_lines))

        
        messagebox.showinfo("Success", f"EDL file created successfully at {edl_path}")  
    
    except FileNotFoundError:
        messagebox.showerror("Error", f"CSV file not found: {csv_path}")
        return
    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert CSV to EDL: {e}")
        return