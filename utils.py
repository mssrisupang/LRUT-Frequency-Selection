import os
import pandas as pd
from tkinter import filedialog

def load_data(file_path):
    df_area = pd.read_excel(file_path, sheet_name='Area')
    df_peri = pd.read_excel(file_path, sheet_name='Perimeter')
    df_dist = pd.read_excel(file_path, sheet_name='Distance')
    return df_area, df_peri, df_dist

def get_file_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'data', 'PolarPlotDigitization.xlsx')
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        file_path = filedialog.askopenfilename(title="Select the Excel file", filetypes=[("Excel files", "*.xlsx")])
    return file_path
