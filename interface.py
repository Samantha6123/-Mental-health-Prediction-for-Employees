import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *
import tkinter.filedialog
from tkinter import font
import csv

from PIL import Image, ImageTk

from input_preprocess import input_test



window = Tk()
window.title("Mental Health Prediction")
window.geometry("1250x750")

window.configure(background="lavender")
my_font1 = font.Font(family='Verdana', size=14)
my_font2 = font.Font(family='Helvetica', size=16)
my_font3 = font.Font(family='Verdana', size=12)


style = ttk.Style(window)
style.configure('lefttab.TNotebook', tabposition='wn')

tab_control = ttk.Notebook(window,style='lefttab.TNotebook', width=500, height=1000)



tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)

#adding tabs
tab_control.add(tab1, text=f'{"PREDICTION":^40s}')
tab_control.add(tab2, text=f'{"ABOUT":^40s}')
tab_control.add(tab3, text=f'{"INSTRUCTIONS":^40s}')




label1 = Label(tab1, text= 'Predict Employee Mental Health',padx=5, pady=5, font=my_font2, fg="purple4")
label1.grid(column=0, row=0)

tab_control.pack(expand=1, fill='both',padx=10,pady=10)


#functions------------------
def openfiles():
	file1 = tkinter.filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

	read_text = open(file1).read()
	displayed_file.insert(tk.END,read_text)
	return file1
	
def predict_mhc():
	raw_text = displayed_file.get('1.0',tk.END)
	print(raw_text)
	final_text = input_test(openfiles())
	result = '\nResult:{}'.format(final_text)
	tab1_display_text.insert(tk.END,result)
	

'''def load_csv_file():
    # Prompt the user to select a CSV file
    csv_file_path = tkinter.filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    
    # Read the CSV file and store the data
    with open(csv_file_path, newline='') as csvfile:
        csv_data = list(csv.reader(csvfile))
    
    # Call your tkinter function with the CSV data
    input_test(csv_data)'''

#Prediction Tab-------------------------------------------------------
l1=Label(tab1,text="Upload the csv file",font=my_font1)
l1.grid(row=1,column=0)

displayed_file = ScrolledText(tab1,height=12,width=130)
displayed_file.grid(row=2,column=0, columnspan=5,padx=5,pady=3)

#buttons
b20=Button(tab1,text="OPEN FILE", width=12,command=openfiles,bg='purple3',fg='#fff')
b20.grid(row=3,column=0,padx=3,pady=5)

#b21=Button(tab2,text="Reset ", width=12,command=clear_text_file,bg="#b9f6ca")
#b21.grid(row=3,column=1,padx=10,pady=10)

b22=Button(tab1,text="PREDICT", width=12,command=predict_mhc,bg='purple3',fg='#fff')
b22.grid(row=3,column=1,padx=3,pady=5)

b24=Button(tab1,text="CLOSE", width=12,command=window.destroy,bg='purple3',fg='#fff')
b24.grid(row=4,column=0,padx=3,pady=5)

tab1_display_text = Text(tab1)
tab1_display_text = ScrolledText(tab1,height=12,width=130)
tab1_display_text.grid(row=7,column=0, columnspan=3,padx=5,pady=5)


# About TAB-----------------------------------------------------

# Load the image
image = Image.open("m2.jpg")
photo = ImageTk.PhotoImage(image)

# Create the image label and add it to the window
image_label = tk.Label(tab2, image=photo)
image_label.grid(row=0, column=0, columnspan=2)


paragraph_text = "\nMental health issues are a significant concern in the tech industry, with many employees facing high levels of stress and burnout. However, despite the availability of mental health treatment, many employees may not seek help due to various reasons such as stigma, lack of awareness, or fear of discrimination.\nTo address this issue, we aim to develop a machine learning model that can predict whether an employee in a tech company needs mental health treatment or not based on their background data acquired. "
paragraph_var=tk.StringVar()
paragraph_var.set(paragraph_text)
paragraph_label = tk.Label(tab2, textvariable=paragraph_var, justify="left", wraplength=600, font=my_font1)
paragraph_label.grid()

quote_text= "\n\n\nMental health is not a destination, but a process. It's about how you drive, not where you're going..."
quote_var=tk.StringVar()
quote_var.set(quote_text)
quote_label= tk.Label(tab2, textvariable=quote_var, justify="left", wraplength=600, font=my_font2,fg="purple4")
quote_label.grid()


#Instructions TAB----------------------------------------------

l3=Label(tab3,text="INSTRUCTIONS",font=my_font1)
l3.grid(row=0,column=0)

par = "The uploded csv files should be in the format given below:"
par_var=tk.StringVar()
par_var.set(par)
par_label = tk.Label(tab3, textvariable=par_var, justify="left", wraplength=600, font=my_font1)
par_label.grid()

# Load the image
image1 = Image.open("Screenshot.png")
photo1 = ImageTk.PhotoImage(image1)

# Create the image label and add it to the window
image_label1 = tk.Label(tab3, image=photo1)
image_label1.grid(row=2, column=0)

p = "\n1.Input CSV file must contain the above features.\n\n2.When you upload the file, the data will be displayed and you need to select the file again.\n\n3.Click on the predict button to get the results (Note: The results will be automatically saved into your systems)\n\n4.In output, '1' represents that the employee needs treatment."
p_var=tk.StringVar()
p_var.set(p)
p_label = tk.Label(tab3, textvariable=p_var, justify="left", wraplength=1000, font=my_font3)
p_label.grid()

window.mainloop()


