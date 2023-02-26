import sqlite3
from student import Student
from studentEvent import StudentEvent

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("studentEvents.db")
        self.cur=self.conn.cursor()
        try:
            studendTable = '''CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                firstname TEXT NOT NULL, 
                lastname TEXT NOT NULL, 
                grade INT NOT NULL
            );'''
            self.conn.execute(studendTable)
            eventsTable = '''CREATE TABLE IF NOT EXISTS student_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                studentid INTEGER NOT NULL,
                eventdate TEXT NOT NULL, 
                eventname TEXT NOT NULL, 
                involvement TEXT NOT NULL, 
                points INT NOT NULL DEFAULT 1,
                FOREIGN KEY (studentid) REFERENCES students (id)
            );'''
            self.conn.execute(eventsTable)
        except Exception as error:
            print ("database create error:", TabError)

    def insertStudent(self, firstName, lastName, grade):
        self.cur.execute("INSERT INTO students(firstname, lastname, grade) VALUES (?,?,?)",\
                         (firstName, lastName, grade))
        self.conn.commit()
        studentid = self.cur.lastrowid
        print ("new id ", studentid)
        return studentid
    
    def insertEvent(self, studentId, eventDate, eventName, involvement, points):
        self.cur.execute("INSERT INTO student_events(studentid, eventdate, eventname, involvement, points) VALUES (?,?,?,?,?)", \
                         (studentId, eventDate, eventName, involvement, points))
        self.conn.commit()

    def updateEvent(self, id, studentId, eventDate, eventName, involvement, points):
        self.cur.execute("UPDATE student_events SET studentid=?,eventdate=?,eventname=?,involvement=?,points=? WHERE id=?", \
                         (studentId, eventDate, eventName, involvement, points, id))
        self.conn.commit()

    def getAllStudents(self, grade = 0):
        query = '''SELECT s.id, s.firstname, s.lastname, s.grade, 
            (SELECT SUM(e.points)
                FROM student_events e
                WHERE s.id = e.studentId
            ) as points
            FROM students s'''
        if grade == 0:
            query += ";"
        else:
            query += " where grade == {};".format(grade)
        self.cur.execute(query)
        return self.cur.fetchall()
    
    def getStudentEvents(self, studentId):
        query = '''SELECT id, studentid, eventdate, eventname, involvement, points
            FROM student_events where studentid = {};'''.format(studentId)
        self.cur.execute(query)
        return self.cur.fetchall()

    def searchByName(self, name):
        query = '''SELECT s.id, s.firstname, s.lastname, s.grade, 
            (SELECT SUM(e.points)
                FROM student_events e
                WHERE s.id = e.studentId
            ) as points
            FROM students s
            where s.firstname like '%{}%' OR s.lastname like '%{}%';'''.format(name, name)
        self.cur.execute(query)
        return self.cur.fetchall()

    def __del__(self):
        self.conn.close()

