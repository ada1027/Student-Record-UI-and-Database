import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from tkcalendar import DateEntry 
from datetime import date
from database import Database
from sortableListBox import SortableListBox
import csv

db = Database()
selectedStudentId = 0

def addStudent(): # addStudent button event handler
    global selectedStudentId
    if selectedStudentId != 0:
        selectedStudentId = 0
        setText(first_name_entry, "", True)
        setText(last_name_entry, "", True)
        grade_combobox.config(state=NORMAL)
        grade_combobox.set("")
    else:
        firstname = first_name_entry.get()
        lastname = last_name_entry.get()
        if (firstname and lastname):
            gradeValue = grade_combobox.get()
            if gradeValue:
                grade = grade_dict[gradeValue] 
                selectedStudentId = db.insertStudent(firstname, lastname, grade)
                if selectedStudentId > 0:
                    first_name_entry.configure(state=DISABLED)
                    last_name_entry.config(state=DISABLED)
                    grade_combobox.config(state=DISABLED)
            else:
                messagebox.showwarning(title="Error", message="Please select a grade")
        else:
            messagebox.showwarning(title="Error", message="Not all fields filled.")

def addEvent():
    global selectedStudentId
    if selectedStudentId == 0:
        addStudent()
    if selectedStudentId > 0:
        eventdate = cal.get_date()
        eventname = events_combobox.get()
        involvement = title_combobox.get()
        points = points_spinbox.get()
        allFields = eventdate and eventname and involvement and points
        if allFields:
            db.insertEvent(selectedStudentId, eventdate, eventname, involvement, points)
        else:
            messagebox.showwarning(title="Error", message="Not all fields filled.")
    else:
        messagebox.showwarning(title="Error", message="Student info missing")

def resetEventFields():
    events_combobox.set("")
    title_combobox.set("")

def studentSelected(event):
    global selectedStudentTuple
    selectedStudentTuple = studentListBox.tree.item(studentListBox.tree.focus())["values"]
    if selectedStudentTuple:
        # print(selectedStudentTuple) # [2, 'firstName', 'lastName', 10, 100]
        global selectedStudentId
        selectedStudentId = selectedStudentTuple[0]
        items = db.getStudentEvents(selectedStudentId)
        eventItem = map(lambda x: x[2:], items)
        eventListBox.showItems(eventItem)
        setText(first_name_entry, selectedStudentTuple[1], False)
        setText(last_name_entry, selectedStudentTuple[2], False)
        grade_combobox.current(selectedStudentTuple[3] - 9)
        grade_combobox.config(state=DISABLED)
        resetEventFields()

def setText(textField, value, enabled):
    textField.config(state=NORMAL) # eanble textfield first so that it's editable
    textField.delete(0, END)
    if value:
        textField.insert(0, value)
    if enabled:
        textField.config(state=NORMAL)
    else:
        textField.config(state=DISABLED)

def searchByName():
    keyWord = searchInput.get()
    if (keyWord):
        items = db.searchByName(keyWord)
        studentListBox.showItems(items) 
        eventListBox.showItems([])  
    else:
        messagebox.showwarning(title="Error", message="please type a name to search.")

def viewAllStudents():
    items = db.getAllStudents()
    studentListBox.showItems(items)
    eventListBox.showItems([])
    global selectedStudentId
    selectedStudentId = 0

def getGradeStudents():
    gradeValue = grade_filter_combobox.get()
    if gradeValue:
        grade = grade_dict[gradeValue]
        items = db.getAllStudents(grade)
        return items
    else:
        messagebox.showwarning(title="Error", message="please select a grade.")

def viewGradeStudents():
    gradeStudents = getGradeStudents()
    if gradeStudents:
        studentListBox.showItems(gradeStudents)
        eventListBox.showItems([])

def exportGradeStudents():
    gradeStudents = getGradeStudents()
    if gradeStudents:
        with open('students.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["First Name", "Last Name", "Grade", "Points"])
            for row in gradeStudents:
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

studentListBox = SortableListBox(ttk, leaderboard_frame, 
    ["ID", "First Name", "Last Name", "Grade", "Total Points"])
studentListBox.tree.bind('<ButtonRelease-1>', studentSelected)
eventListBox = SortableListBox(ttk, leaderboard_frame, 
    ["Date", "Event", "Involvement", "Points"])

#New Register or Search Student
user_registration_frame = tkinter.LabelFrame(frame,width=10, height=200, text = " Student Registration ")
user_registration_frame.grid(row= 0, column=0, sticky="news", padx=20, pady=5)


newStudent = tkinter.Button(user_registration_frame, text="Add New Student", command=addStudent)
newStudent.grid(row=0, column=0, sticky="news", padx=10, pady=10)

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

# registered_label = tkinter.Label(courses_frame, text="Student Registration Status")
# reg_status_var = tkinter.StringVar(value="Not Registered")
# registered_check = tkinter.Checkbutton(courses_frame, text="Already Registered Student", variable=reg_status_var, onvalue="Registered", offvalue="Not registered")
# registered_label.grid(row=0, column=0)
# registered_check.grid(row=1, column=0)

# Button
button = tkinter.Button(frame, text="Add Event", command=addEvent)
button.grid(row=5, column=0, sticky="news", padx=20, pady=10)
viewAllButton = tkinter.Button(frame, text="show all students", command=viewAllStudents)
viewAllButton.grid(row=6, column=0, sticky="news", padx=20, pady=10)

searchButton = tkinter.Button(frame, text = "Search by name", command=searchByName)
searchButton.grid(row = 7, column = 0)
searchInput = tkinter.Entry(frame)
searchInput.grid(row = 7, column = 1)

grade_filter_label = tkinter.Label(frame, text="Grade: ")
grade_filter_combobox = ttk.Combobox(frame, state="readonly", values=list(grade_dict.keys()), width = 17)
grade_filter_label.grid(row=8, column=0,sticky="news",padx = 15)
grade_filter_combobox.grid(row=8, column=1,padx=20, pady = 10)
grade_filter_combobox.current(0)

viewGradeButton = tkinter.Button(frame, text = "View studends in grade", command=viewGradeStudents)
viewGradeButton.grid(row = 9, column = 0)

exportGradeButton = tkinter.Button(frame, text = "Export studends in grade", command=exportGradeStudents)
exportGradeButton.grid(row = 9, column = 1)

window.mainloop()

