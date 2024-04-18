import tkinter as tk
from tkinter import scrolledtext

def convert_gcode():
    # Get text from input_text widget
    input_gcode = input_text.get("1.0", tk.END)
    # Split the input into lines
    lines = input_gcode.split('\n')
    # Process each line to remove inline comments and then filter out empty lines
    processed_lines = [line.split(';')[0].strip() for line in lines]
    non_empty_lines = [line for line in processed_lines if line]
    # Join the processed lines back into a single string without comments
    cleaned_gcode = '\\n'.join(non_empty_lines)  # Use double backslashes for literal \n in the output
    # Set converted G-code to output_text widget
    output_text.delete("1.0", tk.END)  # Clear existing text
    output_text.insert("1.0", cleaned_gcode)  # No need to strip trailing '\\n' due to join method used

    # Adjust cleaned_gcode for file writing to display \\n
    file_gcode = cleaned_gcode.replace('\\n', '\\\\n')

    # Save the cleaned G-code to a text file
    with open("converted_gcode.txt", "w") as file:
        file.write(file_gcode)

    print(file_gcode)

# Create the main window
root = tk.Tk()
root.title("G-code Converter")

# Create a frame for the top part of the GUI
top_frame = tk.Frame(root)
top_frame.pack(padx=10, pady=5, fill=tk.X)

# Input text area
input_label = tk.Label(top_frame, text="Input G-code:")
input_label.pack(anchor='w')
input_text = scrolledtext.ScrolledText(top_frame, height=10)
input_text.pack(fill=tk.X, padx=5, pady=5)

# Convert button
convert_button = tk.Button(top_frame, text="Convert", command=convert_gcode)
convert_button.pack(pady=5)

# Output text area
output_label = tk.Label(top_frame, text="Converted G-code:")
output_label.pack(anchor='w')
output_text = scrolledtext.ScrolledText(top_frame, height=10)
output_text.pack(fill=tk.X, padx=5, pady=5)

# Start the GUI event loop
root.mainloop()
