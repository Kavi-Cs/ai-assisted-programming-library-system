class Book:
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.is_available = True

    def __str__(self):
        status = "Available" if self.is_available else "Borrowed"
        return f"{self.book_id} | {self.title} | {self.author} | {status}"


class Member:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = []

    def __str__(self):
        borrowed = ", ".join(self.borrowed_books) if self.borrowed_books else "None"
        return f"{self.member_id} | {self.name} | Borrowed: {borrowed}"


class Library:
    def __init__(self):
        self.books = {}
        self.members = {}

    def add_book(self, book_id, title, author):
        if book_id in self.books:
            return "Book ID already exists."
        self.books[book_id] = Book(book_id, title, author)
        return "Book added successfully."

    def add_member(self, member_id, name):
        if member_id in self.members:
            return "Member ID already exists."
        self.members[member_id] = Member(member_id, name)
        return "Member added successfully."

    def borrow_book(self, member_id, book_id):
        if member_id not in self.members:
            return "Member not found."
        if book_id not in self.books:
            return "Book not found."

        book = self.books[book_id]
        member = self.members[member_id]

        if not book.is_available:
            return "Book is already borrowed."

        book.is_available = False
        member.borrowed_books.append(book_id)
        return "Book borrowed successfully."

    def return_book(self, member_id, book_id):
        if member_id not in self.members:
            return "Member not found."
        if book_id not in self.books:
            return "Book not found."

        book = self.books[book_id]
        member = self.members[member_id]

        if book_id not in member.borrowed_books:
            return "This member did not borrow the selected book."

        book.is_available = True
        member.borrowed_books.remove(book_id)
        return "Book returned successfully."

    def list_books(self):
        if not self.books:
            return "No books available."
        return "\n".join(str(book) for book in self.books.values())

    def list_members(self):
        if not self.members:
            return "No members registered."
        return "\n".join(str(member) for member in self.members.values())


def seed_library(library):
    library.add_book("B001", "Clean Code", "Robert C. Martin")
    library.add_book("B002", "Python Crash Course", "Eric Matthes")
    library.add_member("M001", "Nimal Perera")
    library.add_member("M002", "Asha Silva")


def main():
    library = Library()
    seed_library(library)

    while True:
        print("\nLibrary Management System - Version A")
        print("1. Add book")
        print("2. Add member")
        print("3. Borrow book")
        print("4. Return book")
        print("5. List books")
        print("6. List members")
        print("0. Exit")

        choice = input("Select option: ").strip()

        if choice == "1":
            book_id = input("Book ID: ").strip()
            title = input("Title: ").strip()
            author = input("Author: ").strip()
            print(library.add_book(book_id, title, author))
        elif choice == "2":
            member_id = input("Member ID: ").strip()
            name = input("Name: ").strip()
            print(library.add_member(member_id, name))
        elif choice == "3":
            member_id = input("Member ID: ").strip()
            book_id = input("Book ID: ").strip()
            print(library.borrow_book(member_id, book_id))
        elif choice == "4":
            member_id = input("Member ID: ").strip()
            book_id = input("Book ID: ").strip()
            print(library.return_book(member_id, book_id))
        elif choice == "5":
            print(library.list_books())
        elif choice == "6":
            print(library.list_members())
        elif choice == "0":
            print("Exiting system.")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
