import tkinter as tk
from tkinter import ttk

# Create a GUI window
window = tk.Tk()

# Create a notebook widget
tab_control = ttk.Notebook(window)

# Create two tabs
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)

# Add the tabs to the notebook widget
tab_control.add(tab1, text=f'{"Tab 1":^40s}')
tab_control.add(tab2, text=f'{"Tab 2":^40s}')

# Change the background color of the second tab to yellow
tab_control.tab(tab2, option='configure', background='yellow')

# Pack the notebook widget
tab_control.pack(expand=1, fill='both', padx=10, pady=10)

# Run the main event loop
window.mainloop()
