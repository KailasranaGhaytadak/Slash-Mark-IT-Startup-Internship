import tkinter as tk
from tkinter import messagebox

class Task:
    def __init__(self, description, priority):
        self.description = description
        self.priority = priority

class TaskManagerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Task Manager")

        self.tasks = []

        self.label_description = tk.Label(master, text="Task Description:", font=("Arial", 12, "bold"))
        self.label_description.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        self.entry_description = tk.Entry(master, font=("Arial", 12))
        self.entry_description.grid(row=0, column=1, padx=10, pady=5)

        self.label_priority = tk.Label(master, text="Priority (H/M/L):", font=("Arial", 12, "bold"))
        self.label_priority.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        self.entry_priority = tk.Entry(master, font=("Arial", 12))
        self.entry_priority.grid(row=1, column=1, padx=10, pady=5)

        self.button_add = tk.Button(master, text="Add Task", command=self.add_task, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white")
        self.button_add.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W+tk.E)

        self.button_list = tk.Button(master, text="List Tasks", command=self.list_tasks, font=("Arial", 12, "bold"), bg="#008CBA", fg="white")
        self.button_list.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W+tk.E)

        self.button_delete = tk.Button(master, text="Delete Task", command=self.delete_task, font=("Arial", 12, "bold"), bg="#FF5733", fg="white")
        self.button_delete.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W+tk.E)

        self.button_delete_all = tk.Button(master, text="Delete All Tasks", command=self.delete_all_tasks, font=("Arial", 12, "bold"), bg="#FF5733", fg="white")
        self.button_delete_all.grid(row=5, column=1, padx=10, pady=5, sticky=tk.W+tk.E)

        self.button_recommend = tk.Button(master, text="Recommend Task", command=self.recommend_task, font=("Arial", 12, "bold"), bg="#8E44AD", fg="white")
        self.button_recommend.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W+tk.E)

        self.button_exit = tk.Button(master, text="Exit", command=master.quit, font=("Arial", 12, "bold"), bg="#FF5733", fg="white")
        self.button_exit.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W+tk.E)

        self.listbox_tasks = tk.Listbox(master, width=50, height=10, font=("Arial", 12))
        self.listbox_tasks.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    def add_task(self):
        description = self.entry_description.get().strip()
        priority = self.entry_priority.get().strip().upper()

        if not description:
            messagebox.showwarning("Warning", "Please enter a task description.")
            return

        if priority not in {'H', 'M', 'L'}:
            messagebox.showwarning("Warning", "Invalid priority input. Please enter 'H', 'M', or 'L'.")
            return

        for task in self.tasks:
            if task.description == description:
                confirmed = messagebox.askyesno("Confirmation", "Task '{}' already exists in the list. Do you want to change its priority?".format(description))
                if confirmed:
                    task.priority = priority
                    messagebox.showinfo("Success", "Priority of Task '{}' changed successfully to '{}'.".format(description, priority))
                    self.entry_description.delete(0, tk.END)
                    self.entry_priority.delete(0, tk.END)
                    self.list_tasks()
                return

        self.tasks.append(Task(description, priority))
        messagebox.showinfo("Success", "Task '{}' added successfully with priority '{}'.".format(description, priority))
        self.entry_description.delete(0, tk.END)
        self.entry_priority.delete(0, tk.END)

    def list_tasks(self):
        self.listbox_tasks.delete(0, tk.END)

        if not self.tasks:
            messagebox.showinfo("Information", "No tasks available.")
            return

        sorted_tasks = sorted(self.tasks, key=lambda x: ('High' if x.priority == 'H' else 'Medium' if x.priority == 'M' else 'Low'))
        for task in sorted_tasks:
            priority_full_form = {'H': 'High', 'M': 'Medium', 'L': 'Low'}
            self.listbox_tasks.insert(tk.END, "Task: {} - Priority: {}".format(task.description, priority_full_form[task.priority]))

        # Increase font size of added tasks in the listbox
        self.listbox_tasks.config(font=("Arial", 14))

    def delete_task(self):
        selected_task_index = self.listbox_tasks.curselection()
        if not selected_task_index:
            messagebox.showwarning("Warning", "Please select a task to delete.")
            return

        task_description = self.listbox_tasks.get(selected_task_index[0])
        description = task_description.split(" - ")[0].split(": ")[1]

        for task in self.tasks:
            if task.description == description:
                self.tasks.remove(task)
                break

        self.listbox_tasks.delete(selected_task_index)

        messagebox.showinfo("Success", "Task '{}' deleted successfully.".format(description))

    def delete_all_tasks(self):
        if not self.tasks:
            messagebox.showinfo("Information", "No tasks available to delete.")
            return

        confirmed = messagebox.askyesno("Confirmation", "Are you sure you want to delete all tasks?")
        if confirmed:
            self.tasks = []
            self.listbox_tasks.delete(0, tk.END)
            messagebox.showinfo("Success", "All tasks deleted successfully.")

    def recommend_task(self):
        if not self.tasks:
            messagebox.showinfo("Information", "No tasks available to recommend.")
            return

        high_priority_tasks = [task for task in self.tasks if task.priority == 'H']
        if high_priority_tasks:
            recommended_task = high_priority_tasks[0]
        else:
            medium_priority_tasks = [task for task in self.tasks if task.priority == 'M']
            if medium_priority_tasks:
                recommended_task = medium_priority_tasks[0]
            else:
                recommended_task = self.tasks[0]

        messagebox.showinfo("Recommendation", f"Recommended Task: {recommended_task.description} - Priority: {recommended_task.priority}")

def main():
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
