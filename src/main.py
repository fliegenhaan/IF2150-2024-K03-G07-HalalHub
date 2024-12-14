from views.main_window import MainWindow
import os

def init_data_directory():
    """Initialize data directory and required CSV files"""
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

if __name__ == "__main__":
    data_dir = init_data_directory()
    app = MainWindow()
    app.run()
