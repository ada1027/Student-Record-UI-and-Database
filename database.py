import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("student_events.db") #connect to database
        self.cur=self.conn.cursor()
        try:
            student_table = '''CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                first_name TEXT NOT NULL, 
                last_name TEXT NOT NULL, 
                grade INT NOT NULL
            );''' #create a table for student info- Id, Name and Grade
            self.conn.execute(student_table) 
            events_table = '''CREATE TABLE IF NOT EXISTS student_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                student_id INTEGER NOT NULL,
                event_date TEXT NOT NULL, 
                quarter INT NOT NULL,
                event_name TEXT NOT NULL, 
                involvement TEXT NOT NULL, 
                points INT NOT NULL DEFAULT 1,
                FOREIGN KEY (student_id) REFERENCES students (id)
            );''' #create table for event logs, Id reference to student
            self.conn.execute(events_table) 
        # exception
        except Exception as error:
            print ("database create error:", TabError)

    # insert student into database
    def insert_student(self, first_name, last_name, grade):
        #insert student name and grade into student table
        self.cur.execute("INSERT INTO students(first_name, last_name, grade) VALUES (?,?,?)",\
                         (first_name, last_name, grade))
        self.conn.commit()
        #set student id
        student_id = self.cur.lastrowid
        return student_id
    
    #insert event info into database
    def insert_event(self, student_id, event_date, quarter, event_name, involvement, points):
        #insert student id, date, quarter, name of event, participation type, and points into event table
        self.cur.execute("INSERT INTO student_events(student_id, event_date, quarter, event_name, involvement, points) VALUES (?,?,?,?,?,?)", \
                         (student_id, event_date, quarter, event_name, involvement, points))
        self.conn.commit()

    # get all student info
    def get_all_students(self, grade = 0):
        # add points to student's total points
        query = '''SELECT s.id, s.first_name, s.last_name, s.grade, 
            (SELECT SUM(e.points)
                FROM student_events e
                WHERE s.id = e.student_id
            ) as total_points
            FROM students s'''
        #order students from most points to least
        if grade == 0:
            query += " ORDER BY total_points DESC;"
        else:
            query += f" where grade == {grade} ORDER BY total_points DESC;"
        self.cur.execute(query)
        return self.cur.fetchall()
    
    # get event logs of specific student
    def get_student_events(self, student_id):
        #search all events with specific student id
        query = '''SELECT id, student_id, event_date, quarter, event_name, involvement, points
            FROM student_events where student_id = {};'''.format(student_id)
        self.cur.execute(query)
        return self.cur.fetchall()

    # search a student's name to find their record
    def search_by_name(self, name):
        # search first and last names for user-inputed characters
        query = '''SELECT s.id, s.first_name, s.last_name, s.grade, 
            (SELECT SUM(e.points)
                FROM student_events e
                WHERE s.id = e.student_id
            ) as points
            FROM students s
            where s.first_name like '%{}%' OR s.last_name like '%{}%';'''.format(name, name)
        self.cur.execute(query)
        return self.cur.fetchall()

    #close
    def __del__(self):
        self.conn.close()

    
