import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from tkcalendar import DateEntry 
from datetime import date
from database import Database
from sortableListBox import Sortable_list_box
import csv

db = Database()
selected_student_id = 0

def add_student(): # add_student button event handler
    global selected_student_id
    if selected_student_id != 0:
        selected_student_id = 0
        set_text(first_name_entry, "", True)
        set_text(last_name_entry, "", True)
        grade_combobox.config(state=NORMAL)
        grade_combobox.set("")
    else:
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        if (first_name and last_name):
            grade_value = grade_combobox.get()
            if grade_value:
                grade = grade_dict[grade_value] 
                selected_student_id = db.insert_student(first_name, last_name, grade)
                if selected_student_id > 0:
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
        event_name = events_combobox.get()
        involvement = title_combobox.get()
        points = points_spinbox.get()
        all_fields = event_date and event_name and involvement and points
        if all_fields:
            db.insert_event(selected_student_id, event_date, event_name, involvement, points)
        else:
            messagebox.showwarning(title="Error", message="Not all fields filled.")
    else:
        messagebox.showwarning(title="Error", message="Student info missing")

def reset_event_fields():
    events_combobox.set("")
    title_combobox.set("")

def student_selected(event):
    global selected_student_tupel
    selected_student_tuple = student_list_box.tree.item(student_list_box.tree.focus())["values"]
    if selected_student_tuple:
        # print(selected_student_tuple) # [2, 'first_name', 'last_name', 10, 100]
        global selected_student_id
        selected_student_id = selected_student_tuple[0]
        items = db.get_student_events(selected_student_id)
        event_item = map(lambda x: x[2:], items)
        event_list_box.show_items(event_item)
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
    if grade_students:
        student_list_box.show_items(grade_students)
        event_list_box.show_items([])

def export_grade_students():
    grade_student = get_grade_students()
    if grade_student:
        with open('students.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["First Name", "Last Name", "Grade", "Points"])
            for row in grade_student:
                writer.writerow(row[1:])

window = tkinter.Tk()
window.title("Data Entry Form")
center = tkinter.Frame(window)
center.pack(padx=20,pady=20,anchor=CENTER)
frame = tkinter.Frame(center)
frame.pack(padx=20, pady = 20, side = LEFT, fill = BOTH)

#Leaderboard
leaderboard_frame = tkinter.Frame(center)
leaderboard_frame.pack(padx=20, pady = 20, side=RIGHT, fill = BOTH)

student_list_box = Sortable_list_box(ttk, leaderboard_frame, 
    ["ID", "First Name", "Last Name", "Grade", "Total Points"])
student_list_box.tree.bind('<ButtonRelease-1>', student_selected)
event_list_box = Sortable_list_box(ttk, leaderboard_frame, 
    ["Date", "Event", "Involvement", "Points"])

#New Register or Search Student
user_registration_frame = tkinter.LabelFrame(frame,width=10, height=200, text = " Student Registration ")
user_registration_frame.grid(row= 0, column=0, sticky="news", padx=20, pady=5)


new_student = tkinter.Button(user_registration_frame, text="Add New Student", command=add_student)
new_student.grid(row=0, column=0, sticky="news", padx=10, pady=10)

# Saving User Info
user_info_frame =tkinter.LabelFrame(frame, text=" Student Information ")
user_info_frame.grid(row= 1, column=0, sticky = "news", padx=20, pady=5)

first_name_label = tkinter.Label(user_info_frame, text="First Name")
first_name_label.grid(row=0, column=0)
last_name_label = tkinter.Label(user_info_frame, text="Last Name")
last_name_label.grid(row=0, column=1)

first_name_entry = tkinter.Entry(user_info_frame)
last_name_entry = tkinter.Entry(user_info_frame)
first_name_entry.grid(row=1, column=0,padx=20,pady=10)
last_name_entry.grid(row=1, column=1,padx=20,pady=10)

# grades
grade_frame = tkinter.LabelFrame(frame, text = " Select Grade: ")
grade_frame.grid(row=2, column=0, sticky="news", padx=20, pady=5)
grade_label = tkinter.Label(grade_frame, text = "Select Grade: ")
grade_dict = {"grade 9": 9, "grade 10": 10, "grade 11": 11, "grade 12": 12}
grade_combobox = ttk.Combobox(grade_frame, state="readonly", values=list(grade_dict.keys()), width = 17)
grade_label.grid(row=0, column=1,sticky="news",padx = 15)
grade_combobox.grid(row=1, column=1,padx=20, pady = 10)


#event logs
event_frame = tkinter.LabelFrame(frame, text = "Event Log: ")
event_frame.grid(row=3, column = 0,sticky = "news",padx = 20, pady = 5)

event_values = ["Basketball Game", "Baseball Game", "Volleyball Game", "Soccer Game", "Talent Show", "Christmas Concert", "Spring Concert", "Mass", "Prayer"]
events_label = tkinter.Label(event_frame, text="Event: ")
events_combobox = ttk.Combobox(event_frame, state="readonly", values=event_values, width = 17)
events_label.grid(row=0, column=0 )
events_combobox.grid(row=1, column=0,padx=10)

title_label = tkinter.Label(event_frame, text="Participation")
title_combobox = ttk.Combobox(event_frame, state="readonly", values=["Participant", "Attendant"], width = 17)
title_label.grid(row=0, column=1,sticky="news",padx = 15)
title_combobox.grid(row=1, column=1,padx=20, pady = 10)

date_label=tkinter.Label(event_frame,text='Date: ')
date_label.grid(row=3,column=0)
cal=DateEntry(event_frame,selectmode='day',width=17)
cal.grid(row=4,column=0,padx=20,pady=10)
cal.set_date(date.today()) # todays date 

points_label = tkinter.Label(event_frame, text="Points: ")
points_spinbox = tkinter.Spinbox(event_frame, from_=1, to=1000,width=15)
points_label.grid(row=3, column=1)
points_spinbox.grid(row=4, column=1, padx=10, pady=10)

# Button
button = tkinter.Button(frame, text="Add Event", command=add_event)
button.grid(row=5, column=0, sticky="news", padx=20, pady=10)
view_all_button = tkinter.Button(frame, text="show all students", command=view_all_students)
view_all_button.grid(row=6, column=0, sticky="news", padx=20, pady=10)

search_button = tkinter.Button(frame, text = "Search by name", command=search_by_name)
search_button.grid(row = 7, column = 0)
search_input = tkinter.Entry(frame)
search_input.grid(row = 7, column = 1)

grade_filter_label = tkinter.Label(frame, text="Grade: ")
grade_filter_combobox = ttk.Combobox(frame, state="readonly", values=list(grade_dict.keys()), width = 17)
grade_filter_label.grid(row=8, column=0,sticky="news",padx = 15)
grade_filter_combobox.grid(row=8, column=1,padx=20, pady = 10)
grade_filter_combobox.current(0)

view_grade_button = tkinter.Button(frame, text = "View students in grade", command=view_grade_students)
view_grade_button.grid(row = 9, column = 0)

export_grade_button = tkinter.Button(frame, text = "Export students in grade", command=export_grade_students)
export_grade_button.grid(row = 9, column = 1)

window.mainloop()

