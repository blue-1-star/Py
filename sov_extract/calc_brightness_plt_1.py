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


def calculate_brightness_pil(image_path, lower_threshold=0, upper_threshold=255):
    """
    Обчислює середню яскравість зображення в градаціях сірого, враховуючи пороги.

    Параметри:
    image_path (str): Шлях до зображення.
    lower_threshold (int): Нижній поріг яскравості (0 за замовчуванням).
    upper_threshold (int): Верхній поріг яскравості (255 за замовчуванням).

    Повертає:
    dict: Середнє значення яскравості, кількість вилучених темних і світлих пікселів.
    """
    # Завантажуємо зображення
    img = Image.open(image_path)
    grayscale_img = img.convert('L')  # Перетворення в градації сірого
    
    # Перетворюємо зображення у numpy масив
    pixel_values = np.array(grayscale_img)
    
    # Фільтруємо пікселі за порогами
    filtered_pixels = pixel_values[(pixel_values >= lower_threshold) & (pixel_values <= upper_threshold)]
    
    # Обчислення статистики
    mean_brightness = np.mean(filtered_pixels) if len(filtered_pixels) > 0 else 0
    
    # Рахуємо кількість відкинутих пікселів
    dark_pixels_removed = np.sum(pixel_values < lower_threshold)
    bright_pixels_removed = np.sum(pixel_values > upper_threshold)

    # Повертаємо результат у вигляді словника
    return {
        'mean_brightness': mean_brightness,
        'dark_pixels_removed': dark_pixels_removed,
        'bright_pixels_removed': bright_pixels_removed,
        'total_pixels': pixel_values.size
    }

def calculate_brightness_color(image_path, lower_threshold=0, upper_threshold=255):
    """
    Обчислює середню яскравість кольорового зображення, враховуючи пороги для кожного каналу.

    Параметри:
    image_path (str): Шлях до зображення.
    lower_threshold (int): Нижній поріг яскравості (0 за замовчуванням).
    upper_threshold (int): Верхній поріг яскравості (255 за замовчуванням).

    Повертає:
    dict: Середнє значення яскравості, кількість вилучених темних і світлих пікселів.
    """
    # Завантажуємо зображення
    img = Image.open(image_path)
    
    # Перетворюємо зображення у numpy масив
    pixel_values = np.array(img)
    
    # Обчислюємо яскравість для кожного пікселя за формулою
    brightness_values = 0.299 * pixel_values[:, :, 0] + 0.587 * pixel_values[:, :, 1] + 0.114 * pixel_values[:, :, 2]
    
    # Фільтруємо пікселі за порогами
    filtered_pixels = brightness_values[(brightness_values >= lower_threshold) & (brightness_values <= upper_threshold)]
    
    # Обчислення статистики
    mean_brightness = np.mean(filtered_pixels) if len(filtered_pixels) > 0 else 0
    
    # Рахуємо кількість відкинутих пікселів
    dark_pixels_removed = np.sum(brightness_values < lower_threshold)
    bright_pixels_removed = np.sum(brightness_values > upper_threshold)

    # Повертаємо результат у вигляді словника
    return {
        'mean_brightness': mean_brightness,
        'dark_pixels_removed': dark_pixels_removed,
        'bright_pixels_removed': bright_pixels_removed,
        'total_pixels': brightness_values.size
    }


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
def calculate_brightness_dataframe(image_dir, lower_threshold):
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.orf', '.jpg', '.jpeg'))]

    # Список для зберігання результатів
    results = []
    
    # Проходимо по всіх файлах та обчислюємо яскравість
    for img_file in image_files:
        img_path = os.path.join(image_dir, img_file)
        
        # Обчислюємо яскравість обома методами
        brightness_pil = calculate_brightness_pil(img_path, lower_threshold)
        brightness_color = calculate_brightness_color(img_path, lower_threshold)
        
        file_format = "ORF" if img_file.lower().endswith('.orf') else "JPEG"
        
        results.append({
            "Filename": img_file,
            "Format": file_format,
            "Brightness_PIL": brightness_pil['mean_brightness'],
            "Brightness_Color": brightness_color['mean_brightness'],
            "Removed_pix_pil" : brightness_pil['dark_pixels_removed'],
            "Removed_pix_col" : brightness_color['dark_pixels_removed']
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
def save_brightness_excel(df, output_file, lower_threshold):
    # Створюємо Excel-файл з трьома листами
    summary = { 
        'date'  : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'files' : len(df),
        'lower_threshold' : lower_threshold
    }
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Лист 1: Оригінальний порядок
        df.sort_values(['Filename'], inplace=True)
        df.to_excel(writer, index=False, sheet_name='Original Order')
        summary.to_excel(writer, sheet_name='Original Order', index=False, startrow=len(df) + 2)
        # Лист 2: Сортовані по яскравості всередині груп (PIL)
        df.sort_values(['Format', 'Rank_in_Group_PIL'], inplace=True)
        df.to_excel(writer, index=False, sheet_name='Sorted by Brightness_PIL')
        summary.to_excel(writer, sheet_name='Sorted by Brightness_PIL', index=False, startrow=len(df) + 2)

        # Лист 3: Сортовані по яскравості всередині груп (Color)
        df.sort_values(['Format', 'Rank_in_Group_Color'], inplace=True)
        df.to_excel(writer, index=False, sheet_name='Sorted by Brightness_Color')
        summary.to_excel(writer, sheet_name='Sorted by Brightness_Color', index=False, startrow=len(df) + 2)

        # Лист 4: Глобальне сортування по яскравості (PIL)
        df.sort_values(['Rank_Global_PIL'], inplace=True)
        df.to_excel(writer, index=False, sheet_name='Global Sorted by PIL')
        summary.to_excel(writer, sheet_name='Global Sorted by PIL', index=False, startrow=len(df) + 2)
        
        # Лист 5: Глобальне сортування по яскравості (Color)
        df.sort_values(['Rank_Global_Color'], inplace=True)
        df.to_excel(writer, index=False, sheet_name='Global Sorted by Color')
        summary.to_excel(writer, sheet_name='Global Sorted by Color', index=False, startrow=len(df) + 2)

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
    output_path = os.path.join(image_dir, "comparision_orf_1.pdf")
    plt.savefig(output_path,  format="pdf", dpi=300, bbox_inches='tight')  # Рекомендується встановити високий dpi для якості
    plt.show()
    plt.close()
# Виконання коду
if __name__ == "__main__":
    image_dir = r"G:\My\sov\extract"  # Твій шлях до папки зображень
    output_file = os.path.join(image_dir, "brightness_comparison_comb.xlsx")
    lower_threshold = 1
    # Перевірка, чи існує збережений DataFrame
    cache_file = os.path.join(image_dir, "brightness_data.csv")

    if os.path.exists(cache_file):
        df = pd.read_csv(cache_file)
        print("Data loaded from cache.")
    else:
        df = calculate_brightness_dataframe(image_dir, lower_threshold)
        df.to_csv(cache_file, index=False)
        print("Brightness calculations completed and cached.")

    # Збереження у файл Excel
    save_brightness_excel(df, output_file)

    # Створення графіків
    create_brightness_plots(df)
