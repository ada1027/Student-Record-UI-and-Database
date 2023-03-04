import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from tkcalendar import DateEntry 
from datetime import date
from database import Database
from sortableListBox import Sortable_list_box
import sv_ttk
import csv

def clear_fields():
    global selected_student_id
    selected_student_id = 0
    set_text(first_name_entry, "", True)
    set_text(last_name_entry, "", True)
    grade_combobox.config(state=NORMAL)
    grade_combobox.set("")
    new_student.config(state=NORMAL)

# add_student button event handler
def add_student(): 
    global selected_student_id
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    if (first_name and last_name):
        grade_value = grade_combobox.get()
        if grade_value:
            grade = grade_dict[grade_value] 
            selected_student_id = db.insert_student(first_name, last_name, grade)
            if selected_student_id > 0:
                new_student.config(state=DISABLED)
                first_name_entry.configure(state=DISABLED)
                last_name_entry.config(state=DISABLED)
                grade_combobox.config(state=DISABLED)
        else:
            messagebox.showwarning(title="Error", message="Please select a grade")
    else:
        messagebox.showwarning(title="Error", message="Not all fields filled.")

def add_event():
    global selected_student_id
    if selected_student_id == 0:
        add_student()

    if selected_student_id > 0:
        event_date = cal.get_date()
        event_selection = events_combobox.get()
        event_name, separator, tail = event_selection.partition(' (')
        quarter = quarter_spinbox.get()
        involvement = title_combobox.get()
        points = get_event_points(event_name, involvement)
        all_fields = event_date and event_name and involvement and quarter and points
        if all_fields:
            print(selected_student_id)
            db.insert_event(selected_student_id, event_date, quarter, event_name, involvement, points)
        else:
            messagebox.showwarning(title="Error", message="Not all fields filled.")
    else:
        messagebox.showwarning(title="Error", message="Student info missing")

def reset_event_fields():
    events_combobox.set("")
    title_combobox.set("")

def get_event_points(event_name, involvement):
    if involvement == "Participant":
        return event_dict[event_name][0]
    else:
        return event_dict[event_name][1]

# when a student is selected, set name and grade fields and disable those fields
def student_selected(event):
    global selected_student_tuple
    selected_student_tuple = student_list_box.tree.item(student_list_box.tree.focus())["values"]
    if selected_student_tuple:
        # print(selected_student_tuple) # [2, 'first_name', 'last_name', 10, 100]
        global selected_student_id
        selected_student_id = selected_student_tuple[0]
        items = db.get_student_events(selected_student_id)
        event_item = map(lambda x: x[2:], items)
        event_list_box.show_items(event_item)
        new_student.config(state=DISABLED)
        set_text(first_name_entry, selected_student_tuple[1], False)
        set_text(last_name_entry, selected_student_tuple[2], False)
        grade_combobox.current(selected_student_tuple[3] - 9)
        grade_combobox.config(state=DISABLED)
        reset_event_fields()

def set_text(text_field, value, enabled):
    text_field.config(state=NORMAL) # eanble text_field first so that it's editable
    text_field.delete(0, END)
    if value:
        text_field.insert(0, value)
    if enabled:
        text_field.config(state=NORMAL)
    else:
        text_field.config(state=DISABLED)

def search_by_name():
    keyWord = search_input.get()
    if (keyWord):
        items = db.search_by_name(keyWord)
        student_list_box.show_items(items) 
        event_list_box.show_items([])  
    else:
        messagebox.showwarning(title="Error", message="please type a name to search.")

def view_all_students():
    items = db.get_all_students()
    student_list_box.show_items(items)
    event_list_box.show_items([])
    global selected_student_id
    selected_student_id = 0
    new_student.config(state=NORMAL)

def get_grade_students():
    grade_value = grade_filter_combobox.get()
    if grade_value:
        grade = grade_dict[grade_value]
        items = db.get_all_students(grade)
        return items
    else:
        messagebox.showwarning(title="Error", message="please select a grade.")

def view_grade_students():
    grade_students = get_grade_students()
    event_list_box.show_items([])
    student_list_box.show_items(grade_students)

