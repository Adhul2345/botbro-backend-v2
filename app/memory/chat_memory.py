import json
import os

class ChatMemory:
    def __init__(self, memory_file='data/memory.json'):
        self.memory_file = memory_file
        self.memory = []
        self.load_memory()

    def add_message(self, role, content):
        # Automatically convert 'bot' role to 'assistant'
        if role == "bot":
            role = "assistant"
        self.memory.append({"role": role, "content": content})
        self.save_memory()

    def get_memory(self):
        return self.memory

    def get_messages(self):
        return self.memory

    def save_memory(self):
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=2)

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                self.memory = json.load(f)

            # 🔥 Fix any legacy 'bot' messages to 'assistant'
            for message in self.memory:
                if message["role"] == "bot":
                    message["role"] = "assistant"
            self.save_memory()  # Save corrected version

        else:
            self.memory = []
