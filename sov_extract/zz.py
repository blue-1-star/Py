for idx, img_file in enumerate(image_files):
    # цикл по всем файлам с изображениями
        img_path = os.path.join(image_dir, img_file)
        img = process_image(img_path)  # обработка .orf либо других расширений
        rgb_array = np.array(img)  # Преобразуем изображение обратно в NumPy-массив
        hsv_array = rgb_to_hsv(rgb_array)
        hue_channel = hsv_array[:, :, 0]  # Оттенок
        saturation_channel = hsv_array[:, :, 1]  # Насыщенность
        value_channel = hsv_array[:, :, 2]  # Яркость
        # Вычисляем гистограммы
        hist_hue, hist_saturation, hist_value, bin_edges = get_hsv_histograms(hsv_array)
        
        brightness_pil = calculate_brightness_pil(img_path, lower_threshold)
        brightness_square = calculate_brightness_with_area(img_path, shape ='rectangle',  size = size, lower_threshold=lower_threshold)
        brightness_circle = calculate_brightness_with_area(img_path, shape ='ellipse', size=size, lower_threshold=lower_threshold)
        
        # тут должна быть адаптированная функция  !!!!
        plot_hist(hue_channel, output_file, shape, size)
        #       
        avg_color_ellipse = calculate_color_with_area(img_path, 'ellipse', size=size, lower_threshold=lower_threshold)

        # Основной словарь результатов
        result_row = {
            "Filename": img_file,
            "Substrate": subst[idx],
            "Bright_P_mean": brightness_pil['mean_brightness'],
            "Bright_P_std": brightness_pil['stdv_brightness'],
            "Bright_Sq_m": brightness_square['mean_brightness'],
            "Bright_Sq_s": brightness_square['stdv_brightness'],
            "Bright_Cl_m": brightness_circle['mean_brightness'],
            "Bright_Cl_s": brightness_circle['stdv_brightness'],
            "color_ellips": avg_color_ellipse,
            "Hist_hue_m" :  np.mean(hist_hue),
            "Hist_sat_m" :  np.mean(hist_saturation),
            "Hist_value_m": np.mean(hist_value),
            "Hist_hue_s" :  np.std(hist_hue),
            "Hist_sat_s" :  np.std(hist_saturation),
            "Hist_value_s": np.std(hist_value),
            "Size": f"fig({sx} x {sy})"
        }
        results.append(result_row)
         
df = pd.DataFrame(results)