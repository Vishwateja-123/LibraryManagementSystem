from datetime import date, timedelta


class BorrowRecordHistory:
    finePerDay = 10

    def __init__(self, historyId, student, book):
        self.historyId = historyId
        self.student = student
        self.book = book
        self.issueDate = date.today()
        self.dueDate = self.issueDate + timedelta(days=14)
        self.returnDate = None
        self.fineAmount = 0
        self.status = "Borrowed"

    def viewHistory(self):
        return {
            "historyId": self.historyId,
            "student": self.student.name,
            "book": self.book.title,
            "issueDate": self.issueDate,
            "dueDate": self.dueDate,
            "returnDate": self.returnDate,
            "fineAmount": self.fineAmount,
            "status": self.status,
        }

    def calculateFine(self, returnDate=None):
        if returnDate is None:
            returnDate = date.today()

        lateDays = (returnDate - self.dueDate).days

        if lateDays > 0:
            self.fineAmount = lateDays * self.finePerDay
        else:
            self.fineAmount = 0

        return self.fineAmount

    def closeRecord(self, returnDate=None):
        if returnDate is None:
            returnDate = date.today()

        self.returnDate = returnDate
        self.calculateFine(returnDate)
        self.status = "Returned"
        return self.fineAmount
