import tkinter as tk
from tkinter import filedialog
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class DataVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Visualizer")

        # Button to load JSON file
        self.load_button = tk.Button(self.root, text="Load JSON File", command=self.load_json)
        self.load_button.pack()

        # Add a button to open the graph in a fully featured Matplotlib window
        self.open_graph_button = tk.Button(self.root, text="Open Graph in Matplotlib", command=self.open_graph_in_matplotlib)
        self.open_graph_button.pack()

        # Placeholder for the matplotlib figure
        self.figure = Figure(figsize=(10, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().pack()

        # Styling the plot
        self.ax.set_facecolor('#2e2e2e')
        self.figure.set_facecolor('#2e2e2e')
        self.ax.grid(True, color='gray')

    def load_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.plot_data(data)

    def plot_data(self, data):
        # Assuming you want to plot 'a', 'ph', and 'err' values from 'x' axis points for the first run
        run_id = next(iter(data['runs']))  # Get the first run ID
        points = data['runs'][run_id]['axes']['x']['points']
        
        x_values = list(map(int, points.keys()))
        a_values = [point['a'] for point in points.values()]
        ph_values = [point['ph'] for point in points.values()]
       # err_values = [point['err'] for point in points.values()]

        self.ax.clear()  # Clear previous plot
        self.ax.plot(x_values, a_values, marker='o', linestyle='-', color='lime', label='Amplitude (dB)')
        self.ax.plot(x_values, ph_values, marker='o', linestyle='-', color='blue', label='Phase (degrees)')
       # self.ax.plot(x_values, err_values, marker='o', linestyle='-', color='red', label='Error')

        self.ax.set_title('Frequency Response Plot', color='white')
        self.ax.set_xlabel('Frequency (Hz)', color='white')
        self.ax.set_ylabel('Values', color='white')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.legend()

        self.canvas.draw()

    def open_graph_in_matplotlib(self):
        # Check if the figure has plots
        if self.ax.lines:
            # Create a new Matplotlib window with all functionalities
            new_window_figure = plt.figure(figsize=self.figure.get_size_inches())
            new_ax = new_window_figure.add_subplot(111)
            new_ax.set_facecolor('#2e2e2e')
            new_window_figure.set_facecolor('#2e2e2e')

            # Copy the data from the existing plot to the new plot
            for line in self.ax.lines:
                new_ax.plot(line.get_xdata(), line.get_ydata(), marker=line.get_marker(), linestyle=line.get_linestyle(), color=line.get_color(), label=line.get_label())

            new_ax.set_title('Frequency Response Plot', color='white')
            new_ax.set_xlabel('Frequency (Hz)', color='white')
            new_ax.set_ylabel('Values', color='white')
            new_ax.tick_params(axis='x', colors='white')
            new_ax.tick_params(axis='y', colors='white')
            new_ax.legend()

            # Show the new window
            plt.show()
        else:
            print("No data to display. Please load a JSON file first.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataVisualizerApp(root)
    root.mainloop()



