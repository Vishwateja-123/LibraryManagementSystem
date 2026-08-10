from datetime import date, timedelta


class User:
    def __init__(self, userId, name, username, password):
        self._userId = userId
        self._name = name
        self._username = username
        self._password = password
        self._loggedIn = False

    def login(self, username, password):
        if username == self._username and password == self._password:
            self._loggedIn = True
            print(f"{self._name} logged in successfully.")
            return True

        print("Invalid username or password.")
        return False

    def logout(self):
        self._loggedIn = False
        print(f"{self._name} logged out.")


class Book:
    def __init__(
        self,
        bookId,
        title,
        category,
        author,
        publisher,
        rackNumber,
    ):
        self._bookId = bookId
        self._title = title
        self._category = category
        self._author = author
        self._publisher = publisher
        self._status = "Available"
        self._rackNumber = rackNumber
        self._borrowedBy = None
        self._reservedBy = None

    def checkAvailability(self):
        return self._status == "Available"

    def __str__(self):
        return f"{self._bookId} - {self._title} ({self._status})"


class BorrowRecordHistory:
    FINE_PER_DAY = 10.0

    def __init__(self, historyId, student, book):
        self._historyId = historyId
        self._student = student
        self._book = book
        self._issueDate = date.today()
        self._dueDate = self._issueDate + timedelta(days=14)
        self._returnDate = None
        self._fineAmount = 0.0
        self._status = "Borrowed"

    def viewHistory(self):
        return {
            "historyId": self._historyId,
            "student": self._student._name,
            "book": self._book._title,
            "issueDate": self._issueDate,
            "dueDate": self._dueDate,
            "returnDate": self._returnDate,
            "fineAmount": self._fineAmount,
            "status": self._status,
        }

    def calculateFine(self, returnedOn=None):
        returnedOn = returnedOn or date.today()
        lateDays = (returnedOn - self._dueDate).days
        self._fineAmount = max(0, lateDays) * self.FINE_PER_DAY
        return self._fineAmount

    def closeRecord(self, returnedOn=None):
        if self._status == "Returned":
            return self._fineAmount

        self._returnDate = returnedOn or date.today()
        self.calculateFine(self._returnDate)
        self._status = "Returned"
        return self._fineAmount


class Student(User):
    def __init__(self, userId, studentId, name, username, password):
        super().__init__(userId, name, username, password)
        self._studentId = studentId
        self._borrowedBooks = []
        self._reservedBooks = []
        self._history = []

    def searchBook(self, books, title):
        title = title.lower()
        return [book for book in books if title in book._title.lower()]

    def borrowBook(self, book, historyId):
        if not book.checkAvailability():
            print(f"'{book._title}' is not available.")
            return None

        if book._reservedBy not in (None, self):
            print(f"'{book._title}' is reserved by another student.")
            return None

        book._status = "Borrowed"
        book._borrowedBy = self
        book._reservedBy = None
        self._borrowedBooks.append(book)

        if book in self._reservedBooks:
            self._reservedBooks.remove(book)

        record = BorrowRecordHistory(historyId, self, book)
        self._history.append(record)
        print(f"'{book._title}' borrowed until {record._dueDate}.")
        return record

    def returnBook(self, book, returnedOn=None):
        if book not in self._borrowedBooks:
            print("This book was not borrowed by this student.")
            return None

        record = next(
            (
                item
                for item in reversed(self._history)
                if item._book == book and item._status == "Borrowed"
            ),
            None,
        )

        fine = record.closeRecord(returnedOn) if record else 0.0
        self._borrowedBooks.remove(book)
        book._borrowedBy = None
        book._status = "Available"
        print(f"'{book._title}' returned. Fine: Rs.{fine:.2f}")
        return fine

    def reserveBook(self, book):
        if book.checkAvailability():
            print("The book is available, so you can borrow it directly.")
            return False

        if book._reservedBy is not None:
            print("The book is already reserved.")
            return False

        book._reservedBy = self
        self._reservedBooks.append(book)
        print(f"'{book._title}' reserved successfully.")
        return True

    def renewBook(self, book):
        record = next(
            (
                item
                for item in reversed(self._history)
                if item._book == book and item._status == "Borrowed"
            ),
            None,
        )

        if record is None:
            print("No active borrowing record was found.")
            return False

        if book._reservedBy not in (None, self):
            print("The book cannot be renewed because another student reserved it.")
            return False

        record._dueDate += timedelta(days=14)
        print(f"Book renewed. New due date: {record._dueDate}")
        return True


class Librarian(User):
    def __init__(self, userId, librarianId, name, username, password):
        super().__init__(userId, name, username, password)
        self._librarianId = librarianId
        self._books = []
        self._students = []
        self._records = []

    def manageBooks(self):
        return self._books

    def registerStudent(self, student):
        if student not in self._students:
            self._students.append(student)
            print(f"Student {student._name} registered successfully.")
            return True
        return False

    def manageStudents(self):
        return self._students

    def sendDueReminder(self):
        reminders = []
        today = date.today()

        for record in self._records:
            if record._status == "Borrowed" and record._dueDate <= today:
                message = (
                    f"Reminder for {record._student._name}: "
                    f"'{record._book._title}' is due on {record._dueDate}."
                )
                reminders.append(message)

        return reminders

    def addBook(self, book):
        if any(item._bookId == book._bookId for item in self._books):
            print("A book with this ID already exists.")
            return False

        self._books.append(book)
        print(f"'{book._title}' added successfully.")
        return True

    def updateBook(self, bookId, **changes):
        book = self._findBook(bookId)
        if book is None:
            print("Book not found.")
            return False

        allowedFields = {
            "title": "_title",
            "category": "_category",
            "author": "_author",
            "publisher": "_publisher",
            "status": "_status",
            "rackNumber": "_rackNumber",
        }

        for field, value in changes.items():
            if field in allowedFields:
                setattr(book, allowedFields[field], value)

        print("Book updated successfully.")
        return True

    def removeBook(self, bookId):
        book = self._findBook(bookId)
        if book is None:
            print("Book not found.")
            return False

        if not book.checkAvailability():
            print("A borrowed book cannot be removed.")
            return False

        self._books.remove(book)
        print(f"'{book._title}' removed successfully.")
        return True

    def addRecord(self, record):
        if record is not None and record not in self._records:
            self._records.append(record)

    def _findBook(self, bookId):
        return next(
            (book for book in self._books if book._bookId == bookId),
            None,
        )


if __name__ == "__main__":
    librarian = Librarian(1, 101, "Ravi", "ravi", "admin123")
    student = Student(2, 201, "Vishwa", "vishwa", "student123")

    book1 = Book(
        1001,
        "Python Programming",
        "Programming",
        "John Smith",
        "ABC Publications",
        "R-10",
    )

    librarian.login("ravi", "admin123")
    librarian.registerStudent(student)
    librarian.addBook(book1)

    results = student.searchBook(librarian.manageBooks(), "Python")
    print("Search results:", *results)

    record = student.borrowBook(book1, 5001)
    librarian.addRecord(record)
    student.renewBook(book1)
    student.returnBook(book1)

    if record:
        print("Borrow history:", record.viewHistory())

    librarian.logout()
