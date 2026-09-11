"""
ITECC04 - Data Structures and Algorithms
PART I - Student Record Manager
Data Structure: Dynamic Array ADT (implemented manually)

Note: Python's built-in list already resizes itself automatically, which would
defeat the purpose of this exercise. To truly implement the Dynamic Array
ourselves, we use a low-level fixed-size ctypes array as the internal storage
and manage capacity/resizing manually, the same way you would with a raw
array in Java or C.
"""

import ctypes


# ---------------------------------------------------------
# Student: simple data holder (the "record" stored in the array)
# ---------------------------------------------------------
class Student:
    def __init__(self, student_id, student_name, course, year_level):
        self.student_id = student_id
        self.student_name = student_name
        self.course = course
        self.year_level = year_level

    def __str__(self):
        return (f"Student ID   : {self.student_id}\n"
                f"Student Name : {self.student_name}\n"
                f"Course       : {self.course}\n"
                f"Year Level   : {self.year_level}")


# ---------------------------------------------------------
# DynamicArray: manually implemented Dynamic Array ADT
# ---------------------------------------------------------
class DynamicArray:
    INITIAL_CAPACITY = 5

    def __init__(self):
        self.capacity = DynamicArray.INITIAL_CAPACITY
        self.count = 0
        self.data = self._make_array(self.capacity)

    @staticmethod
    def _make_array(capacity):
        """Creates a new fixed-size low-level array (like `new Student[capacity]` in Java)."""
        return (capacity * ctypes.py_object)()

    def _resize(self):
        """Doubles the capacity of the internal array when it becomes full."""
        new_capacity = self.capacity * 2
        new_data = self._make_array(new_capacity)
        for i in range(self.count):
            new_data[i] = self.data[i]
        old_capacity = self.capacity
        self.data = new_data
        self.capacity = new_capacity
        print(f"[Array capacity increased from {old_capacity} to {new_capacity}]")

    def add(self, student):
        """Adds a new student at the end of the array, resizing if needed."""
        if self.count == self.capacity:
            print("Array is full.")
            self._resize()
        self.data[self.count] = student
        self.count += 1

    def get(self, index):
        if index < 0 or index >= self.count:
            raise IndexError(f"Invalid index: {index}")
        return self.data[index]

    def set(self, index, student):
        if index < 0 or index >= self.count:
            raise IndexError(f"Invalid index: {index}")
        self.data[index] = student

    def search(self, student_id):
        """Linear search by Student ID; returns index or -1 if not found."""
        for i in range(self.count):
            if self.data[i].student_id.lower() == student_id.lower():
                return i
        return -1

    def remove(self, index):
        """Removes the student at the given index and shifts remaining elements left."""
        if index < 0 or index >= self.count:
            return False
        for i in range(index, self.count - 1):
            self.data[i] = self.data[i + 1]
        self.data[self.count - 1] = None  # clear the now-unused last slot
        self.count -= 1
        return True

    def size(self):
        return self.count

    def get_capacity(self):
        return self.capacity

    def is_empty(self):
        return self.count == 0

    def display(self):
        if self.is_empty():
            print("No student records found.")
            return
        print("-" * 40)
        for i in range(self.count):
            print(f"Record #{i + 1}")
            print(self.data[i])
            print("-" * 40)


# ---------------------------------------------------------
# Console application logic
# ---------------------------------------------------------
students = DynamicArray()


def print_menu():
    print("================================")
    print("     STUDENT RECORD MANAGER")
    print("================================")
    print("1. Add Student")
    print("2. Display Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Remove Student")
    print("6. Display Array Information")
    print("7. Exit")


def read_int(prompt):
    while True:
        line = input(prompt).strip()
        try:
            return int(line)
        except ValueError:
            print("Please enter a valid whole number.")


def read_int_in_range(prompt, low, high):
    while True:
        value = read_int(prompt)
        if low <= value <= high:
            return value
        print(f"Please enter a number between {low} and {high}.")


def read_non_empty(prompt):
    while True:
        line = input(prompt).strip()
        if line:
            return line
        print("This field cannot be empty.")


def add_student():
    print("\n-- Add Student --")
    student_id = read_non_empty("Student ID: ")

    if students.search(student_id) != -1:
        print("A student with this ID already exists. Add cancelled.")
        return

    name = read_non_empty("Student Name: ")
    course = read_non_empty("Course: ")
    year = read_int_in_range("Year Level (1-6): ", 1, 6)

    students.add(Student(student_id, name, course, year))
    print("Student added successfully.")


def display_students():
    print("\n-- Student List --")
    students.display()
    print(f"Total students: {students.size()}")


def search_student():
    print("\n-- Search Student --")
    student_id = read_non_empty("Enter Student ID to search: ")
    index = students.search(student_id)
    if index == -1:
        print("Student not found.")
    else:
        print("Student found:")
        print(students.get(index))


def update_student():
    print("\n-- Update Student --")
    student_id = read_non_empty("Enter Student ID to update: ")
    index = students.search(student_id)
    if index == -1:
        print("Student not found.")
        return

    existing = students.get(index)
    print(f"Current record:\n{existing}")
    print("Enter new values (leave blank to keep current value):")

    name = input(f"Student Name [{existing.student_name}]: ").strip()
    if name:
        existing.student_name = name

    course = input(f"Course [{existing.course}]: ").strip()
    if course:
        existing.course = course

    year_str = input(f"Year Level [{existing.year_level}]: ").strip()
    if year_str:
        try:
            year = int(year_str)
            if 1 <= year <= 6:
                existing.year_level = year
            else:
                print("Year level out of range; kept previous value.")
        except ValueError:
            print("Invalid number; kept previous value.")

    students.set(index, existing)
    print("Student updated successfully.")


def remove_student():
    print("\n-- Remove Student --")
    student_id = read_non_empty("Enter Student ID to remove: ")
    index = students.search(student_id)
    if index == -1:
        print("Student not found.")
        return
    students.remove(index)
    print("Student removed successfully.")


def display_array_info():
    print("\n-- Array Information --")
    print(f"Current number of students : {students.size()}")
    print(f"Current array capacity     : {students.get_capacity()}")


def main():
    choice = None
    while choice != 7:
        print_menu()
        choice = read_int("Enter your choice: ")

        if choice == 1:
            add_student()
        elif choice == 2:
            display_students()
        elif choice == 3:
            search_student()
        elif choice == 4:
            update_student()
        elif choice == 5:
            remove_student()
        elif choice == 6:
            display_array_info()
        elif choice == 7:
            print("Exiting Student Record Manager. Goodbye!")
        else:
            print("Invalid choice. Please try again.")

        print()


if __name__ == "__main__":
    main()
