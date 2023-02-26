import sqlite3
from student import Student
from studentEvent import Student_event

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("student_events.db")
        self.cur=self.conn.cursor()
        try:
            student_table = '''CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                first_name TEXT NOT NULL, 
                last_name TEXT NOT NULL, 
                grade INT NOT NULL
            );'''
            self.conn.execute(student_table)
            events_table = '''CREATE TABLE IF NOT EXISTS student_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                student_id INTEGER NOT NULL,
                event_date TEXT NOT NULL, 
                event_name TEXT NOT NULL, 
                involvement TEXT NOT NULL, 
                points INT NOT NULL DEFAULT 1,
                FOREIGN KEY (student_id) REFERENCES students (id)
            );'''
            self.conn.execute(events_table)
        except Exception as error:
            print ("database create error:", TabError)

    def insert_student(self, first_name, last_name, grade):
        self.cur.execute("INSERT INTO students(first_name, last_name, grade) VALUES (?,?,?)",\
                         (first_name, last_name, grade))
        self.conn.commit()
        student_id = self.cur.lastrowid
        print ("new id ", student_id)
        return student_id
    
    def insert_event(self, student_id, event_date, event_name, involvement, points):
        self.cur.execute("INSERT INTO student_events(student_id, event_date, event_name, involvement, points) VALUES (?,?,?,?,?)", \
                         (student_id, event_date, event_name, involvement, points))
        self.conn.commit()

    def update_event(self, id, student_id, event_date, event_name, involvement, points):
        self.cur.execute("UPDATE student_events SET student_id=?,event_date=?,event_name=?,involvement=?,points=? WHERE id=?", \
                         (student_id, event_date, event_name, involvement, points, id))
        self.conn.commit()

    def get_all_students(self, grade = 0):
        query = '''SELECT s.id, s.first_name, s.last_name, s.grade, 
            (SELECT SUM(e.points)
                FROM student_events e
                WHERE s.id = e.student_id
            ) as points
            FROM students s'''
        if grade == 0:
            query += ";"
        else:
            query += " where grade == {};".format(grade)
        self.cur.execute(query)
        return self.cur.fetchall()
    
    def get_student_events(self, student_id):
        query = '''SELECT id, student_id, event_date, event_name, involvement, points
            FROM student_events where student_id = {};'''.format(student_id)
        self.cur.execute(query)
        return self.cur.fetchall()

    def search_by_name(self, name):
        query = '''SELECT s.id, s.first_name, s.last_name, s.grade, 
            (SELECT SUM(e.points)
                FROM student_events e
                WHERE s.id = e.student_id
            ) as points
            FROM students s
            where s.first_name like '%{}%' OR s.last_name like '%{}%';'''.format(name, name)
        self.cur.execute(query)
        return self.cur.fetchall()

    def __del__(self):
        self.conn.close()

