#!/bin/python3

import os
import pandas as pd
import matplotlib.pyplot as plt


data = pd.DataFrame(
    columns=[
        "Назва",
        "Автор",
        "Рік видання",
        "Жанр",
        "Кількість примірників",
    ]
)


# ==============================================


def load_books_from_csv(file_path):
    return pd.read_csv(file_path)


def save_books_to_csv(file_path, df):
    df.to_csv(file_path, index=False)


def add_book(df, book):
    return pd.concat([df, pd.DataFrame([book])], ignore_index=True)


def delete_book(df, title):
    return df[df['Назва'] != title]


def display_books(df):
    print(df.to_markdown(index=False, tablefmt="grid"))


# ==============================================


def total_books_count(df):
    return df['Кількість примірників'].sum()


def popular_genres(df):
    return df['Жанр'].value_counts()


def search_books(df, author=None, year=None):
    if author:
        df = df[df['Автор'] == author]
    if year:
        df = df[df['Рік видання'] == year]
    return df


# ==============================================


def plot_genre_distribution(df):
    genre_counts = df['Жанр'].value_counts()
    genre_counts.plot.pie(
        autopct='%1.1f%%',
        startangle=90,
        ylabel='',
        title="Розподіл книг за жанрами"
    )

    plt.show()


def plot_books_by_year(df):
    df['Рік видання'] = pd.to_numeric(df['Рік видання'], errors='coerce')

    year_counts = df.groupby('Рік видання')['Кількість примірників'].sum()
    year_counts.plot(
        kind='bar',
        title="Кількість книг за роками видання",
        xlabel="Рік",
        ylabel="Кількість"
    )

    plt.show()


# ==============================================


def clean_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def print_menu(commands):
    print(" ====== MENU =============")
    for hotkey, command in commands.items():
        command_doc = command[1]

        print(f" {hotkey} | {command_doc}")
    print(" =========================")


def main():
    default_filename = "books.csv"

    def cmd_load():
        global data

        filename = input("Введіть ім'я файлу: ")
        try:
            data = load_books_from_csv(filename)
        except IOError:
            print()
            print(f"Can't open file \"{filename}\"!")
        else:
            print("Дані завантажено!")

    def cmd_print_data():
        global data

        display_books(data)

    def cmd_save_data():
        global data

        filename = input("Введіть ім'я файлу: ")
        try:
            save_books_to_csv(filename, data)
        except IOError:
            print()
            print(f"Can't open file \"{filename}\"!")
        else:
            print("Дані завантажено!")

    def cmd_delete_book():
        global data

        title = input("Введіть назву книги: ")
        if title not in data["Назва книги"].values:
            print("Книгу не знайдено!")
            return

        data = data[data['Назва книги'] != title]
        print("Книгу видалено!")

    def cmd_search_books():
        global data

        author = input("Введіть автора (ентер щоб пропустити): ")
        year = None
        if author == "":
            year = input("Введіть рік публікації: ")
            year = int(year) if year else None

        results = search_books(data, author, year)
        if results.empty:
            print("Книгу не знайдено!")
        else:
            display_books(results)

    def cmd_total_books():
        global data

        print(f"Загальна кількість книг: {total_books_count(data)}")

    def cmd_plot_genre_distribution():
        global data

        plot_genre_distribution(data)

    def cmd_plot_books_by_year():
        global data

        plot_books_by_year(data)

    commands = {
        "l": (cmd_load, "load data from file"),
        "p": (cmd_print_data, "print data"),
        "d": (cmd_delete_book, "delete book"),
        "s": (cmd_save_data, "save data"),
        "f": (cmd_search_books, "search books"),
        "t": (cmd_total_books, "total number of books"),
        "v": (cmd_plot_genre_distribution, "plot genre distribution"),
        "y": (cmd_plot_books_by_year, "plot books by year"),
        "q": (exit, "exit"),
    }

    while True:
        clean_screen()
        print_menu(commands)

        hotkey = input(">>> ").strip().lower()

        command = commands.get(hotkey)

        if command is None:
            input("Команду не знайдено!")
            continue
        command_func = command[0]

        command_func()
        input("Нажміть ентер для продовження")


if __name__ == '__main__':
    main()
