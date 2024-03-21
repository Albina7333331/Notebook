import csv
import os
from datetime import datetime

NOTES_FILE = "notes.csv"
FIELDNAMES = ["id", "title", "message", "created_at", "updated_at"]


class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1

    def get_value(self):
        return self.value


class Note:
    id_counter = Counter()

    def __init__(self, title, message):
        self.id = self.id_counter.get_value()
        self.title = title
        self.message = message
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.id_counter.increment()

    def update(self, title, message):
        self.title = title
        self.message = message
        self.updated_at = datetime.now().isoformat()


def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []
    with open(NOTES_FILE, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def save_notes(notes):
    with open(NOTES_FILE, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(notes)


def add_note(title, message):
    notes = load_notes()
    note = Note(title, message)
    notes.append({
        "id": note.id,
        "title": note.title,
        "message": note.message,
        "created_at": note.created_at,
        "updated_at": note.updated_at
    })
    save_notes(notes)
    return note


def edit_note(note_id, title, message):
    notes = load_notes()
    for note in notes:
        if note["id"] == note_id:
            note["title"] = title
            note["message"] = message
            note["updated_at"] = datetime.now().isoformat()
            save_notes(notes)
            return note
    return None


def delete_note(note_id):
    notes = load_notes()
    for note in notes:
        if note["id"] == note_id:
            notes.remove(note)
            save_notes(notes)
            return True
    return False


def list_notes():
    notes = load_notes()
    for note in notes:
        print(f"ID: {note['id']}")
        print(f"Title: {note['title']}")
        print(f"Message: {note['message']}")
        print(f"Created At: {note['created_at']}")
        print(f"Updated At: {note['updated_at']}")
        print("-" * 20)


def main():
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()

    while True:
        print("Выберите действие:")
        print("1. Добавить заметку")
        print("2. Редактировать заметку")
        print("3. Удалить заметку")
        print("4. Список заметок")
        print("5. Выйти")

        choice = input("Введите номер действия: ")

        if choice == "1":
            title = input("Введите заголовок заметки: ")
            message = input("Введите тело заметки: ")
            add_note(title, message)
            print("Заметка успешно добавлена.")
        elif choice == "2":
            note_id = int(input("Введите ID заметки для редактирования: "))
            found = False
            for note in load_notes():
                if note["id"] == note_id:
                    title = input("Введите новый заголовок заметки: ")
                    message = input("Введите новое тело заметки: ")
                    edit_note(note_id, title, message)
                    found = True
                    print("Заметка успешно отредактирована.")
                    break
            if not found:
                print("Заметка с указанным ID не найдена.")
        elif choice == "3":
            note_id = input("Введите ID заметки для удаления: ")
            # note_id -= 1  # Уменьшаем на 1, чтобы соответствовать индексации в списке
            if delete_note(note_id):
                print("Заметка успешно удалена.")
            else:
                print("Заметка с указанным ID не найдена.")
        elif choice == "4":
            list_notes()
        elif choice == "5":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите действие из списка.")


main()
