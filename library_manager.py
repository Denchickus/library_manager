import json
from typing import List, Dict, Optional

DATA_FILE = "data.json"


class Book:
    def __init__(self, title: str, author: str, year: int):
        self.id = None  # ID будет генерироваться автоматически
        self.title = title
        self.author = author
        self.year = year
        self.status = "в наличии"

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }


class LibraryManager:
    def __init__(self, data_file: str = DATA_FILE):
        self.data_file = data_file
        self.books: List[Dict] = self.load_books()

    def load_books(self) -> List[Dict]:
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_books(self) -> None:
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int) -> None:
        new_book = Book(title, author, year)
        new_book.id = len(self.books) + 1
        self.books.append(new_book.to_dict())
        self.save_books()
        print(f"Книга '{title}' успешно добавлена!")

    def remove_book(self, book_id: int) -> None:
        book = self.find_book_by_id(book_id)
        if book:
            self.books.remove(book)
            self.save_books()
            print(f"Книга с ID {book_id} успешно удалена!")
        else:
            print(f"Книга с ID {book_id} не найдена.")

    def find_book_by_id(self, book_id: int) -> Optional[Dict]:
        return next((book for book in self.books if book["id"] == book_id), None)

    def search_books(self, query: str, field: str) -> List[Dict]:
        return [book for book in self.books if str(book[field]).lower() == query.lower()]

    def display_books(self) -> None:
        if not self.books:
            print("Библиотека пуста.")
            return
        print("\nСписок книг в библиотеке:")
        for book in self.books:
            print(
                f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}, Год: {book['year']}, Статус: {book['status']}"
            )

    def update_status(self, book_id: int, new_status: str) -> None:
        if new_status not in ["в наличии", "выдана"]:
            print("Некорректный статус. Используйте 'в наличии' или 'выдана'.")
            return

        book = self.find_book_by_id(book_id)
        if book:
            book["status"] = new_status
            self.save_books()
            print(f"Статус книги с ID {book_id} успешно обновлён на '{new_status}'.")
        else:
            print(f"Книга с ID {book_id} не найдена.")


def main():
    library = LibraryManager()
    while True:
        print(
            "\nДоступные команды:\n"
            "1. Добавить книгу\n"
            "2. Удалить книгу\n"
            "3. Найти книгу\n"
            "4. Показать все книги\n"
            "5. Изменить статус книги\n"
            "6. Выйти\n"
        )
        command = input("Введите номер команды: ").strip()
        if command == "1":
            title = input("Введите название книги: ").strip()
            author = input("Введите автора книги: ").strip()
            year = int(input("Введите год издания книги: ").strip())
            library.add_book(title, author, year)
        elif command == "2":
            book_id = int(input("Введите ID книги для удаления: ").strip())
            library.remove_book(book_id)
        elif command == "3":
            field = input("По какому полю искать? (title/author/year): ").strip()
            query = input(f"Введите значение для поиска по {field}: ").strip()
            results = library.search_books(query, field)
            if results:
                for book in results:
                    print(book)
            else:
                print("Книг по данному запросу не найдено.")
        elif command == "4":
            library.display_books()
        elif command == "5":
            book_id = int(input("Введите ID книги: ").strip())
            new_status = input("Введите новый статус (в наличии/выдана): ").strip()
            library.update_status(book_id, new_status)
        elif command == "6":
            print("Выход из программы. До свидания!")
            break
        else:
            print("Неверная команда. Попробуйте ещё раз.")


if __name__ == "__main__":
    main()