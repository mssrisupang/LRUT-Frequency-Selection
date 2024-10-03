import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

def calculate_pearson_correlation(df, case_number, frequencies, conf_frame, result_text_widget):
    correlation_matrix = np.zeros((3, 3))
    result_text_widget.delete(1.0, tk.END)  # Clear previous results
    max_correlation = -np.inf
    best_pair = None

    # Calculate Pearson correlations between each pair of frequencies
    for i in range(3):
        for j in range(3):
            freq1 = frequencies[i]
            freq2 = frequencies[j]
            correlation, _ = pearsonr(df[df['#Case'] == case_number][freq1], df[df['#Case'] == case_number][freq2])
            correlation_matrix[i][j] = correlation

            # Append the Pearson correlation results to the text widget
            if i != j:
                result_text_widget.insert(tk.END, f'Pearson Correlation between {freq1} and {freq2}: {correlation:.2f}\n')
                # Keep track of the best pair of frequencies
                if correlation > max_correlation:
                    max_correlation = correlation
                    best_pair = (freq1, freq2)

    # Display the best pair summary in the summary text widget
    if best_pair:
        result_text_widget.insert(tk.END, f'The best pair of frequencies is {best_pair[0]} and {best_pair[1]} with a Pearson correlation of {max_correlation:.2f}.\n')

    # Plot the confusion matrix using Seaborn in the same window
    fig, ax = plt.subplots(figsize=(3, 3))  
    sns.heatmap(correlation_matrix, annot=True, lw=1, linecolor='black', clip_on=False,
                cmap='Blues', cbar=False, ax=ax, square=True, annot_kws={"size": 10},
                xticklabels=frequencies, yticklabels=frequencies)

    for ind, row in enumerate(correlation_matrix):
        row_no_diagonal = np.copy(row)
        row_no_diagonal[ind] = -np.inf  
        
        max_col = np.argmax(row_no_diagonal)
        ax.add_patch(plt.Rectangle((max_col, ind), 1, 1, fc='none', ec='red', lw=3, clip_on=False))

    ax.set_title(f'Pearson Correlation for Case {case_number}', fontsize=10, pad=30, va='top')  # Add padding between title and plot
    ax.tick_params(axis='both', which='major', labelsize=8)

    plt.xticks(rotation=0, ha='center', va='top', fontsize=8)
    plt.yticks(rotation=0, fontsize=8)
    plt.tight_layout(pad=2.0)

    #Embed the plot in Tkinter
    for widget in conf_frame.winfo_children():
        widget.destroy()  # Clear previous figures
    canvas = FigureCanvasTkAgg(fig, master=conf_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=1, ipadx=2, ipady=2)
    return best_pair


# Function to overlay DWG plots with transparency
def display_overlay_dwg_image(case_number, best_pair, base_path,overlay_frame):
    freq1, freq2 = best_pair
    filename1 = f"case{case_number}_{freq1}.png"
    filename2 = f"case{case_number}_{freq2}.png"
    
    image_path1 = f"{base_path}/{filename1}"
    image_path2 = f"{base_path}/{filename2}"

    # Try to open both DWG images and overlay them
    try:
        img1 = Image.open(image_path1).convert("RGBA")
        img2 = Image.open(image_path2).convert("RGBA")

        # Resize both images to the same size
        img1 = img1.resize((250, 250), Image.ANTIALIAS)
        img2 = img2.resize((250, 250), Image.ANTIALIAS)

        # Overlay the images using transparency
        overlay_img = Image.blend(img1, img2, alpha=0.5)  # 50% transparency for both images

        fig, ax = plt.subplots(figsize=(2, 2))
        ax.imshow(overlay_img)
        ax.set_title(f"Overlay of {freq1} and {freq2} for Case {case_number}", fontsize=7)
        ax.axis('off')

        # Embed the plot in the Tkinter window
        for widget in overlay_frame.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=overlay_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=3, column=1, ipadx=2, ipady=2)

    except Exception as e:
        print(f"Error displaying overlay images: {e}")

# Function for DWG Image display
def display_dwg_image(case_number, frequencies, dwg_frame, base_path):
    for widget in dwg_frame.winfo_children():
        widget.destroy()

    # Create subplots for 3 images (one for each frequency)
    fig, axes = plt.subplots(1, 3, figsize=(5, 3))  # 3 subplots horizontally

    for i, freq in enumerate(frequencies):
        filename = f"case{case_number}_{freq}.png"  # Create filename based on case number and frequency
        image_path = f"{base_path}/{filename}"  # Use base path from user input

        try:
            img = Image.open(image_path)
            img = img.resize((120, 120), Image.ANTIALIAS)
            axes[i].imshow(img)  # Display image in the subplot
            axes[i].set_title(f"Case {case_number} - {freq}", fontsize=8)
            axes[i].axis('off')  # Turn off the axis
        except Exception as e:
            print(f"Image for {filename} not found: {e}")
            axes[i].set_title(f"Image not found: {freq}")
            axes[i].axis('off')

    plt.subplots_adjust(wspace=0.3)  # Adjust space between the images
    plt.tight_layout()
    
    # Embed the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=dwg_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=2, column=0, padx=2, pady=2, sticky="nsew")

def display_ground_truth_image(ground_frame, case_number, frequencies, base_path):
    for widget in ground_frame.winfo_children():
        widget.destroy()

    dwg_folder = "polar_DWG"
    filename = f"case{case_number}.png"
    image_path = f"{base_path}/{dwg_folder}/{filename}"  # Use base path from user input

    if os.path.exists(image_path):
        img = Image.open(image_path)
        img = img.resize((250, 250), Image.ANTIALIAS)  # Adjust the size as needed
        
        img_photo = ImageTk.PhotoImage(img)

        dwg_image_label = tk.Label(ground_frame, image=img_photo)
        dwg_image_label.image = img_photo  
        dwg_image_label.grid(row=2, column=2)
    else:
        print(f"Image file does not exist: {image_path}")
