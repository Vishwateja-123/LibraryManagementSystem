class Book:
    def __init__(
        self,
        bookId,
        title,
        category,
        author,
        publisher,
        rackNumber
    ):
        self.bookId = bookId
        self.title = title
        self.category = category
        self.author = author
        self.publisher = publisher
        self.status = "Available"
        self.rackNumber = rackNumber
        self.borrowedBy = None
        self.reservedBy = None

    def checkAvailability(self):
        return self.status == "Available"

    def __str__(self):
        return (
            str(self.bookId)
            + " - "
            + self.title
            + " - "
            + self.status
        )
