// Fiji Macro: "Analyze Green Pixels with Scale and Excel Export"
macro "Analyze Green Pixels Advanced" {
    // Указываем папку с изображениями
    img_folder = getDirectory("Выберите папку с изображениями");
    list_files_Fiji = getFileList(img_folder);
    
    // Проверяем наличие файла масштабов
    scale_file = img_folder + "file_list.xlsx";
    has_scale = File.exists(scale_file);
    
    // Создаём Excel-файл для результатов
    output_path = img_folder + "Green_Pixel_Analysis_Results.xlsx";
    header = "Image Name\tGreen Pixels\tTotal Pixels\tPercentage (%)\tScale (pix/mm)\tArea (mm²)";
    File.saveString(header, output_path);
    
    // Параметры Color Threshold (HSV-диапазон)
    hue_range = "35-85";
    saturation_range = "50-255";
    brightness_range = "50-255";
    
    // Загружаем данные масштаба если есть
    if (has_scale) {
        Table.open(scale_file);
        Table.rename("scale_data");
    }
    
    // Обрабатываем каждое изображение
    for (i = 0; i < list_files_Fiji.length; i++) {
        file_name = list_files_Fiji[i];
        if (endsWith(file_name, ".jpg") || endsWith(file_name, ".png")) {
            // Получаем имя файла без расширения
            file_name_no_ext = replace(file_name, ".jpg", "");
            file_name_no_ext = replace(file_name_no_ext, ".png", "");
            
            // Получаем масштаб если есть
            scale_pix_per_mm = 0;
            if (has_scale) {
                for (row = 0; row < Table.size; row++) {
                    if (Table.getString("File Name", row).contains(file_name_no_ext)) {
                        scale_pix_per_mm = Table.get("Scale pix/mm", row);
                        break;
                    }
                }
            }
            
            // Открываем изображение
            img_path = img_folder + file_name;
            open(img_path);
            title = getTitle();
            
            // Создаем HSB стэк
            run("HSB Stack");
            
            // Применяем Color Threshold через специальный вызов
            call("ij.plugin.frame.ColorThresholder.run", 
                "threshold", 
                "Hue=" + hue_range + 
                " Saturation=" + saturation_range + 
                " Brightness=" + brightness_range);
            
            // Преобразуем в маску
            run("Convert to Mask");
            
            // Анализируем частицы
            run("Analyze Particles...", "display summarize add");
            
            // Получаем результаты
            green_pixels = ParticleAnalyzer.getNParticles() * ParticleAnalyzer.getParticleSize();
            if (isNaN(green_pixels)) green_pixels = 0;
            total_pixels = getWidth() * getHeight();
            percentage = (green_pixels / total_pixels) * 100;
            
            // Вычисляем площадь в мм² если есть масштаб
            area_mm2 = 0;
            if (scale_pix_per_mm > 0) {
                area_mm2 = green_pixels / (scale_pix_per_mm * scale_pix_per_mm);
            }
            
            // Записываем результаты
            result_line = file_name + "\t" + green_pixels + "\t" + 
                         total_pixels + "\t" + d2s(percentage,2) + "\t";
            
            if (has_scale) {
                result_line += scale_pix_per_mm + "\t" + d2s(area_mm2,4);
            } else {
                result_line += "N/A\tN/A";
            }
            
            File.append(result_line, output_path);
            
            // Закрываем окна
            selectWindow(title);
            close();
            close("HSB Stack");
        }
    }
    
    // Закрываем таблицу масштабов если была открыта
    if (has_scale) {
        close("scale_data");
    }
    
    // Открываем результаты в Excel
    if (File.exists(output_path)) {
        open(output_path);
    }
    
    print("Анализ завершён! Результаты сохранены в: " + output_path);
}