# Library Management System

A console-based Library Management System implemented in Python using object-oriented programming. The classes and relationships are based on the UML class diagram prepared for this project.

## Classes

- `User` – common login and logout functionality
- `Librarian` – manages books, students, borrowing records, and due reminders
- `Student` – searches, borrows, returns, reserves, and renews books
- `Book` – stores book information and availability
- `BorrowRecordHistory` – tracks issue dates, due dates, returns, status, and fines

## Features

- User login and logout
- Student registration
- Add, update, and remove books
- Search books by title
- Borrow and return books
- Reserve unavailable books
- Renew borrowed books
- Track borrowing history
- Calculate overdue fines automatically
- Send due-date reminders

## Requirements

- Python 3.9 or later
- No external packages are required

## Run the project

Clone the repository:

```bash
git clone https://github.com/Vishwateja-123/LibraryManagementSystem.git
cd LibraryManagementSystem
```

Run the program:

```bash
python3 library_management_system.py
```

## Fine policy

- The normal borrowing period is 14 days.
- Renewal extends the due date by another 14 days.
- The overdue fine is Rs.10 per day.

## Author

Vishwateja Paidipelly
