# Library Management System

This project is a simple command-line Library Management System developed in
Python using object-oriented programming.

## Main classes

- User
- Librarian
- Student
- Book
- BorrowRecordHistory

## Functions

- User login and logout
- Add, update and remove books
- Register students
- Search and borrow books
- Return, reserve and renew books
- View borrowing history
- Calculate late-return fine

## Project structure

```text
LibraryManagementSystem/
    __init__.py
    __main__.py
    user.py
    librarian.py
    student.py
    book.py
    borrow_record_history.py
tests/
    test_LibraryManagementSystem.py
```

## Run the project

```bash
python -m LibraryManagementSystem
```

The application asks you to create a librarian account when it starts.

## Run the tests

```bash
pip install -r dev-requirements.txt
pytest
```
