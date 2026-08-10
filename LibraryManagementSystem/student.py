from datetime import timedelta

from .borrow_record_history import BorrowRecordHistory
from .user import User


class Student(User):
    def __init__(
        self,
        userId,
        studentId,
        name,
        username,
        password
    ):
        super().__init__(userId, name, username, password)
        self.studentId = studentId
        self.borrowedBooks = []
        self.reservedBooks = []
        self.history = []

    def searchBook(self, books, title):
        result = []

        for book in books:
            if title.lower() in book.title.lower():
                result.append(book)

        return result

    def borrowBook(self, book, historyId):
        if not book.checkAvailability():
            return None

        if book.reservedBy is not None and book.reservedBy != self:
            return None

        book.status = "Borrowed"
        book.borrowedBy = self
        book.reservedBy = None
        self.borrowedBooks.append(book)

        if book in self.reservedBooks:
            self.reservedBooks.remove(book)

        record = BorrowRecordHistory(historyId, self, book)
        self.history.append(record)
        return record

    def returnBook(self, book, returnDate=None):
        if book not in self.borrowedBooks:
            return None

        record = None

        for currentRecord in self.history:
            if (
                currentRecord.book == book
                and currentRecord.status == "Borrowed"
            ):
                record = currentRecord

        if record is None:
            return None

        fine = record.closeRecord(returnDate)
        self.borrowedBooks.remove(book)
        book.status = "Available"
        book.borrowedBy = None
        return fine

    def reserveBook(self, book):
        if book.checkAvailability():
            return False

        if book.reservedBy is not None:
            return False

        book.reservedBy = self
        self.reservedBooks.append(book)
        return True

    def renewBook(self, book):
        record = None

        for currentRecord in self.history:
            if (
                currentRecord.book == book
                and currentRecord.status == "Borrowed"
            ):
                record = currentRecord

        if record is None:
            return False

        if book.reservedBy is not None and book.reservedBy != self:
            return False

        record.dueDate = record.dueDate + timedelta(days=14)
        return True
