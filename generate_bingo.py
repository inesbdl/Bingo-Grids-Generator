import os
import random
import io
from PIL import Image, ImageOps
from reportlab.pdfgen import canvas
import PyPDF2
from tqdm import tqdm
import tkinter as tk
from tkinter import Label, Entry, Button, messagebox, filedialog

def generate_bingo_grid(image_folder, num_rows, num_cols, border_size, num_images_to_fill):
    image_files = [f for f in os.listdir(image_folder) if f != 'empty_cell.png']
    random.shuffle(image_files)

    empty_cell_image = "empty_cell.png"
    empty_cell_path = os.path.join(image_folder, empty_cell_image)

    if not os.path.isfile(empty_cell_path):
        raise FileNotFoundError(f"L'image vide '{empty_cell_image}' n'a pas été trouvée dans le dossier '{image_folder}'.")

    if len(image_files) < num_images_to_fill:
        raise ValueError("Il n'y a pas assez d'images pour remplir le nombre de cases pleines demandé.")

    selected_images = image_files[:num_images_to_fill]

    while len(selected_images) < num_rows * num_cols:
        selected_images.append(empty_cell_image)

    random.shuffle(selected_images)

    custom_page_size = (8000, 6000)
    page_width, page_height = custom_page_size
    cell_size = min(int((page_width - 2 * border_size) // num_cols), int((page_height - 2 * border_size) // num_rows))

    pdf_bytes = io.BytesIO()
    c = canvas.Canvas(pdf_bytes, pagesize=custom_page_size)
    width, height = custom_page_size
    margin_x = (width - (num_cols * cell_size + 2 * border_size)) / 2
    margin_y = (height - (num_rows * cell_size + 2 * border_size)) / 2

    filled_images_count = 0
    empty_cells = []

    for i in range(num_rows):
        for j in range(num_cols):
            img_name = selected_images.pop()
            if img_name != empty_cell_image:
                filled_images_count += 1
            else:
                empty_cells.append((i, j))
            img_path = os.path.join(image_folder, img_name)
            with Image.open(img_path) as img:
                img = img.resize((cell_size, cell_size), Image.LANCZOS)
                img_with_border = ImageOps.expand(img, border=border_size, fill='white')
                img_temp_path = f'temp_image_{i}_{j}.png'
                img_with_border.save(img_temp_path)
            x = margin_x + j * (cell_size + 2 * border_size)
            y = height - (margin_y + (i + 1) * (cell_size + 2 * border_size))
            c.drawImage(img_temp_path, x, y, width=cell_size + 2 * border_size, height=cell_size + 2 * border_size)
            os.remove(img_temp_path)

    while filled_images_count < num_images_to_fill:
        if empty_cells:
            i, j = empty_cells.pop()
            img_name = random.choice(image_files[:num_images_to_fill])
            img_path = os.path.join(image_folder, img_name)
            with Image.open(img_path) as img:
                img = img.resize((cell_size, cell_size), Image.LANCZOS)
                img_with_border = ImageOps.expand(img, border=border_size, fill='white')
                img_temp_path = f'temp_image_{i}_{j}.png'
                img_with_border.save(img_temp_path)
            x = margin_x + j * (cell_size + 2 * border_size)
            y = height - (margin_y + (i + 1) * (cell_size + 2 * border_size))
            c.drawImage(img_temp_path, x, y, width=cell_size + 2 * border_size, height=cell_size + 2 * border_size)
            os.remove(img_temp_path)
            filled_images_count += 1

    c.save()
    pdf_bytes.seek(0)
    return pdf_bytes

def generate_grids():
    image_folder = image_folder_entry.get()
    num_rows = int(num_rows_entry.get())
    num_cols = int(num_cols_entry.get())
    border_size = int(border_size_entry.get())
    num_images_to_fill = int(num_images_to_fill_entry.get())
    num_grids_to_generate = int(num_grids_to_generate_entry.get())
    output_filename = output_filename_entry.get()

    try:
        bingo_pdfs = []
        total_iterations = num_grids_to_generate * num_rows * num_cols
        with tqdm(total=total_iterations) as pbar:
            for i in range(num_grids_to_generate):
                bingo_pdfs.append(generate_bingo_grid(image_folder, num_rows, num_cols, border_size, num_images_to_fill))
                pbar.update(num_rows * num_cols)

        output_pdf = PyPDF2.PdfWriter()

        for pdf_data in bingo_pdfs:
            input_pdf = PyPDF2.PdfReader(pdf_data)
            for page in input_pdf.pages:
                output_pdf.add_page(page)

        with open(output_filename, 'wb') as f:
            output_pdf.write(f)

        messagebox.showinfo("Succès", "Grilles générées avec succès.")
    except FileNotFoundError as e:
        messagebox.showerror("Erreur", str(e))
    except ValueError as e:
        messagebox.showerror("Erreur", str(e))
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur inattendue s'est produite : {str(e)}")

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        image_folder_entry.delete(0, tk.END)
        image_folder_entry.insert(0, folder_selected)

root = tk.Tk()
root.title("Générateur de Grilles de Bingo")
root.geometry("600x400")

Label(root, text="Dossier d'images:").grid(row=0, column=0, pady=5, padx=5, sticky='e')
image_folder_entry = Entry(root, width=30)
image_folder_entry.grid(row=0, column=1, pady=5, padx=5)
image_folder_entry.insert(0, 'images')
Button(root, text="Parcourir", command=select_folder).grid(row=0, column=2, pady=5, padx=5)

Label(root, text="Nombre de lignes:").grid(row=1, column=0, pady=5, padx=5, sticky='e')
num_rows_entry = Entry(root, width=10)
num_rows_entry.grid(row=1, column=1, pady=5, padx=5)
num_rows_entry.insert(0, '3')

Label(root, text="Nombre de colonnes:").grid(row=2, column=0, pady=5, padx=5, sticky='e')
num_cols_entry = Entry(root, width=10)
num_cols_entry.grid(row=2, column=1, pady=5, padx=5)
num_cols_entry.insert(0, '9')

Label(root, text="Taille de la bordure:").grid(row=3, column=0, pady=5, padx=5, sticky='e')
border_size_entry = Entry(root, width=10)
border_size_entry.grid(row=3, column=1, pady=5, padx=5)
border_size_entry.insert(0, '5')

Label(root, text="Nombre d'images à remplir:").grid(row=4, column=0, pady=5, padx=5, sticky='e')
num_images_to_fill_entry = Entry(root, width=10)
num_images_to_fill_entry.grid(row=4, column=1, pady=5, padx=5)
num_images_to_fill_entry.insert(0, '15')

Label(root, text="Nombre de grilles à générer:").grid(row=4, column=0, pady=5, padx=5, sticky='e')
num_grids_to_generate_entry = Entry(root, width=10)
num_grids_to_generate_entry.grid(row=4, column=1, pady=5, padx=5)
num_grids_to_generate_entry.insert(0, '100')

Label(root, text="Nom du fichier de sortie:").grid(row=5, column=0, pady=5, padx=5, sticky='e')
output_filename_entry = Entry(root, width=30)
output_filename_entry.grid(row=5, column=1, pady=5, padx=5)
output_filename_entry.insert(0, 'bingo_grids_combined.pdf')

generate_button = Button(root, text="Générer les grilles", command=generate_grids, bg='lightblue')
generate_button.grid(row=6, columnspan=3, pady=20)

root.mainloop()
