import tkinter as tk
from tkinter import filedialog
from analysis import calculate_pearson_correlation, display_overlay_dwg_image, display_dwg_image, display_ground_truth_image




def setup_gui(df_area, df_peri, df_dist, file_path):
    root = tk.Tk()
    root.title('LRUT Frequency Selection GUI')
    width = root.winfo_screenwidth() 
    height = root.winfo_screenheight()
    root.geometry("%dx%d" % (width, height))
    root.protocol("WM_DELETE_WINDOW", root.quit)

    # Frames setup
    right_frame = tk.Frame(root, width=200, height=300, bg='grey')
    right_frame.grid(row=0, column=1, padx=2, pady=2, sticky="nsew")

    conf_frame = tk.Frame(right_frame, width=200, height=300)
    conf_frame.grid(row=1, column=1, padx=2, pady=2)
    tk.Label(right_frame, text="Confusion Matrix").grid(row=0, column=1, padx=5, pady=5)

    overlay_frame = tk.Frame(right_frame, width=200, height=300)
    overlay_frame.grid(row=3, column=1, padx=2, pady=2)
    tk.Label(right_frame, text="Overlay Images").grid(row=2, column=1, padx=5, pady=5)

    left_frame = tk.Frame(root, width=200, height=300, bg='gray')
    left_frame.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")

    text_frame = tk.Frame(root, width=50, height=300, bg='gray')
    text_frame.grid(row=0, column=2, padx=2, pady=2, sticky="nsew")

    result_text_frame = tk.Frame(text_frame)
    result_text_frame.grid(row=0, column=2, padx=2, pady=2)
    result_text_widget = tk.Text(result_text_frame, height=10, width=50)
    result_text_widget.grid(row=0, column=2, padx=2, pady=2)


    ground_frame = tk.Frame(text_frame, width=50, height=55)
    tk.Label(text_frame, text="DWG Image").grid(row=1, column=2, padx=2, pady=2) 
    ground_frame.grid(row=3, column=2, padx=2, pady=2, sticky="nsew")


    dwg_frame = tk.Frame(left_frame, width=100, height=200)
    tk.Label(left_frame, text="Polar Plots").grid(row=0, column=0, padx=2, pady=2) 
    dwg_frame.grid(row=2, column=0, padx=2, pady=2, sticky="nsew")



    tool_bar = tk.Frame(left_frame, width=100, height=200)
    tool_bar.grid(row=4, column=0, padx=2, pady=2)

    # Dropdown menu for selecting case number
    tk.Label(tool_bar, text="Select Case Number").grid(row=1, column=0, padx=5, pady=3, ipadx=10) 
    case_numbers = [3, 4, 8, 9, 10, 11, 13, 15, 17, 18, 19, 20, 21, 25, 27, 29, 30, 31, 33, 34, 35, 36, 38, 39, 40, 41]
    case_number_var = tk.StringVar()
    case_number_var.set(case_numbers[0])  # Default

    tk.OptionMenu(tool_bar, case_number_var, *case_numbers).grid(row=1, column=1, padx=5, pady=3, ipadx=10) 

    # Base path for DWG images
    base_path = tk.StringVar()
    tk.Entry(tool_bar, textvariable=base_path, width=50).grid(row=0, column=0, padx=5, pady=3, ipadx=10)

    def set_image_path():
        folder_path = filedialog.askdirectory()
        if folder_path:
            base_path.set(folder_path)

    tk.Button(tool_bar, text="Set Image Base Path", command=set_image_path).grid(row=0, column=1, padx=2, pady=2, ipadx=10)
    # Button to display overlay and DWG images and ground truth image
    def on_show_overlay_image(case_number, best_pair,overlay_frame,ground_frame):
        frequencies = ['36Hz', '44Hz', '67Hz'] 
        display_overlay_dwg_image(case_number, best_pair,  base_path.get(), overlay_frame)
        display_dwg_image(case_number, frequencies, dwg_frame, base_path.get())
        display_ground_truth_image(ground_frame, case_number, frequencies, base_path.get())

    # Button to calculate Pearson correlation and display confusion matrix
    def on_calculate_pearson():
        case_number = int(case_number_var.get())
        frequencies = ['36Hz', '44Hz', '67Hz']
        best_pair = calculate_pearson_correlation(df_area, case_number, frequencies, conf_frame, result_text_widget)
        on_show_overlay_image(case_number, best_pair, overlay_frame, ground_frame)

    tk.Button(tool_bar, text="Analysis", font=('tahoma 13') ,bg='RED',command=on_calculate_pearson).grid(row=2, column=1, padx=2, pady=2)

    root.mainloop()