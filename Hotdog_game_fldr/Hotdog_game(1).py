# 🌭✨ HOT DOG MATH SHOWDOWN: GLIZZY GLADIATORS EDITION ✨🌭
#
# 📢 ATTENTION HUMAN (OR FUTURE SLEEP-DEPRIVED ME):
# This code simulates three math-powered hot dog eaters battling for SUPREMACY:
# - 🟥 KobaYOLOshi (n²): "Slow start, but I YEET hot dogs later"  
# - 🟦 Doubler (2ⁿ): "I break the game by round 8, FIGHT ME"  
# - 🟩 Sonya "Extra Dip" (n² + n): "I brought my own mustard"  
#
# 🔥 DEPENDENCIES:
# - Run `pip install matplotlib numpy` or cry in "ModuleNotFoundError"  
# - Pray to the Python gods if you’re on Windows 🙏🐍 (story of my life) 
#
# 🎛️ CONTROLS:
# - [Next Round]: "JUST ONE MORE BITE—OH GOD IT’S 2ⁿ"  
# - [Replay]: "Relive the trauma (now with 100% more MATH)"  
# - [Graph]: "Proof that numbers can be scary"  
#
# 💀 KNOWN BUGS:
# - The Doubler becomes a literal black hole by round 10 (feature, not bug)  
# - Sonya’s color looks like moldy guacamole (WIP)  
# - Me, after debugging this: 🤡  
#
# 🚨 WARNING:
# This code contains:  
# - 10% actual math  
# - 30% tkinter spaghetti  
# - 60% "why did I think this was a good idea?"  
#
# P.S. If you’re reading this, bring snacks. You’ll need them. 🍕 ;-;


import tkinter as tk
from tkinter import ttk
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

class MathCompetitionGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hot Dog Math Showdown")

        # Grid scaling
        self.cell_size = 70  # Enlarged scale

        # Canvas setup
        self.canvas = tk.Canvas(root, width=self.cell_size * 21, height=self.cell_size * 21, bg='white')
        self.canvas.pack(side=tk.LEFT)

        # Control panel
        self.controls = ttk.Frame(root)
        self.controls.pack(side=tk.RIGHT, padx=10)

        # Competitors - Kobayashi, Doubler, Sonya with their respective formulas
        self.kobayashi = {"position": [1, 1], "color": "red", "formula": lambda n: n**2}
        self.doubler = {"position": [1, 1], "color": "blue", "formula": lambda n: 2**n}
        self.sonya = {"position": [1, 1], "color": "green", "formula": lambda n: n**2 + n}

        # Round tracker- starts at 1
        self.round = 1
        self.max_rounds = 20
        self.history = []

        # Initialize UI- draw grid, draw competitors, draw graph
        self.setup_controls()
        self.draw_grid()
        self.setup_graph()
     # End of __init__ - setup UI and draw initial grid and graph- competitors are not drawn yet- they are added in the next round - round 1 is skipped
    def setup_controls(self):
        ttk.Button(self.controls, text="Next Round", command=self.next_round).pack(pady=5)
        ttk.Button(self.controls, text="Reset", command=self.reset).pack(pady=5)
        
        # Round tracker- label and entry- entry is disabled - only the label is updated when the round changes
        ttk.Label(self.controls, text="Animation Speed:").pack()
        self.speed = tk.DoubleVar(value=1.0)
        ttk.Scale(self.controls, from_=0.1, to=2.0, variable=self.speed, orient="horizontal").pack()

        # Competitor labels - initially empty - will be populated as competitors are added or removed
        self.kobayashi_label = ttk.Label(self.controls, text="Kobayashi Total: 0")
        self.kobayashi_label.pack()
        self.doubler_label = ttk.Label(self.controls, text="Doubler Total: 0")
        self.doubler_label.pack()
        self.sonya_label = ttk.Label(self.controls, text="Sonya Total: 0")
        self.sonya_label.pack()
        ttk.Label(self.controls, text="Jump to Round:").pack(pady=(10, 0))
        self.round_entry = ttk.Entry(self.controls)
        self.round_entry.pack()
        ttk.Button(self.controls, text="Go", command=self.jump_to_round).pack()

        ttk.Button(self.controls, text="Replay", command=self.replay).pack(pady=10)
    # End of setup_controls - setup control panel with buttons, round tracker, and competitor labels


    def draw_grid(self):
        self.canvas.delete("all")
        for i in range(1, 21):
            self.canvas.create_line(self.cell_size * i, self.cell_size, self.cell_size * i, self.cell_size * 21, fill="gray", dash=(1, 1))
            self.canvas.create_line(self.cell_size, self.cell_size * i, self.cell_size * 21, self.cell_size * i, fill="gray", dash=(1, 1))
            self.canvas.create_text(self.cell_size * i + 25, 30, text=f"R{i}" if i <= 10 else i)
            self.canvas.create_text(30, self.cell_size * i + 25, text=str(2**i if i <= 10 else i * 10))

