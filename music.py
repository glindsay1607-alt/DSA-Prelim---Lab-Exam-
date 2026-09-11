"""
ITECC04 - Data Structures and Algorithms
PART II - Music Playlist Manager
Data Structure: Singly Linked List ADT (implemented manually)
"""


# ---------------------------------------------------------
# Song: simple data holder stored inside each Node
# ---------------------------------------------------------
class Song:
    def __init__(self, song_id, song_title, artist, duration):
        self.song_id = song_id
        self.song_title = song_title
        self.artist = artist
        self.duration = duration  # stored as text, e.g. "4:23"

    def __str__(self):
        return (f"Song ID    : {self.song_id}\n"
                f"Song Title : {self.song_title}\n"
                f"Artist     : {self.artist}\n"
                f"Duration   : {self.duration}")


# ---------------------------------------------------------
# Node: holds song data and a reference to the next node
# ---------------------------------------------------------
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


# ---------------------------------------------------------
# LinkedList: manually implemented Singly Linked List ADT
# ---------------------------------------------------------
class LinkedList:
    def __init__(self):
        self.head = None
        self.count = 0

    def is_empty(self):
        return self.head is None

    def size(self):
        return self.count

    def insert_first(self, song):
        """Add a song at the beginning of the list."""
        new_node = Node(song)
        new_node.next = self.head
        self.head = new_node
        self.count += 1

    def insert_last(self, song):
        """Add a song at the end of the list."""
        new_node = Node(song)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self.count += 1

    def insert_at(self, position, song):
        """Insert a song at a specific 1-based position (1 = first).
        Returns False if the position is invalid."""
        if position < 1 or position > self.count + 1:
            return False
        if position == 1:
            self.insert_first(song)
            return True

        new_node = Node(song)
        current = self.head
        for _ in range(1, position - 1):
            current = current.next
        new_node.next = current.next
        current.next = new_node
        self.count += 1
        return True

    def search(self, song_id):
        """Linear search by Song ID; returns the Node or None if not found."""
        current = self.head
        while current is not None:
            if current.data.song_id.lower() == song_id.lower():
                return current
            current = current.next
        return None

    def delete(self, song_id):
        """Remove the first song matching the given Song ID."""
        if self.head is None:
            return False

        if self.head.data.song_id.lower() == song_id.lower():
            self.head = self.head.next
            self.count -= 1
            return True

        current = self.head
        while current.next is not None and current.next.data.song_id.lower() != song_id.lower():
            current = current.next

        if current.next is None:
            return False  # not found

        current.next = current.next.next  # bypass the node to remove
        self.count -= 1
        return True

    def display(self):
        """Traverse the list and print every song, from head until NULL."""
        if self.is_empty():
            print("The playlist is empty.")
            return
        current = self.head
        position = 1
        print("-" * 40)
        while current is not None:
            print(f"Position #{position}")
            print(current.data)
            print("-" * 40)
            current = current.next
            position += 1
        print(f"Total songs: {self.count}")


# ---------------------------------------------------------
# Console application logic
# ---------------------------------------------------------
playlist = LinkedList()


def print_menu():
    print("================================")
    print("     MUSIC PLAYLIST MANAGER")
    print("================================")
    print("1. Add Song at Beginning")
    print("2. Add Song at End")
    print("3. Insert Song at Position")
    print("4. Display Playlist")
    print("5. Search Song")
    print("6. Remove Song")
    print("7. Display Playlist Size")
    print("8. Exit")


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


def prompt_new_song():
    song_id = read_non_empty("Song ID: ")
    if playlist.search(song_id) is not None:
        print("A song with this ID already exists.")
        return None
    title = read_non_empty("Song Title: ")
    artist = read_non_empty("Artist: ")
    duration = read_non_empty("Duration (e.g. 4:23): ")
    return Song(song_id, title, artist, duration)


def add_song_at_beginning():
    print("\n-- Add Song at Beginning --")
    song = prompt_new_song()
    if song is None:
        return
    playlist.insert_first(song)
    print("Song added at the beginning.")


def add_song_at_end():
    print("\n-- Add Song at End --")
    song = prompt_new_song()
    if song is None:
        return
    playlist.insert_last(song)
    print("Song added at the end.")


def insert_song_at_position():
    print("\n-- Insert Song at Position --")
    max_pos = playlist.size() + 1
    position = read_int_in_range(f"Enter position (1 to {max_pos}): ", 1, max_pos)
    song = prompt_new_song()
    if song is None:
        return
    ok = playlist.insert_at(position, song)
    if ok:
        print(f"Song inserted at position {position}.")
    else:
        print("Invalid position. Song not inserted.")


def display_playlist():
    print("\n-- Playlist --")
    playlist.display()


def search_song():
    print("\n-- Search Song --")
    song_id = read_non_empty("Enter Song ID to search: ")
    found = playlist.search(song_id)
    if found is None:
        print("Song not found.")
    else:
        print("Song found:")
        print(found.data)


def remove_song():
    print("\n-- Remove Song --")
    song_id = read_non_empty("Enter Song ID to remove: ")
    removed = playlist.delete(song_id)
    if removed:
        print("Song removed successfully.")
    else:
        print("Song not found.")


def display_playlist_size():
    print("\n-- Playlist Size --")
    print(f"Total songs in playlist: {playlist.size()}")


def main():
    choice = None
    while choice != 8:
        print_menu()
        choice = read_int("Enter your choice: ")

        if choice == 1:
            add_song_at_beginning()
        elif choice == 2:
            add_song_at_end()
        elif choice == 3:
            insert_song_at_position()
        elif choice == 4:
            display_playlist()
        elif choice == 5:
            search_song()
        elif choice == 6:
            remove_song()
        elif choice == 7:
            display_playlist_size()
        elif choice == 8:
            print("Exiting Music Playlist Manager. Goodbye!")
        else:
            print("Invalid choice. Please try again.")

        print()


if __name__ == "__main__":
    main()
