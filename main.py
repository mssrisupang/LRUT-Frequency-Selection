from gui import setup_gui
from utils import load_data, get_file_path

def main():
    file_path = get_file_path()  # Dynamically get the file path
    df_area, df_peri, df_dist = load_data(file_path)  # Load data from Excel
    setup_gui(df_area, df_peri, df_dist, file_path)  # Run the GUI

if __name__ == "__main__":
    main()