# End of draw_grid - draw grid with rows and columns labeled
    def setup_graph(self):
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.graph_canvas = FigureCanvasTkAgg(self.fig, master=self.controls)
        self.graph_canvas.get_tk_widget().pack()
    # End of setup_graph - setup graph canvas with a figure and axis

    def next_round(self):
        if self.round > self.max_rounds:
            return
        # Update round tracker
        self.kobayashi["position"] = [self.round, self.kobayashi["formula"](self.round)]
        self.doubler["position"] = [self.round, self.doubler["formula"](self.round)]
        self.sonya["position"] = [self.round, self.sonya["formula"](self.round)] # Sonya's position is updated here and others are updated in the draw_graph method
        # Update the graph with the new data
        self.kobayashi["cumulative"] = sum(self.kobayashi["formula"](r) for r in range(1, self.round + 1))
        self.doubler["cumulative"] = sum(self.doubler["formula"](r) for r in range(1, self.round + 1))
        self.sonya["cumulative"] = sum(self.sonya["formula"](r) for r in range(1, self.round + 1)) # Sonya's cumulative is updated here and others are updated in the draw_graph method
    # End of next_round - update positions and cumulative totals for each competitor
        self.history.append({
            "round": self.round,
            "positions": {
                "kobayashi": self.kobayashi["position"],
                "doubler": self.doubler["position"],
                "sonya": self.sonya["position"]
            }
        })
    # End of history.append - add current round to history dictionary
        self.draw_competitors()
        self.update_graph() 
            # self.draw_grid()
        self.kobayashi_label.config(text=f"Kobayashi Total: {self.kobayashi['cumulative']}") # Update Kobayashi's total
        self.doubler_label.config(text=f"Doubler Total: {self.doubler['cumulative']}") # Update Doubler's total
        self.sonya_label.config(text=f"Sonya Total: {self.sonya['cumulative']}") # Update Sonya's total

        self.round += 1
    # End of next_round - increment round number and update labels
    def draw_competitors(self):
        for competitor in [self.kobayashi, self.doubler, self.sonya]:
            x, y = competitor["position"]
            scaled_x = self.cell_size + (x - 1) * self.cell_size
            scaled_y = self.cell_size * 21 - (y - 1) * 2
            # Draw a rectangle for the competitor's position
            self.canvas.create_oval(scaled_x - 15, scaled_y - 15, scaled_x + 15, scaled_y + 15, fill=competitor["color"]) # Draw a circle for the competitor's position
            self.canvas.create_text(scaled_x, scaled_y - 20, text=f"{competitor['formula'](self.round)}") # Draw the competitor's value at their position
    # End of draw_competitors - draw each competitor at their current position

    def update_graph(self):
        rounds = range(1, self.round + 1)
        self.ax.clear()
        self.ax.plot(rounds, [self.kobayashi["formula"](r) for r in rounds], 'r-', label="Kobayashi (n²)")
        self.ax.plot(rounds, [self.doubler["formula"](r) for r in rounds], 'b-', label="Doubler (2ⁿ)")
        self.ax.plot(rounds, [self.sonya["formula"](r) for r in rounds], 'g-', label="Sonya (n²+n)")
        self.ax.legend()
        self.ax.set_xlabel("Round")
        self.ax.set_ylabel("Hot Dogs")
        self.graph_canvas.draw()
 # End of update_graph - update the graph with the current round's data
 
    def jump_to_round(self):
        try:# Try to convert the input to an integer
            target = int(self.round_entry.get())
            if 1 <= target <= self.max_rounds:# Check if the target round is within the valid range
                self.reset()
                for _ in range(target):# Simulate the rounds up to the target round
                    self.next_round()
        except ValueError:# dummy proofing for non-integer input
            pass

    def replay(self):# Replay the game from the start
        self.reset()
        for frame in self.history:
            self.kobayashi["position"] = frame["positions"]["kobayashi"]
            self.doubler["position"] = frame["positions"]["doubler"]
            self.sonya["position"] = frame["positions"]["sonya"] # Update the positions of the competitors
            self.round = frame["round"]
            self.draw_competitors()
            self.update_graph()
            self.root.update()
            time.sleep(1 / self.speed.get()) # Pause for a short time to simulate the game's speed

