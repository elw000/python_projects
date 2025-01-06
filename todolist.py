import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class TodoApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Todo List")
        self.root.geometry("500x600")
        self.root.configure(bg="#f0f0f0")

        # Task storage
        self.tasks = []
        self.load_tasks()
        
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Task entry
        self.task_var = tk.StringVar()
        self.task_entry = ttk.Entry(self.main_frame, textvariable=self.task_var, width=40)
        self.task_entry.grid(row=0, column=0, padx=5, pady=5)
        
        # Priority selection
        self.priority_var = tk.StringVar(value="Medium")
        self.priority_combo = ttk.Combobox(self.main_frame, 
                                         textvariable=self.priority_var,
                                         values=["High", "Medium", "Low"],
                                         width=10)
        self.priority_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Add button
        self.add_button = ttk.Button(self.main_frame, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Task listbox
        self.task_listbox = tk.Listbox(self.main_frame, width=60, height=20)
        self.task_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        
        # Buttons frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=2, column=0, columnspan=3, pady=5)
        
        # Control buttons
        ttk.Button(self.button_frame, text="Complete", command=self.complete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Edit", command=self.edit_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Delete", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        
        self.refresh_tasks()
        
    def add_task(self):
        task = self.task_var.get().strip()
        if task:
            priority = self.priority_var.get()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.tasks.append({
                "task": task,
                "priority": priority,
                "timestamp": timestamp,
                "completed": False
            })
            self.task_var.set("")
            self.save_tasks()
            self.refresh_tasks()
        
    def complete_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            self.tasks[index]["completed"] = True
            self.save_tasks()
            self.refresh_tasks()
            
    def edit_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            task = self.tasks[index]
            
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Task")
            edit_window.geometry("300x150")
            
            ttk.Label(edit_window, text="Task:").pack(pady=5)
            edit_var = tk.StringVar(value=task["task"])
            edit_entry = ttk.Entry(edit_window, textvariable=edit_var, width=40)
            edit_entry.pack(pady=5)
            
            priority_var = tk.StringVar(value=task["priority"])
            priority_combo = ttk.Combobox(edit_window, 
                                        textvariable=priority_var,
                                        values=["High", "Medium", "Low"])
            priority_combo.pack(pady=5)
            
            def save_edit():
                task["task"] = edit_var.get()
                task["priority"] = priority_var.get()
                self.save_tasks()
                self.refresh_tasks()
                edit_window.destroy()
                
            ttk.Button(edit_window, text="Save", command=save_edit).pack(pady=10)
            
    def delete_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
                index = selection[0]
                del self.tasks[index]
                self.save_tasks()
                self.refresh_tasks()
    
    def refresh_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✓ " if task["completed"] else "  "
            priority_marker = {
                "High": "🔴",
                "Medium": "🟡",
                "Low": "🟢"
            }.get(task["priority"], "")
            
            task_text = f"{status}{priority_marker} {task['task']} ({task['timestamp']})"
            self.task_listbox.insert(tk.END, task_text)
            
            if task["completed"]:
                index = self.task_listbox.size() - 1
                self.task_listbox.itemconfig(index, fg="gray")
    
    def save_tasks(self):
        try:
            with open("tasks.json", "w") as f:
                json.dump(self.tasks, f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {e}")
    
    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                self.tasks = json.load(f)
        except FileNotFoundError:
            self.tasks = []
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tasks: {e}")
            self.tasks = []
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TodoApp()
    app.run()
