from pathlib import Path
import json

class HistoryManager:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.history = []
        self.index = -1

    def load(self):
        try:
            with open(self.file_path, "r") as f:
                self.history = json.load(f)
        except FileNotFoundError:
            self.history = []

    def save(self):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.file_path, "w") as f:
            json.dump(self.history, f)

    def append(self, entry: str):
        self.history.append(entry)
        self.index = len(self.history)

    def back(self):
        if self.history and self.index > 0:
            self.index -= 1
            return self.history[self.index]
        return ""

    def forward(self):
        if self.history and self.index < len(self.history) - 1:
            self.index += 1
            return self.history[self.index]
        self.index = -1
        return ""
