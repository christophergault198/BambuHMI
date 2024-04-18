import tkinter as tk
from tkinter import filedialog
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MeshDataApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mesh Data Visualizer")
        self.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        self.load_button = tk.Button(self, text="Load JSON File", command=self.load_json)
        self.load_button.pack(pady=20)

    def load_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.plot_mesh_data(data)

    def plot_mesh_data(self, data):
        # Example: Plotting mesh data for the first run
        first_run_key = list(data['runs'].keys())[0]
        mesh_data = data['runs'][first_run_key]['mesh']

        x = []
        y = []
        z = []

        for x_val, inner_dict in mesh_data.items():
            for y_val, z_val in inner_dict.items():
                x.append(float(x_val))
                y.append(float(y_val))
                z.append(z_val)

        fig, ax = plt.subplots()
        sc = ax.scatter(x, y, c=z, cmap='viridis')
        plt.colorbar(sc, label='Mesh Value')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Mesh Data Visualization')

        # Embedding the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

if __name__ == "__main__":
    app = MeshDataApp()
    app.mainloop()