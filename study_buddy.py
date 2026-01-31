import tkinter as tk
from tkinter import messagebox
import time
from datetime import datetime
import json
import os

DATA_FILE = "items.json"

#Creating main application class
class StudyPartnerApp:
    def __init__(self, source):
        self.source = source
        self.source.title("Study Partner")
        self.source.geometry("700x500")
        self.source.resizable(False, False)

        # Attributes
        self.energy = 100
        self.happiness = 50
        self.tasks_complete = 0
        self.tasks = self.load_items()

        # UI Setup
        self.create_widgets()

        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)

        self.update_clock()
        self.update_partner_state()
        self.source.protocol("WM_DELETE_WINDOW", self.on_close)
        self.display_warning()

    # UI Layout
    def create_widgets(self):
        # Left side: Drawing + stats
        left_frame = tk.Frame(self.source, padx=10, pady=10)
        left_frame.pack(side="left", fill="y")

        self.canvas = tk.Canvas(left_frame, width=250, height=250, bg="#f0f8ff")
        self.canvas.pack()

        self.stats_label = tk.Label(left_frame, text="", font=("Arial", 11))
        self.stats_label.pack(pady=10)

        self.clock_label = tk.Label(left_frame, font=("Arial", 14, "bold"))
        self.clock_label.pack()

        # Right side: Task manager
        right_frame = tk.Frame(self.source, padx=10, pady=10)
        right_frame.pack(side="right", fill="both", expand=True)

        tk.Label(right_frame, text="Tasks", font=("Arial", 14, "bold")).pack()

        self.task_entry = tk.Entry(right_frame, font=("Arial", 11))
        self.task_entry.pack(fill="x", pady=5)

        add_btn = tk.Button(right_frame, text="Add Task", command=self.add_task)
        add_btn.pack(pady=2)

        self.task_listbox = tk.Listbox(right_frame, font=("Arial", 11), height=10)
        self.task_listbox.pack(fill="both", expand=True, pady=5)

        del_btn = tk.Button(right_frame, text="Complete Selected Task", command=self.complete_task)
        del_btn.pack(pady=5)

    #Clock + Time
    def update_clock(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.clock_label.config(text=f"Time: {current_time}")
        self.source.after(1000, self.update_clock)

    def time_of_day(self):
        hour = datetime.now().hour
        if 6 <= hour < 12:
            return "morning"
        elif 12 <= hour < 18:
            return "afternoon"
        else:
            return "night"

    #Study Partner Drawing
    def draw_partner(self, mood):
        self.canvas.delete("all")

        # Face
        self.canvas.create_oval(50, 50, 200, 200, fill="#ffebcd", outline="black")

        # Eyes
        self.canvas.create_oval(85, 90, 105, 110, fill="black")
        self.canvas.create_oval(145, 90, 165, 110, fill="black")

        # Mouth based on mood
        if mood == "happy":
            self.canvas.create_arc(90, 120, 160, 170, start=180, extent=180, width=3)
        elif mood == "tired":
            self.canvas.create_line(85, 150, 95, 160, width=3)
            self.canvas.create_line(95, 160, 105, 150, width=3)
            self.canvas.create_line(105, 150, 115, 160, width=3)
            self.canvas.create_line(115, 160, 125, 150, width=3)
            self.canvas.create_line(125, 150, 135, 160, width=3)
            self.canvas.create_line(135, 160, 145, 150, width=3)
            self.canvas.create_line(145, 150, 155, 160, width=3)
            self.canvas.create_line(155, 160, 165, 150, width=3)
            self.canvas.create_oval(85, 90, 105, 110, fill="dark red")
            self.canvas.create_oval(145, 90, 165, 110, fill="dark red")
        else:  # neutral
            self.canvas.create_line(80, 150, 170, 150, width=4)

        # Text mood indicator
        self.canvas.create_text(125, 230, text=mood.upper(), font=("Arial", 10, "bold"))

    #Attribute Updates
    def update_partner_state(self):
        time_of_day = self.time_of_day()

        # Mood
        if self.energy < 30:
            mood = "tired"
        elif self.happiness > 60:
            mood = "happy"
        else:
            mood = "neutral"

        self.draw_partner(mood)

        self.stats_label.config(
            text=f"Energy: {self.energy}\nHappiness: {self.happiness}\nTasks Completed: {self.tasks_complete}")
        
        self.source.after(3000, self.update_partner_state)
        self.source.after(864000, self.lose_energy)

    def lose_energy(self):

         self.energy = max(0, self.energy - 1)


    def display_warning(self) :
        if self.energy <= 30:
            messagebox.showinfo("lock in", "do task u chud")
        self.source.after(5000, self.display_warning)

    #Task Management
    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append(task)
            self.task_listbox.insert(tk.END, task)
            self.save_items()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Empty Task", "Please enter a task.")

    def complete_task(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a task to complete.")
            return

        index = selected[0]
        self.task_listbox.delete(index)
        del self.tasks[index]
        self.save_items()

        # Reward system
        self.happiness = min(100, self.happiness + 5)
        self.tasks_complete += 1

        if self.energy < 30:
            self.energy = min(100, self.energy + 1)
        else:
            self.energy = min(100, self.energy + 2)
        
        messagebox.showinfo("Great job!", "Task completed! 🎉")

    def load_items(self):
      if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
          return json.load(f)
        return[]

    def save_items(self):
      with open(DATA_FILE, "w") as f:
        json.dump(self.tasks, f)

    def on_close(self):
      self.save_items()
      self.source.destroy()

# Run Application
if __name__ == "__main__":
    root = tk.Tk()
    app = StudyPartnerApp(root)
    root.mainloop()
