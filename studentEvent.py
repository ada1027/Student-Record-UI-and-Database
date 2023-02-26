class StudentEvent:
    def __init__(self, studentId, eventDate, eventName, involvement, points, id = 0):
        self.studentId = studentId
        self.eventDate = eventDate
        self.eventName = eventName
        self.involvement = involvement
        self.points = points
        self.id = id