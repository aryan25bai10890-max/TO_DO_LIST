import tkinter as tk
from tkinter import ttk, messagebox

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("520x500")
        self.root.resizable(True, True)
        
        # List to store tasks
        self.tasks = []
        
        # Color scheme for different sections
        self.colors = {
            'header': '#4A90E2',      # Blue - Header
            'input': '#50E3C2',       # Teal - Input section
            'buttons': '#FFFFFF',     # WHITE - Buttons (changed to white boxes)
            'list_header': '#F5A623', # Orange - List header
            'list_bg': '#FFFFFF',     # White - List background
            'counter': '#B8E986',     # Green - Counter
            'complete': '#7ED321',    # Green - Completed tasks
            'pending': '#FF6B6B',     # Red - Pending tasks
            'button_text': '#000000'  # BLACK - Button text
        }
        
        # Configure styles
        self.configure_styles()
        
        # Create the GUI
        self.create_widgets()
        
    def configure_styles(self):
        style = ttk.Style()
        
        # Configure different section styles
        style.configure('Header.TFrame', background=self.colors['header'])
        style.configure('Input.TFrame', background=self.colors['input'])
        style.configure('Buttons.TFrame', background=self.colors['buttons'])
        style.configure('ListHeader.TFrame', background=self.colors['list_header'])
        style.configure('List.TFrame', background=self.colors['list_bg'])
        style.configure('Counter.TFrame', background=self.colors['counter'])
        
        # Label styles
        style.configure('Header.TLabel', 
                       background=self.colors['header'],
                       foreground='white',
                       font=('Arial', 18, 'bold'))
        
        style.configure('Input.TLabel',
                       background=self.colors['input'],
                       foreground='#333333',
                       font=('Arial', 10, 'bold'))
        
        style.configure('ListHeader.TLabel',
                       background=self.colors['list_header'],
                       foreground='white',
                       font=('Arial', 11, 'bold'))
        
        style.configure('Counter.TLabel',
                       background=self.colors['counter'],
                       foreground='#333333',
                       font=('Arial', 10, 'bold'))
        
        # Button styles - WHITE buttons with BLACK text
        style.configure('White.TButton',
                       background=self.colors['buttons'],
                       foreground=self.colors['button_text'],  # BLACK text
                       font=('Arial', 9, 'bold'),
                       borderwidth=2,
                       relief='raised',
                       focuscolor='none')
        
        style.map('White.TButton',
                 background=[('active', '#F0F0F0'),  # Slightly darker when hovered
                           ('pressed', '#E0E0E0')])  # Even darker when pressed
        
        # Entry style
        style.configure('Teal.TEntry',
                       fieldbackground='white',
                       foreground='#333333',
                       borderwidth=2,
                       relief='solid')
    
    def create_widgets(self):
        # Header Section - BLUE
        header_frame = ttk.Frame(self.root, style='Header.TFrame', padding="15")
        header_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(header_frame, text="To-Do List", style='Header.TLabel')
        title_label.pack()
        
        # Input Section - TEAL
        input_frame = ttk.Frame(self.root, style='Input.TFrame', padding="15")
        input_frame.pack(fill=tk.X, pady=(0, 5))
        
        input_label = ttk.Label(input_frame, text="✏️ ADD NEW TASK:", style='Input.TLabel')
        input_label.pack(anchor=tk.W, pady=(0, 8))
        
        entry_frame = ttk.Frame(input_frame, style='Input.TFrame')
        entry_frame.pack(fill=tk.X)
        
        self.task_entry = ttk.Entry(entry_frame, style='Teal.TEntry', font=('Arial', 11), width=40)
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        
        add_btn = ttk.Button(entry_frame, text="ADD", command=self.add_task, style='White.TButton', width=8)
        add_btn.pack(side=tk.RIGHT)
        
        # Buttons Section - WHITE (changed from purple)
        buttons_frame = ttk.Frame(self.root, style='Buttons.TFrame', padding="12")
        buttons_frame.pack(fill=tk.X, pady=5)
        
        btn1 = ttk.Button(buttons_frame, text="✅ MARK COMPLETE", 
                         command=self.mark_complete, style='White.TButton', width=18)
        btn1.pack(side=tk.LEFT, padx=5)
        
        btn2 = ttk.Button(buttons_frame, text="❌ DELETE TASK", 
                         command=self.delete_task, style='White.TButton', width=15)
        btn2.pack(side=tk.LEFT, padx=5)
        
        btn3 = ttk.Button(buttons_frame, text="🗑️CLEAR ALL", 
                         command=self.clear_all, style='White.TButton', width=18)
        btn3.pack(side=tk.LEFT, padx=5)
        
        # List Header - ORANGE
        list_header_frame = ttk.Frame(self.root, style='ListHeader.TFrame', padding="10")
        list_header_frame.pack(fill=tk.X, pady=(10, 0))
        
        list_title = ttk.Label(list_header_frame, text="📋 YOUR TASKS", style='ListHeader.TLabel')
        list_title.pack()
        
        # Task List Section - WHITE
        list_frame = ttk.Frame(self.root, style='List.TFrame', padding="15")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Custom treeview style for the list
        style = ttk.Style()
        style.configure("Colorful.Treeview",
                       background="white",
                       foreground="#333333",
                       fieldbackground="white",
                       rowheight=25)
        
        style.configure("Colorful.Treeview.Heading",
                       background=self.colors['list_header'],
                       foreground='white',
                       relief='flat',
                       font=('Arial', 10, 'bold'))
        
        style.map("Colorful.Treeview.Heading",
                 background=[('active', '#E5961A')])
        
        # Treeview for tasks
        columns = ('Status', 'Task')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', 
                                height=15, style="Colorful.Treeview")
        
        # Define headings
        self.tree.heading('Status', text='STATUS')
        self.tree.heading('Task', text='TASK DESCRIPTION')
        
        # Set column widths
        self.tree.column('Status', width=120, anchor=tk.CENTER)
        self.tree.column('Task', width=360, anchor=tk.W)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Configure treeview tags for colored rows
        self.tree.tag_configure('completed', background='#F0F8F0', foreground=self.colors['complete'])
        self.tree.tag_configure('pending', background='#FFF0F0', foreground=self.colors['pending'])
        
        # Counter Section - GREEN
        counter_frame = ttk.Frame(self.root, style='Counter.TFrame', padding="12")
        counter_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.counter_label = ttk.Label(counter_frame, text="📊 Total Tasks: 0 | ✅ Completed: 0 | ⏳ Pending: 0", 
                                      style='Counter.TLabel')
        self.counter_label.pack()
        
        # Double-click to mark complete/incomplete
        self.tree.bind('<Double-1>', self.toggle_status)
        
        # Focus on entry when app starts
        self.task_entry.focus()
    
    def add_task(self):
        task_text = self.task_entry.get().strip()
        
        if not task_text:
            messagebox.showwarning("Warning", "Please enter a task!")
            return
        
        # Add to tasks list
        task = {
            'text': task_text,
            'completed': False
        }
        self.tasks.append(task)
        
        # Add to treeview with color tag
        item_id = self.tree.insert('', tk.END, values=('🔴 PENDING', task_text), tags=('pending',))
        
        # Clear entry
        self.task_entry.delete(0, tk.END)
        
        # Update counter
        self.update_counter()
        
        # Focus back to entry
        self.task_entry.focus()
    
    def mark_complete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task!")
            return
        
        for item in selected:
            # Update in treeview
            current_values = self.tree.item(item, 'values')
            if 'PENDING' in current_values[0]:
                self.tree.set(item, 'Status', '✅ COMPLETED')
                self.tree.item(item, tags=('completed',))
                # Update in tasks list
                index = self.tree.index(item)
                if index < len(self.tasks):
                    self.tasks[index]['completed'] = True
        
        self.update_counter()
    
    def toggle_status(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        
        item = selected[0]
        current_values = self.tree.item(item, 'values')
        
        if 'PENDING' in current_values[0]:
            self.tree.set(item, 'Status', '✅ COMPLETED')
            self.tree.item(item, tags=('completed',))
            # Update in tasks list
            index = self.tree.index(item)
            if index < len(self.tasks):
                self.tasks[index]['completed'] = True
        else:
            self.tree.set(item, 'Status', '🔴 PENDING')
            self.tree.item(item, tags=('pending',))
            # Update in tasks list
            index = self.tree.index(item)
            if index < len(self.tasks):
                self.tasks[index]['completed'] = False
        
        self.update_counter()
    
    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to delete!")
            return
        
        if messagebox.askyesno("Confirm", "Delete selected task(s)?"):
            # Delete from treeview (in reverse order to avoid index issues)
            for item in reversed(selected):
                index = self.tree.index(item)
                self.tree.delete(item)
                # Delete from tasks list
                if index < len(self.tasks):
                    self.tasks.pop(index)
            
            self.update_counter()
    
    def clear_all(self):
        if not self.tasks:
            messagebox.showinfo("Info", "No tasks to clear!")
            return
        
        if messagebox.askyesno("Confirm", "Clear ALL tasks?"):
            self.tree.delete(*self.tree.get_children())
            self.tasks.clear()
            self.update_counter()
    
    def update_counter(self):
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task['completed'])
        pending = total - completed
        
        self.counter_label.config(text=f"📊 Total Tasks: {total} | ✅ Completed: {completed} | ⏳ Pending: {pending}")

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()