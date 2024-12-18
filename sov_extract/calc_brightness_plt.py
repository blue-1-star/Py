import os
import rawpy
import openpyxl
from openpyxl.styles import Font
from PIL import Image, ImageStat
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Функція обробки зображень (включно з ORF)
def process_image(img_path):
    if img_path.lower().endswith('.orf'):  # Обробка ORF-файлів через rawpy
        with rawpy.imread(img_path) as raw:
            rgb = raw.postprocess()
        img = Image.fromarray(rgb)
    else:
        img = Image.open(img_path)
    return img

# Функція обчислення яскравості через Pillow (grayscale)
def calculate_brightness_pil(image_path):
    img = process_image(image_path)  # Завантажуємо та обробляємо зображення
    grayscale_img = img.convert('L')  # Конвертація в градації сірого
    stat = ImageStat.Stat(grayscale_img)
    mean_brightness = stat.mean[0]
    return mean_brightness

# Функція обчислення яскравості для кольорових зображень
def calculate_brightness_color(image_path):
    img = process_image(image_path)  # Завантажуємо та обробляємо зображення
    stat = ImageStat.Stat(img)
    r, g, b = stat.mean[:3]  # Середні значення для RGB-каналів
    brightness = (0.299 * r + 0.587 * g + 0.114 * b)  # Яскравість з урахуванням вагових коефіцієнтів
    return brightness

# Функція для створення стовпчастого графіка
def plot_brightness(data, title, ax):
    values = data['Brightness_PIL']
    files = data['Filename']
    colors = plt.cm.Blues(np.linspace(0.4, 0.8, len(values)))
    ax.bar(files, values, color=colors)
    ax.set_title(title)
    ax.set_ylabel('Brightness (PIL)')
    ax.set_xlabel('Files')
    ax.tick_params(axis='x', rotation=45)

# Функція для обчислення яскравості і створення DataFrame
def calculate_brightness_dataframe(image_dir):
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.orf', '.jpg', '.jpeg'))]

    # Список для зберігання результатів
    results = []
    
    # Проходимо по всіх файлах та обчислюємо яскравість
    for img_file in image_files:
        img_path = os.path.join(image_dir, img_file)
        
        # Обчислюємо яскравість обома методами
        brightness_pil = calculate_brightness_pil(img_path)
        brightness_color = calculate_brightness_color(img_path)
        
        file_format = "ORF" if img_file.lower().endswith('.orf') else "JPEG"
        
        results.append({
            "Filename": img_file,
            "Format": file_format,
            "Brightness_PIL": brightness_pil,
            "Brightness_Color": brightness_color
        })

    # Створюємо DataFrame
    df = pd.DataFrame(results)
    
    # Додаємо ранги для обох методів
    df['Rank_in_Group_PIL'] = df.groupby('Format')['Brightness_PIL'].rank(ascending=False).astype(int)
    df['Rank_Global_PIL'] = df['Brightness_PIL'].rank(ascending=False).astype(int)
    df['Rank_in_Group_Color'] = df.groupby('Format')['Brightness_Color'].rank(ascending=False).astype(int)
    df['Rank_Global_Color'] = df['Brightness_Color'].rank(ascending=False).astype(int)

    return df

# Функція для створення таблиць у Excel
def save_brightness_excel(df, output_file):
    # Створюємо Excel-файл з трьома листами
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Лист 1: Оригінальний порядок
        df.sort_values(['Filename'], inplace=True)
        df.to_excel(writer, index=False, sheet_name='Original Order')

        # Лист 2: Сортовані по яскравості всередині груп (PIL)
        df.sort_values(['Format', 'Rank_in_Group_PIL'], inplace=True)
        df.to_excel(writer, index=False, sheet_name='Sorted by Brightness_PIL')

        # Лист 3: Сортовані по яскравості всередині груп (Color)
        df.sort_values(['Format', 'Rank_in_Group_Color'], inplace=True)
        df.to_excel(writer, index=False, sheet_name='Sorted by Brightness_Color')

        # Лист 4: Глобальне сортування по яскравості (PIL)
        df.sort_values(['Rank_Global_PIL'], inplace=True)
        df.to_excel(writer, index=False, sheet_name='Global Sorted by PIL')

        # Лист 5: Глобальне сортування по яскравості (Color)
        df.sort_values(['Rank_Global_Color'], inplace=True)
        df.to_excel(writer, index=False, sheet_name='Global Sorted by Color')

    print(f"Excel-файл '{output_file}' створено успішно!")

# Функція для побудови графіків
def create_brightness_plots(df):
    orf_data = df[df['Format'] == 'ORF']
    jpg_data = df[df['Format'] == 'JPEG']

    # Перші два графіки
    fig, axs = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)
    plot_brightness(orf_data, 'Brightness for ORF Files', axs[0])
    plot_brightness(jpg_data, 'Brightness for JPG Files', axs[1])
    output_path = os.path.join(image_dir, "brightness_graph.pdf")
    plt.savefig(output_path,  format="pdf", dpi=300, bbox_inches='tight')  # Рекомендується встановити високий dpi для якості
    plt.show()
    plt.close()
    # Третій графік: порівняння середньої яскравості
    mean_brightness = df.groupby('Format')['Brightness_PIL'].mean()
    formats = mean_brightness.index
    means = mean_brightness.values

    fig, ax = plt.subplots(figsize=(6, 6))
    colors = ['#1f77b4', '#ff7f0e']  # Кольори для ORF і JPG
    ax.bar(formats, means, color=colors)
    ax.set_title('Average Brightness: ORF vs JPG')
    ax.set_ylabel('Average Brightness (PIL)')
    ax.set_xlabel('File Format')
    output_path = os.path.join(image_dir, "comparision_orf.pdf")
    plt.savefig(output_path,  format="pdf", dpi=300, bbox_inches='tight')  # Рекомендується встановити високий dpi для якості
    plt.show()
    plt.close()
# Виконання коду
if __name__ == "__main__":
    image_dir = r"G:\My\sov\extract"  # Твій шлях до папки зображень
    output_file = os.path.join(image_dir, "brightness_comparison_combined.xlsx")

    # Перевірка, чи існує збережений DataFrame
    cache_file = os.path.join(image_dir, "brightness_data.csv")

    if os.path.exists(cache_file):
        df = pd.read_csv(cache_file)
        print("Data loaded from cache.")
    else:
        df = calculate_brightness_dataframe(image_dir)
        df.to_csv(cache_file, index=False)
        print("Brightness calculations completed and cached.")

    # Збереження у файл Excel
    save_brightness_excel(df, output_file)

    # Створення графіків
    create_brightness_plots(df)