def export_grade_students():
    grade_student = get_grade_students()
    with open('students.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["First Name", "Last Name", "Grade", "Points"])
        for row in grade_student:
            writer.writerow(row[1:])

def open_about_window(): 
    about_window = Toplevel(window)
    about_window.geometry("400x100")
    about_window.grid()
    about_window.title("About")
    info = "This is a program to log and reward student participation in schools."
    info += "\n Created by Ada and Zoe, February 2023"
    tkinter.Label(about_window,justify=tkinter.CENTER,text=info).pack(padx=5,pady=10)
    tkinter.Button(about_window,text='OK',width=10,command=about_window.destroy).pack(pady=10)
    about_window.transient(window)
    about_window.grab_set()
    about_window.wait_window(about_window)

def open_instructions_window():
    instructions_window = Toplevel(window)
    instructions_window.geometry("600x200")
    instructions_window.grid()
    instructions_window.title("Instructions")
    info = "To add new student, fill in fields and click 'Add New Student' \n To display all students on leaderboard, click 'Show All Students'\n To add new event, select student, log an event and click 'Add New Event'"
    info += "\n To see event logs, select student on leaderboard by clicking on name \n To see students in a grade, select grade and click 'View Students in Grade' \n To search for a student, type name in text box and click 'Search By Name'"
    info += "\n To clear all fields in Student Information, click 'Reset'"
    tkinter.Label(instructions_window,justify=tkinter.CENTER, text=info).pack(padx=5,pady=10)
    tkinter.Button(instructions_window,text='OK',width=10, command=instructions_window.destroy ).pack(pady=10)
    instructions_window.transient(window)
    instructions_window.grab_set()
    instructions_window.wait_window(instructions_window)

def toggle_theme():
    if sv_ttk.get_theme() == "dark":
        sv_ttk.use_light_theme()
    elif sv_ttk.get_theme() == "light":
        sv_ttk.use_dark_theme()
    else:
        print("Not Sun Valley theme")

# connect to sqlite database
db = Database()

window = tkinter.Tk()
window.title("Student Record Update")

sv_ttk.use_light_theme()
# sv_ttk.set_theme("dark")

menubar = tkinter.Menu(window)
window.config(menu=menubar)

help_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help",menu=help_menu)
help_menu.add_command(label="Instruction",command = open_instructions_window)
help_menu.add_command(label="About", command=open_about_window)
button = ttk.Button(window, text="Toggle theme", command=toggle_theme)
help_menu.add_command(label="Toggle Theme", command = toggle_theme)
help_menu.add_separator()
help_menu.add_command(label="Exit",command=window.quit)

window.columnconfigure(0,weight=1)
window.columnconfigure(1,weight=3)

frame = tkinter.Frame(window)
frame.grid(row=0,column=0,sticky="nsew")

# Saving User Info
user_info_frame =tkinter.LabelFrame(frame, text=" Student Information ")
user_info_frame.grid(row= 0, column=0, sticky = "nsew", padx=20, pady=5)

first_name_label = tkinter.Label(user_info_frame, text="First Name")
first_name_label.grid(row=0, column=0,sticky="nsew")
last_name_label = tkinter.Label(user_info_frame, text="Last Name")
last_name_label.grid(row=0, column=1,sticky="nsew")

first_name_entry = tkinter.Entry(user_info_frame)
last_name_entry = tkinter.Entry(user_info_frame)
first_name_entry.grid(row=1, column=0,sticky="nsew",padx=20,pady=10)
last_name_entry.grid(row=1, column=1,sticky="nsew",padx=20,pady=10)

# grades
grade_label = tkinter.Label(user_info_frame, text = "Select Grade: ")
grade_dict = {"Grade 9": 9, "Grade 10": 10, "Grade 11": 11, "Grade 12": 12}
grade_combobox = ttk.Combobox(user_info_frame, state="readonly", values=list(grade_dict.keys()), width = 17)
grade_label.grid(row=2, column=0,sticky="nsew",padx = 15)
grade_combobox.grid(row=3, column=0,padx=20,sticky="nsew", pady = 10)

#Clear Fields
clear_field = tkinter.Button(user_info_frame,text="Reset", command = clear_fields)
clear_field.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)