# End of HotDogsGame - the main class for the game- simulation- and graph display and replay functionality 
    def reset(self):
        self.round = 1 # 
        self.history = [] # Clear the history of the game
        self.canvas.delete("all") # Clear the canvas
        self.draw_grid() # Draw the grid
        self.ax.clear() # Clear the graph
        self.graph_canvas.draw()# Redraw the graph canvas
        # End of reset - reset the game to its initial state


if __name__ == "__main__": # If the script is run directly (not imported)
    root = tk.Tk() # Create the main window
    game = MathCompetitionGame(root)# Create an instance of the game
    root.mainloop()







#---------------------------------------------------------Old Code (I ended up ditching)-----------------------------------------#



    """""
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

#setting upp cell size
cell_size = 100


class MathCompetitionGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hot Dog Math Showdown")
        
        # Grid setup
        self.canvas = tk.Canvas(root, width=1700, height=1700, bg='white')
        self.canvas.pack(side=tk.LEFT)
        
        # Control panel
        self.controls = ttk.Frame(root)
        self.controls.pack(side=tk.RIGHT, padx=10)
        
        # Competitors
        self.kobayashi = {"position": [1, 1], "color": "red", "formula": lambda n: n**2}
        self.doubler = {"position": [1, 1], "color": "blue", "formula": lambda n: 2**n}
        self.sonya = {"position": [1, 1], "color": "green", "formula": lambda n: n**2 + n}
        
        # Round tracker
        self.round = 1
        self.max_rounds = 20
        self.history = []
        
        # Initialize UI
        self.setup_controls()
        self.draw_grid()
        self.setup_graph()

    def setup_controls(self):
        ttk.Button(self.controls, text="Next Round", command=self.next_round).pack(pady=5)
        ttk.Button(self.controls, text="Reset", command=self.reset).pack(pady=5)
        
        # Speed control with label
        ttk.Label(self.controls, text="Animation Speed:").pack()
        self.speed = tk.DoubleVar(value=1.0)
        self.scale = ttk.Scale(self.controls, from_=0.1, to=2.0, variable=self.speed, 
                             orient="horizontal")
        self.scale.pack()
        self.kobayashi_label = ttk.Label(self.controls, text="Kobayashi Total: 0")
        self.kobayashi_label.pack()

        self.doubler_label = ttk.Label(self.controls, text="Doubler Total: 0")
        self.doubler_label.pack()

        self.sonya_label = ttk.Label(self.controls, text="Sonya Total: 0")
        self.sonya_label.pack()

        # Round selector
        ttk.Label(self.controls, text="Jump to Round:").pack(pady=(10,0))
        self.round_entry = ttk.Entry(self.controls)
        self.round_entry.pack()
        ttk.Button(self.controls, text="Go", command=self.jump_to_round).pack()
        
        # Add replay button
        ttk.Button(self.controls, text="Replay", command=self.replay).pack(pady=10)

    def draw_grid(self):
        self.canvas.delete("all")
        # Draw 20x20 grid
        for i in range(1, 21):
            # Vertical lines
            self.canvas.create_line(cell_size * i, cell_size, cell_size * i, 1050, fill="gray", dash=(1, 1))
            # Horizontal lines
            self.canvas.create_line(cell_size, cell_size * i, 1050, cell_size * i, fill="gray", dash=(1, 1))
            # Labels
            self.canvas.create_text(cell_size * i + 25, 30, text=f"R{i}" if i <= 10 else i)
            self.canvas.create_text(30, cell_size * i + 25, text=str(2**i if i <= 10 else i*10))

    def setup_graph(self):
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.graph_canvas = FigureCanvasTkAgg(self.fig, master=self.controls)
        self.graph_canvas.get_tk_widget().pack()

    def next_round(self):
        if self.round > self.max_rounds:
            return  # Stop if maximum rounds reached

        # Update positions for this round
        self.kobayashi["position"] = [self.round, self.kobayashi["formula"](self.round)]
        self.doubler["position"] = [self.round, self.doubler["formula"](self.round)]
        self.sonya["position"] = [self.round, self.sonya["formula"](self.round)]

        # ✅ Calculate cumulative totals up to current round
        self.kobayashi["cumulative"] = sum(self.kobayashi["formula"](r) for r in range(1, self.round + 1))
        self.doubler["cumulative"] = sum(self.doubler["formula"](r) for r in range(1, self.round + 1))
        self.sonya["cumulative"] = sum(self.sonya["formula"](r) for r in range(1, self.round + 1))

        # 📝 Save positions for replay
        self.history.append({
            "round": self.round,
            "positions": {
                "kobayashi": self.kobayashi["position"],
                "doubler": self.doubler["position"],
                "sonya": self.sonya["position"]
            }
        })

        # 🎨 Redraw competitors + update graph
        self.draw_competitors()
        self.update_graph()

        # 🏷️ Update GUI labels
        self.kobayashi_label.config(text=f"Kobayashi Total: {self.kobayashi['cumulative']}")
        self.doubler_label.config(text=f"Doubler Total: {self.doubler['cumulative']}")
        self.sonya_label.config(text=f"Sonya Total: {self.sonya['cumulative']}")

        # 🔁 Advance to next round
        self.round += 1



    def draw_competitors(self):
        for competitor in [self.kobayashi, self.doubler, self.sonya]:
            x, y = competitor["position"]
            scaled_x = cell_size + (x - 1) * cell_size
            scaled_y = 1050 - (y - 1) * 2  # Scale for visibility
            
            self.canvas.create_oval(scaled_x - 15, scaled_y - 15,
                                  scaled_x + 15, scaled_y + 15,
                                  fill=competitor["color"])
            
            # Label
            self.canvas.create_text(scaled_x, scaled_y - 20, 
                                  text=f"{competitor['formula'](self.round)}")

    def update_graph(self):
        rounds = range(1, self.round + 1)
        self.ax.clear()
        
        # Plot all competitors
        self.ax.plot(rounds, [self.kobayashi["formula"](r) for r in rounds], 'r-', label="Kobayashi (n²)")
        self.ax.plot(rounds, [self.doubler["formula"](r) for r in rounds], 'b-', label="Doubler (2ⁿ)")
        self.ax.plot(rounds, [self.sonya["formula"](r) for r in rounds], 'g-', label="Sonya (n²+n)")
        
        self.ax.legend()
        self.ax.set_xlabel("Round")
        self.ax.set_ylabel("Hot Dogs")
        self.graph_canvas.draw()

    def jump_to_round(self):
        try:
            target = int(self.round_entry.get())
            if 1 <= target <= self.max_rounds:
                self.reset()
                for _ in range(target):
                    self.next_round()
        except ValueError:
            pass

    def replay(self):
        self.reset()
        for frame in self.history:
            self.kobayashi["position"] = frame["positions"]["kobayashi"]
            self.doubler["position"] = frame["positions"]["doubler"]
            self.sonya["position"] = frame["positions"]["sonya"]
            self.round = frame["round"]
            self.draw_competitors()
            self.update_graph()
            self.root.update()
            time.sleep(1/self.speed.get())

    def reset(self):
        self.round = 1
        self.history = []
        self.canvas.delete("all")
        self.draw_grid()
        self.ax.clear()
        self.graph_canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    game = MathCompetitionGame(root)
    root.mainloop()
"""






