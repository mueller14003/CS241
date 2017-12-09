class Book:
    def __init__(self):
        self.title = "unknown"
        self.author = "unknown"
        self.publication_year = 2000

    def prompt_book_info(self):
        self.title = input("Title: ")
        self.author = input("Author: ")
        self.publication_year = int(input("Publication Year: "))

    def display_book_info(self):
        print("{} ({}) by {}".format(self.title, self.publication_year, self.author))


class TextBook(Book):
    def __init__(self):
        Book.__init__(self)
        self.subject = "unknown"

    def prompt_book_info(self):
        Book.prompt_book_info(self)

    def display_book_info(self):
        Book.display_book_info(self)

    def prompt_subject(self):
        self.subject = input("Subject: ")

    def display_subject(self):
        print("Subject: {}".format(self.subject))


class PictureBook(Book):
    def __init__(self):
        Book.__init__(self)
        self.illustrator = "unknown"

    def prompt_book_info(self):
        Book.prompt_book_info(self)

    def display_book_info(self):
        Book.display_book_info(self)

    def prompt_illustrator(self):
        self.illustrator = input("Illustrator: ")

    def display_illustrator(self):
        print("Illustrated by {}".format(self.illustrator))


def main():
    book = Book()

    book.prompt_book_info()
    book.display_book_info()

    text_book = TextBook()

    text_book.prompt_book_info()
    text_book.prompt_subject()
    text_book.display_book_info()
    text_book.display_subject()

    picture_book = PictureBook()
    picture_book.prompt_book_info()
    picture_book.prompt_illustrator()
    picture_book.display_book_info()
    picture_book.display_illustrator()


if __name__ == "__main__":
    main()