#Register New Student
new_student = tkinter.Button(user_info_frame, text="Add New Student", command=add_student)
new_student.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)


#event logs
event_frame = tkinter.LabelFrame(frame, text = "Event Log: ")
event_frame.grid(row=4, column = 0,sticky = "nsew",padx = 20, pady = 5)

# selected student id before inserting an event
selected_student_id = 0
# two points for each event, one for participant another for attendant
event_dict = { "Basketball Game":(50, 10), "Baseball Game":(50, 10), "Volleyball Game":(50, 10), "Soccer Game":(50, 10), "Tennis":(50, 10),
                "Talent Show":(50, 10), "Christmas Concert":(50, 10), "Spring Concert":(50, 10), "Mass":(50, 10), "Prayer":(50, 10)}
# show "Basketball Game" in event selection
event_list = list(event_dict.keys())
events_label = tkinter.Label(event_frame, text="Event: ")
events_combobox = ttk.Combobox(event_frame, state="readonly", values=event_list, width = 22)
events_label.grid(row=0, column=0,sticky="nsew")
events_combobox.grid(row=1, column=0,sticky="nsew",padx=20, pady=10)

title_label = tkinter.Label(event_frame, text="Participation")
title_combobox = ttk.Combobox(event_frame, state="readonly", values=["Participant", "Attendant"], width = 12)
title_label.grid(row=0, column=1,sticky="nsew",padx = 15)
title_combobox.grid(row=1, column=1,sticky="nsew",padx=10, pady = 10)

date_label=tkinter.Label(event_frame,text='Date: ')
date_label.grid(row=3,column=0,sticky="nsew")
cal=DateEntry(event_frame,selectmode='day',width=22)
cal.grid(row=4,column=0,padx=20,pady=10)
cal.set_date(date.today()) # todays date 

quarter_label = tkinter.Label(event_frame, text="Quarter: ")
quarter_spinbox = tkinter.Spinbox(event_frame, from_=1, to=4,width=12)
quarter_label.grid(row=3, column=1,sticky="nsew")
quarter_spinbox.grid(row=4, column=1, sticky="nsew",padx=10, pady=10)

button = tkinter.Button(frame, text="Add Event", command=add_event)
button.grid(row=5, column=0, sticky="nsew", padx=20, pady=10)

# Filters
left_frame = tkinter.Frame(window)
left_frame.grid(row = 0, column = 1, sticky= "nsew")

search_button = tkinter.Button(left_frame, text = "Search By Name", command=search_by_name)
search_button.grid(row = 0, column = 2)
search_input = tkinter.Entry(left_frame)
search_input.grid(row = 0, column = 1, sticky="nsew", pady= 10)

grade_filter_combobox = ttk.Combobox(left_frame, state="readonly", values=list(grade_dict.keys()), width = 17)
grade_filter_combobox.grid(row=1, column=1,sticky="nsew")
grade_filter_combobox.current(0)

view_grade_button = tkinter.Button(left_frame, text = "View Students in Grade", command=view_grade_students)
view_grade_button.grid(row = 1, column = 2,sticky="nsew",padx=10)

export_grade_button = tkinter.Button(left_frame, text = "Export Students Records", command=export_grade_students)
export_grade_button.grid(row = 1, column = 0,sticky="nsew",padx=10)

view_all_button = tkinter.Button(left_frame, text="Show All Students", command=view_all_students,width=0)
view_all_button.grid(row = 0, column = 0)

#Leaderboard
leaderboard_frame = tkinter.Frame(left_frame)
leaderboard_frame.grid(row=5,column=0,sticky="nsew",pady=10,columnspan=3)

student_list_box = Sortable_list_box(ttk, leaderboard_frame, ["ID", "First Name", "Last Name", "Grades", "Total Points"],8)
student_list_box.tree.bind('<ButtonRelease-1>', student_selected)
event_list_box = Sortable_list_box(ttk, leaderboard_frame, ["Date", "Quarter","Event", "Involvement", "Points"],5)

window.mainloop()
