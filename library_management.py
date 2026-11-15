import json
import os

books = {}
students = {}
issued = []

BOOK_FILE = "books.json"
STUDENT_FILE = "students.json"
ISSUED_FILE = "issued.json"


def create_files():

    if not os.path.exists(BOOK_FILE):
        with open(BOOK_FILE, "w") as file:
            json.dump({}, file, indent=4)

    if not os.path.exists(STUDENT_FILE):
        with open(STUDENT_FILE, "w") as file:
            json.dump({}, file, indent=4)

    if not os.path.exists(ISSUED_FILE):
        with open(ISSUED_FILE, "w") as file:
            json.dump([], file, indent=4)


def load_data():

    global books, students, issued

    with open(BOOK_FILE, "r") as file:
        books = json.load(file)

    with open(STUDENT_FILE, "r") as file:
        students = json.load(file)

    with open(ISSUED_FILE, "r") as file:
        issued = json.load(file)

    print("Data loaded successfully")



def saved_data():

    with open(BOOK_FILE, "w") as file:
        json.dump(books, file, indent=4)

    with open(STUDENT_FILE, "w") as file:
        json.dump(students, file, indent=4)

    with open(ISSUED_FILE, "w") as file:
        json.dump(issued, file, indent=4)



def add_book():

    book_id = input("Enter the book ID: ")

    if book_id in books:
        print("Book already exists")
        return

    title = input("Enter the book title: ")
    author = input("Enter author name: ")
    category = input("Enter category: ")

    try:
        quantity = int(input("Enter quantity: "))
    except ValueError:
        print("Please enter a valid number")
        return

    if quantity <= 0:
        print("Quantity must be greater than 0")
        return

    books[book_id] = {
        "title": title,
        "author": author,
        "category": category,
        "total": quantity,
        "available": quantity
    }

    saved_data()

    print("Book added successfully")



def display_books():

    if not books:
        print("No books available")
        return

    for book_id, details in books.items():

        print("\n-------------------------")
        print("Book ID:", book_id)
        print("Title:", details["title"])
        print("Author:", details["author"])
        print("Category:", details["category"])
        print("Total:", details["total"])
        print("Available:", details["available"])




def search_book():

    search = input("Enter book ID or title: ")

    for book_id, details in books.items():

        if book_id == search or details["title"].lower() == search.lower():

            print("\nBook found")
            print("Book ID:", book_id)
            print("Title:", details["title"])
            print("Author:", details["author"])
            print("Category:", details["category"])
            print("Total:", details["total"])
            print("Available:", details["available"])

            return

    print("Book not found")




def register_student():

    student_id = input("Enter student ID: ")

    if student_id in students:
        print("Student already exists")
        return

    student_name = input("Enter student name: ")
    department = input("Enter department: ")
    contact = input("Enter number: ")

    students[student_id] = {
        "name": student_name,
        "department": department,
        "contact": contact
    }

    saved_data()

    print("Student registered successfully")



def issue_book():

    student_id = input("Enter student ID: ")
    book_id = input("Enter book ID: ")

    
    if student_id not in students:
        print("Student does not exist")
        return

    
    if book_id not in books:
        print("Book does not exist")
        return

    
    if books[book_id]["available"] <= 0:
        print("Book is not available")
        return


    student_issue = 0

    for record in issued:

        if record["student_id"] == student_id:
            student_issue += 1

    if student_issue >= 3:
        print("Cannot issue more than 3 books")
        return

    
    books[book_id]["available"] -= 1

    
    record = {
        "student_id": student_id,
        "student_name": students[student_id]["name"],
        "book_id": book_id,
        "book_title": books[book_id]["title"]
    }

    issued.append(record)

    saved_data()

    print("Book issued successfully")



def return_book():

    student_id = input("Enter student ID: ")
    book_id = input("Enter book ID: ")

    for data in issued:

        if data["student_id"] == student_id and data["book_id"] == book_id:

            books[book_id]["available"] += 1

            issued.remove(data)

            saved_data()

            print("Book returned successfully")
            return

    print("No matching issue record found")




def available_books():

    found = False

    for book_id, details in books.items():

        if details["available"] > 0:

            found = True

            print(
                book_id,
                details["title"],
                "Available:",
                details["available"]
            )

    if not found:
        print("No books are currently available")



def display_issued():

    if not issued:
        print("No books have been issued")
        return

    for record in issued:

        print("\n-------------------------")
        print("Student ID:", record["student_id"])
        print("Student Name:", record["student_name"])
        print("Book ID:", record["book_id"])
        print("Book Title:", record["book_title"])



def delete_book():

    book_id = input("Enter the ID of the book to delete: ")

    if book_id in books:

        # Don't delete if copies are currently issued
        if books[book_id]["available"] != books[book_id]["total"]:
            print("Cannot delete this book because copies are currently issued")
            return

        del books[book_id]

        saved_data()

        print("Book deleted successfully")

    else:
        print("Book not found")



create_files()
load_data()

while True:


    print("     LIBRARY MANAGEMENT SYSTEM")


    print("1. Add a New Book")
    print("2. Display All Books")
    print("3. Search for a Book")
    print("4. Register Student")
    print("5. Issue a Book")
    print("6. Return a Book")
    print("7. Display Available Books")
    print("8. Display Issued Books")
    print("9. Delete a Book")
    print("10. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_book()

    elif choice == "2":
        display_books()

    elif choice == "3":
        search_book()

    elif choice == "4":
        register_student()

    elif choice == "5":
        issue_book()

    elif choice == "6":
        return_book()

    elif choice == "7":
        available_books()

    elif choice == "8":
        display_issued()

    elif choice == "9":
        delete_book()

    elif choice == "10":
        saved_data()
        print("Data saved. Exiting...")
        break

    else:
        print("Invalid choice. Try again.")