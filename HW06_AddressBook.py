from collections import UserDict
from typing import List, Optional

class Field:
    """Базовий клас для всіх полів запису. Зберігає одне значення (рядок)."""
    value: str

    def __init__(self, value: str) -> None:
        """Ініціалізує поле значенням value."""
        self.value = value

    def __str__(self) -> str:
        """Повертає рядкове представлення значення поля."""
        return str(self.value)

class Name(Field):
    """
    Клас Name успадковує Field та використовується для зберігання імені контакту.
    Є обов'язковим полем без додаткової логіки.
    """
    pass  # Додаткова логіка не потрібна, використовуємо реалізацію Field

class Phone(Field):
    """
    Клас Phone успадковує Field та використовується для зберігання номера телефону.
    Перевіряє, що номер складається рівно з 10 цифр, інакше викликає ValueError.
    """
    def __init__(self, value: str) -> None:
        """
        Ініціалізує об'єкт Phone заданим значенням (рядком).
        Перевіряє, що номер містить рівно 10 цифр (у протилежному випадку генерує ValueError).
        """
        if not isinstance(value, str):
            raise ValueError("Номер телефону має бути рядком з 10 цифр.")
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Номер телефону повинен складатися рівно з 10 цифр.")
        # Викликаємо конструктор Field для встановлення value
        super().__init__(value)

class Record:
    """
    Клас Record зберігає інформацію про контакт (запис адресної книги).
    Містить об'єкт Name та список об'єктів Phone.
    Має методи для додавання, видалення, редагування та пошуку телефонних номерів.
    """
    name: Name
    phones: List[Phone]

    def __init__(self, name: str) -> None:
        """
        Ініціалізує запис Record із заданим ім'ям контакту.
        Ім'я зберігається як об'єкт Name; список телефонів ініціалізується порожнім.
        """
        self.name = Name(name)            # Створюємо об'єкт Name для імені
        self.phones: List[Phone] = []     # Порожній список телефонів на початку

    def add_phone(self, phone: str) -> None:
        """
        Додає новий номер телефону до запису.
        Приймає номер як рядок, створює об'єкт Phone (відбувається валідація) і додає його до списку.
        У випадку некоректного номера генерується ValueError.
        """
        phone_obj = Phone(phone)          # Створення об'єкта Phone (виконується валідація)
        self.phones.append(phone_obj)     # Додавання до списку телефонів

    def remove_phone(self, phone: str) -> None:
        """
        Видаляє номер телефону із запису (за значенням).
        Якщо такий номер є у списку, видаляє відповідний об'єкт Phone.
        Якщо номер не знайдено, нічого не відбувається.
        """
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)     # Видаляємо знайдений номер
                break

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """
        Замінює існуючий номер телефону на новий.
        Якщо старий номер присутній, створюється об'єкт Phone для нового номера і старий замінюється новим.
        Якщо новий номер некоректний (не 10 цифр), генерується ValueError.
        Якщо старий номер не знайдено, зміни не виконуються.
        """
        for idx, p in enumerate(self.phones):
            if p.value == old_phone:
                new_phone_obj = Phone(new_phone)  # Може викликати ValueError, якщо new_phone некоректний
                self.phones[idx] = new_phone_obj  # Замінюємо старий номер новим
                break

    def find_phone(self, phone: str) -> Optional[Phone]:
        """
        Шукає заданий номер телефону в записі.
        Повертає об'єкт Phone, якщо знайдено, або None, якщо такого номера немає.
        """
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self) -> str:
        """Повертає рядок з ім'ям контакту та всіма його номерами телефонів."""
        phones_str = "; ".join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"

class AddressBook(UserDict):
    """
    Клас AddressBook призначений для управління кількома записами контактів.
    Успадковується від UserDict, діє як словник із ключами-іменами контактів та об'єктами Record у якості значень.
    Містить методи для додавання, пошуку та видалення записів.
    """
    def add_record(self, record: Record) -> None:
        """
        Додає Record (запис) до адресної книги.
        Запис зберігається у self.data: ключ - ім'я контакту (record.name.value), значення - об'єкт Record.
        """
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        """
        Знаходить та повертає Record за ім'ям контакту.
        Повертає об'єкт Record, якщо знайдено, або None, якщо запис відсутній.
        """
        return self.data.get(name)

    def delete(self, name: str) -> bool:
        """
        Видаляє запис (Record) з адресної книги за вказаним ім'ям контакту.
        Повертає True, якщо запис був знайдений і видалений, або False, якщо запису з таким ім'ям немає.
        """
        if name in self.data:
            del self.data[name]
            return True
        return False

# Приклад використання системи AddressBook
if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    print("Всі записи в адресній книзі:")
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    print("\nПісля редагування телефону John:")
    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"\nЗнайдений телефон для {john.name}: {found_phone}")  # Виведення: John: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
    print("\nПісля видалення Jane:")
    for name, record in book.data.items():
        print(record)