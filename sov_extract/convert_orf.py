from PIL import Image
import os
input_folder = r"G:\My\sov\extract\ORF\A" 
output_folder = r"G:\My\sov\extract\ORF\A" 
def convert_orf_to_png(input_folder, output_folder):
    for file in os.listdir(input_folder):
        if file.endswith(".ORF"):
            
            input_path = os.path.join(input_folder, file)
            output_path = os.path.join(output_folder, os.path.splitext(file)[0] + ".png")
            
            try:
                img = Image.open(input_path)
                img.save(output_path, quality=95)  # Настройка качества
                print(f"Converted {input_path} to {output_path}")
            except Exception as e:
                print(f"Error processing {input_path}: {e}")

# Замените 'input_folder' и 'output_folder' на ваши пути
convert_orf_to_png(input_folder, output_folder)
