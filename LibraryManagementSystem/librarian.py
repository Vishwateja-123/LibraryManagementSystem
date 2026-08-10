from datetime import date

from .user import User


class Librarian(User):
    def __init__(
        self,
        userId,
        librarianId,
        name,
        username,
        password
    ):
        super().__init__(userId, name, username, password)
        self.librarianId = librarianId
        self.books = []
        self.students = []
        self.history = []

    def manageBooks(self):
        return self.books

    def registerStudent(self, student):
        if self.getStudentById(student.studentId) is not None:
            return False

        self.students.append(student)
        return True

    def manageStudents(self):
        return self.students

    def sendDueReminder(self):
        reminders = []

        for record in self.history:
            if record.status == "Borrowed" and record.dueDate <= date.today():
                message = (
                    "Reminder for "
                    + record.student.name
                    + ": "
                    + record.book.title
                    + " is due on "
                    + str(record.dueDate)
                )
                reminders.append(message)

        return reminders

    def addBook(self, book):
        if self.getBookById(book.bookId) is not None:
            return False

        self.books.append(book)
        return True

    def updateBook(
        self,
        bookId,
        title=None,
        category=None,
        author=None,
        publisher=None,
        rackNumber=None
    ):
        book = self.getBookById(bookId)

        if book is None:
            return False

        if title is not None:
            book.title = title
        if category is not None:
            book.category = category
        if author is not None:
            book.author = author
        if publisher is not None:
            book.publisher = publisher
        if rackNumber is not None:
            book.rackNumber = rackNumber

        return True

    def removeBook(self, bookId):
        book = self.getBookById(bookId)

        if book is None or not book.checkAvailability():
            return False

        self.books.remove(book)
        return True

    def addHistory(self, record):
        if record is not None:
            self.history.append(record)

    def getBookById(self, bookId):
        for book in self.books:
            if book.bookId == bookId:
                return book

        return None

    def getStudentById(self, studentId):
        for student in self.students:
            if student.studentId == studentId:
                return student

        return None
