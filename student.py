import studentEvent as event
class Student:
    def __init__(self, firstName, lastName, grade, id, points):
        self.firstName = firstName
        self.lastName = lastName
        self.grade = grade
        self.id = id
        self.totalPoints = points
        self.rank = 0