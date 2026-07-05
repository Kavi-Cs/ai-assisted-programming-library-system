from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List


DATA_FILE = Path(__file__).with_name("library_data.json")


class LibraryError(Exception):
    """Raised when a library operation cannot be completed."""


@dataclass
class Book:
    book_id: str
    title: str
    author: str
    is_available: bool = True

    def display(self) -> str:
        status = "Available" if self.is_available else "Borrowed"
        return f"{self.book_id:<6} {self.title:<28} {self.author:<22} {status}"


@dataclass
class Member:
    member_id: str
    name: str
    borrowed_books: List[str] = field(default_factory=list)

    def display(self) -> str:
        borrowed = ", ".join(self.borrowed_books) if self.borrowed_books else "None"
        return f"{self.member_id:<6} {self.name:<24} Borrowed: {borrowed}"


class LibraryService:
    def __init__(self, data_file: Path = DATA_FILE):
        self.data_file = data_file
        self.books: Dict[str, Book] = {}
        self.members: Dict[str, Member] = {}
        self.load()

    def add_book(self, book_id: str, title: str, author: str) -> None:
        book_id = self._required(book_id, "Book ID").upper()
        title = self._required(title, "Title")
        author = self._required(author, "Author")

        if book_id in self.books:
            raise LibraryError(f"Book ID {book_id} already exists.")

        self.books[book_id] = Book(book_id, title, author)
        self.save()

    def add_member(self, member_id: str, name: str) -> None:
        member_id = self._required(member_id, "Member ID").upper()
        name = self._required(name, "Member name")

        if member_id in self.members:
            raise LibraryError(f"Member ID {member_id} already exists.")

        self.members[member_id] = Member(member_id, name)
        self.save()

    def borrow_book(self, member_id: str, book_id: str) -> None:
        member = self._get_member(member_id)
        book = self._get_book(book_id)

        if not book.is_available:
            raise LibraryError(f"{book.title} is already borrowed.")
        if book.book_id in member.borrowed_books:
            raise LibraryError("The selected member already has this book.")

        book.is_available = False
        member.borrowed_books.append(book.book_id)
        self.save()

    def return_book(self, member_id: str, book_id: str) -> None:
        member = self._get_member(member_id)
        book = self._get_book(book_id)

        if book.book_id not in member.borrowed_books:
            raise LibraryError("This member did not borrow the selected book.")

        member.borrowed_books.remove(book.book_id)
        book.is_available = True
        self.save()

    def search_books(self, keyword: str) -> List[Book]:
        keyword = self._required(keyword, "Search keyword").lower()
        return [
            book
            for book in self.books.values()
            if keyword in book.title.lower()
            or keyword in book.author.lower()
            or keyword in book.book_id.lower()
        ]

    def list_books(self) -> List[Book]:
        return sorted(self.books.values(), key=lambda book: book.book_id)

    def list_members(self) -> List[Member]:
        return sorted(self.members.values(), key=lambda member: member.member_id)

    def save(self) -> None:
        payload = {
            "books": [asdict(book) for book in self.books.values()],
            "members": [asdict(member) for member in self.members.values()],
        }
        self.data_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def load(self) -> None:
        if not self.data_file.exists():
            self._seed_data()
            self.save()
            return

        payload = json.loads(self.data_file.read_text(encoding="utf-8"))
        self.books = {
            item["book_id"]: Book(**item)
            for item in payload.get("books", [])
        }
        self.members = {
            item["member_id"]: Member(**item)
            for item in payload.get("members", [])
        }

    def _seed_data(self) -> None:
        self.books = {
            "B001": Book("B001", "Clean Code", "Robert C. Martin"),
            "B002": Book("B002", "Python Crash Course", "Eric Matthes"),
            "B003": Book("B003", "Design Patterns", "Gamma et al."),
        }
        self.members = {
            "M001": Member("M001", "Nimal Perera"),
            "M002": Member("M002", "Asha Silva"),
        }

    def _get_book(self, book_id: str) -> Book:
        book_id = self._required(book_id, "Book ID").upper()
        if book_id not in self.books:
            raise LibraryError(f"Book ID {book_id} was not found.")
        return self.books[book_id]

    def _get_member(self, member_id: str) -> Member:
        member_id = self._required(member_id, "Member ID").upper()
        if member_id not in self.members:
            raise LibraryError(f"Member ID {member_id} was not found.")
        return self.members[member_id]

    @staticmethod
    def _required(value: str, field_name: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise LibraryError(f"{field_name} cannot be empty.")
        return cleaned


def print_books(books: List[Book]) -> None:
    if not books:
        print("No matching books found.")
        return
    print(f"{'ID':<6} {'Title':<28} {'Author':<22} Status")
    print("-" * 72)
    for book in books:
        print(book.display())


def print_members(members: List[Member]) -> None:
    if not members:
        print("No members registered.")
        return
    print(f"{'ID':<6} {'Name':<24} Borrowing Details")
    print("-" * 72)
    for member in members:
        print(member.display())


def prompt(message: str) -> str:
    return input(message).strip()


def main() -> None:
    service = LibraryService()
    actions = {
        "1": "Add book",
        "2": "Add member",
        "3": "Borrow book",
        "4": "Return book",
        "5": "Search books",
        "6": "List books",
        "7": "List members",
        "0": "Exit",
    }

    while True:
        print("\nLibrary Management System - Version B")
        for key, label in actions.items():
            print(f"{key}. {label}")

        choice = prompt("Select option: ")

        try:
            if choice == "1":
                service.add_book(prompt("Book ID: "), prompt("Title: "), prompt("Author: "))
                print("Book added and saved.")
            elif choice == "2":
                service.add_member(prompt("Member ID: "), prompt("Name: "))
                print("Member added and saved.")
            elif choice == "3":
                service.borrow_book(prompt("Member ID: "), prompt("Book ID: "))
                print("Book borrowed and saved.")
            elif choice == "4":
                service.return_book(prompt("Member ID: "), prompt("Book ID: "))
                print("Book returned and saved.")
            elif choice == "5":
                print_books(service.search_books(prompt("Keyword: ")))
            elif choice == "6":
                print_books(service.list_books())
            elif choice == "7":
                print_members(service.list_members())
            elif choice == "0":
                print("Exiting system.")
                break
            else:
                print("Invalid option. Please select a listed number.")
        except (LibraryError, json.JSONDecodeError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
