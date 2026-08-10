from datetime import date, timedelta

from LibraryManagementSystem.book import Book
from LibraryManagementSystem.librarian import Librarian
from LibraryManagementSystem.student import Student
from LibraryManagementSystem.user import User


def createBook():
    return Book(
        "B101",
        "Python Basics",
        "Programming",
        "John Smith",
        "ABC Publications",
        "R10"
    )


def createStudent():
    return Student(
        "U102",
        "S101",
        "Vishwa",
        "vishwa",
        "1234"
    )


def test_user_login_and_logout():
    user = User("U101", "Ravi", "ravi", "1234")

    assert user.login("ravi", "1234") is True
    assert user.loggedIn is True

    user.logout()
    assert user.loggedIn is False


def test_librarian_can_add_book_and_student():
    librarian = Librarian(
        "U100",
        "L101",
        "Admin",
        "admin",
        "admin123"
    )
    book = createBook()
    student = createStudent()

    assert librarian.addBook(book) is True
    assert librarian.registerStudent(student) is True
    assert librarian.manageBooks() == [book]
    assert librarian.manageStudents() == [student]


def test_student_can_search_and_borrow_book():
    student = createStudent()
    book = createBook()

    result = student.searchBook([book], "python")
    record = student.borrowBook(book, 1)

    assert result == [book]
    assert record is not None
    assert book.status == "Borrowed"
    assert book in student.borrowedBooks


def test_student_can_return_book():
    student = createStudent()
    book = createBook()
    student.borrowBook(book, 1)

    fine = student.returnBook(book)

    assert fine == 0
    assert book.status == "Available"
    assert book not in student.borrowedBooks


def test_fine_is_calculated_for_late_return():
    student = createStudent()
    book = createBook()
    record = student.borrowBook(book, 1)
    record.dueDate = date.today() - timedelta(days=3)

    fine = student.returnBook(book)

    assert fine == 30
    assert record.status == "Returned"
