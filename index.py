import hashlib
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ==============================
# FUNCTION TO CALCULATE HASH
# ==============================
def calculate_hash(filepath):
    hash_algo = hashlib.sha256()

    try:
        with open(filepath, 'rb') as file:
            while True:
                chunk = file.read(4096)

                if not chunk:
                    break

                hash_algo.update(chunk)

        return hash_algo.hexdigest()

    except:
        return None


# ==============================
# STORE FILE HASHES
# ==============================
file_hashes = {}


# ==============================
# EVENT HANDLER
# ==============================
class IntegrityHandler(FileSystemEventHandler):

    # NEW FILE
    def on_created(self, event):

        if not event.is_directory:

            file_hashes[event.src_path] = calculate_hash(event.src_path)

            print(f"\n[NEW FILE] {event.src_path}")

    # MODIFIED FILE
    def on_modified(self, event):

        if not event.is_directory:

            new_hash = calculate_hash(event.src_path)

            old_hash = file_hashes.get(event.src_path)

            if old_hash and new_hash != old_hash:

                print(f"\n[MODIFIED] {event.src_path}")

            file_hashes[event.src_path] = new_hash

    # DELETED FILE
    def on_deleted(self, event):

        if not event.is_directory:

            print(f"\n[DELETED] {event.src_path}")

            file_hashes.pop(event.src_path, None)


# ==============================
# INITIALIZE HASHES
# ==============================
def initialize_hashes(folder):

    for root, dirs, files in os.walk(folder):

        for file in files:

            path = os.path.join(root, file)

            file_hashes[path] = calculate_hash(path)


# ==============================
# MAIN PROGRAM
# ==============================
if __name__ == "__main__":

    folder_path = input("Enter folder path to monitor: ").strip()

    if not os.path.exists(folder_path):

        print("\n[-] Invalid folder path!")

        exit()

    print("\nMonitoring started...\n")

    # Store initial hashes
    initialize_hashes(folder_path)

    # Create observer
    event_handler = IntegrityHandler()

    observer = Observer()

    observer.schedule(event_handler, folder_path, recursive=True)

    observer.start()

    try:
        while True:
            pass

    except KeyboardInterrupt:

        observer.stop()

    observer.join()
