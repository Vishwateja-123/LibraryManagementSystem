from .book import Book
from .librarian import Librarian
from .student import Student


def showBooks(books):
    if not books:
        print("No books found.")
        return

    print("\nBOOK DETAILS")

    for book in books:
        print("Book ID:", book.bookId)
        print("Title:", book.title)
        print("Author:", book.author)
        print("Status:", book.status)
        print("-------------------------")


def main():
    print("WELCOME TO LIBRARY MANAGEMENT SYSTEM")
    print("\nCREATE LIBRARIAN ACCOUNT")
    librarianName = input("Enter librarian name: ")
    librarianUsername = input("Create username: ")
    librarianPassword = input("Create password: ")

    librarian = Librarian(
        1,
        101,
        librarianName,
        librarianUsername,
        librarianPassword
    )

    librarian.login(librarianUsername, librarianPassword)
    print("Librarian account created successfully.")

    while True:
        print("\nLIBRARY MENU")
        print("1. Add Book")
        print("2. Register Student")
        print("3. View Books")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. View Borrow History")
        print("7. Exit")

        try:
            choice = int(input("Choose an option: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        match choice:
            case 1:
                bookId = input("Enter book ID: ")
                title = input("Enter title: ")
                category = input("Enter category: ")
                author = input("Enter author: ")
                publisher = input("Enter publisher: ")
                rackNumber = input("Enter rack number: ")

                book = Book(
                    bookId,
                    title,
                    category,
                    author,
                    publisher,
                    rackNumber
                )

                if librarian.addBook(book):
                    print("Book added successfully.")
                else:
                    print("Book ID already exists.")

            case 2:
                userId = input("Enter user ID: ")
                studentId = input("Enter student ID: ")
                name = input("Enter student name: ")
                studentUsername = input("Enter username: ")
                studentPassword = input("Enter password: ")

                student = Student(
                    userId,
                    studentId,
                    name,
                    studentUsername,
                    studentPassword
                )

                if librarian.registerStudent(student):
                    print("Student registered successfully.")
                else:
                    print("Student ID already exists.")

            case 3:
                showBooks(librarian.manageBooks())

            case 4:
                studentId = input("Enter student ID: ")
                bookId = input("Enter book ID: ")
                student = librarian.getStudentById(studentId)
                book = librarian.getBookById(bookId)

                if student is None or book is None:
                    print("Student or book not found.")
                    continue

                historyId = len(librarian.history) + 1
                record = student.borrowBook(book, historyId)

                if record is None:
                    print("Book is not available.")
                else:
                    librarian.addHistory(record)
                    print("Book borrowed successfully.")
                    print("Due date:", record.dueDate)

            case 5:
                studentId = input("Enter student ID: ")
                bookId = input("Enter book ID: ")
                student = librarian.getStudentById(studentId)
                book = librarian.getBookById(bookId)

                if student is None or book is None:
                    print("Student or book not found.")
                    continue

                fine = student.returnBook(book)

                if fine is None:
                    print("Borrow record not found.")
                else:
                    print("Book returned successfully.")
                    print("Fine amount: Rs.", fine)

            case 6:
                if not librarian.history:
                    print("No borrow history found.")
                    continue

                for record in librarian.history:
                    details = record.viewHistory()
                    print("\nHistory ID:", details["historyId"])
                    print("Student:", details["student"])
                    print("Book:", details["book"])
                    print("Issue date:", details["issueDate"])
                    print("Due date:", details["dueDate"])
                    print("Status:", details["status"])

            case 7:
                librarian.logout()
                print("Exiting the application.")
                break

            case _:
                print("Invalid choice.")


if __name__ == "__main__":
    main()
