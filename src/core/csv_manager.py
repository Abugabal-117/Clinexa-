import csv
import os
from threading import Lock


class CSVManager:
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        if 'DATA_DIR' in os.environ:
            self.data_dir = os.environ['DATA_DIR']
        else:
            self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        self._initialized = True
    
    def read_csv(self, filename):
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.exists(filepath):
            return []
        
        with open(filepath, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return list(reader)
    
    def write_csv(self, filename, data, fieldnames):
        filepath = os.path.join(self.data_dir, filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    
    def append_csv(self, filename, row, fieldnames):
        filepath = os.path.join(self.data_dir, filename)
        file_exists = os.path.exists(filepath)
        
        with open(filepath, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)
    
    def delete_csv(self, filename):
        filepath = os.path.join(self.data_dir, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
