import studentEvent as event
class Student:
    def __init__(self, first_name, last_name, grade, id, points):
        self.first_name = first_name
        self.last_name = last_name
        self.grade = grade
        self.id = id
        self.totalPoints = points
        self.rank = 0
