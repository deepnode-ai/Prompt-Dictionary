import json
import shutil
import datetime
import streamlit as st

class DataManager:
    def __init__(self, filename):
        self.filename = filename

    def load_data(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_data(self, data):
        try:
            with open(self.filename, 'w') as file:
                json.dump(data, file)
            self.backup_data()  # Backup after saving
        except IOError as e:
            st.error(f"Error saving data: {str(e)}")

    def backup_data(self):
        backup_file = f'{self.filename}_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.backup'
        shutil.copy(self.filename, backup_file)

# Usage
data_manager = DataManager('data.json')

