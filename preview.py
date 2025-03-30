import os
import time
import json
import colson
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ColsonHandler(FileSystemEventHandler):
    def __init__(self, colson_path: str):
        # Convert relative path to absolute, preserving the correct directory
        self.colson_path = os.path.abspath(os.path.join(os.getcwd(), colson_path))
        print(f"Watching {self.colson_path}")
        print(f"Preview at {self.colson_path.replace('.colson', '.json')}")
        self.json_path = self.colson_path.replace(".colson", ".json")
        self.last_valid = None
        self.last_modified = 0
        self.debounce_delay = 0.1  # seconds

        # Initial parse
        self.update_preview()

    def on_modified(self, event):
        if not event.src_path.endswith(".colson"):
            return

        modified_path = os.path.abspath(event.src_path)
        if modified_path != self.colson_path:
            return

        current_time = time.time()
        if current_time - self.last_modified < self.debounce_delay:
            return

        self.last_modified = current_time
        print(f"File changed, updating preview...")
        self.update_preview()

    def update_preview(self):
        try:
            with open(self.colson_path, "r", encoding="utf-8") as f:
                content = f.read()
                parsed = colson.loads(content)
                self.last_valid = parsed

                with open(self.json_path, "w", encoding="utf-8") as jf:
                    json.dump(parsed, jf, indent=2, ensure_ascii=False)
                print("Preview updated successfully")
        except Exception as e:
            print(f"Error updating preview: {e}")
            if self.last_valid:
                preview = {"error": str(e), "last_valid_state": self.last_valid}
                with open(self.json_path, "w", encoding="utf-8") as jf:
                    json.dump(preview, jf, indent=2, ensure_ascii=False)


def watch_colson(colson_path: str):
    event_handler = ColsonHandler(colson_path)
    observer = Observer()
    observer.schedule(
        event_handler, os.path.dirname(os.path.abspath(colson_path)), recursive=False
    )
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python preview.py path_to_colson")
        sys.exit(1)

    watch_colson(sys.argv[1])
