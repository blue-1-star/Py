import cv2
import numpy as np
import os

def region_growing_fixed_seed(img, seed, thresh, display_interval=100):
    """
    Region growing algorithm that compares each pixel to the initial seed value.
    
    Parameters:
      img             - Grayscale image.
      seed            - Coordinates of the seed point (x, y).
      thresh          - Threshold for allowable intensity difference.
      display_interval- Number of iterations between screen updates.
      
    Returns:
      mask - Binary mask of the grown region.
    """
    h, w = img.shape
    mask = np.zeros((h, w), np.uint8)
    seed_value = int(img[seed[1], seed[0]])  # Extract pixel value at (x, y)
    seed_list = [seed]
    mask[seed[1], seed[0]] = 255
    iteration = 0
    exit_flag = False

    # Create a resizable window for process display
    process_window = "Process Region Growing"
    cv2.namedWindow(process_window, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(process_window, 800, 600)

    while seed_list and not exit_flag:
        x, y = seed_list.pop(0)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and mask[ny, nx] == 0:
                    # Compare new pixel intensity with the initial seed value
                    if abs(int(img[ny, nx]) - seed_value) < thresh:
                        mask[ny, nx] = 255
                        seed_list.append((nx, ny))
        iteration += 1
        if iteration % display_interval == 0:
            cv2.imshow(process_window, mask)
            # Check if ESC is pressed during region growing to exit early
            if cv2.waitKey(1) == 27:
                print("ESC pressed during region growing. Terminating process early.")
                exit_flag = True
    return mask

# Load the input image
image_path = r"G:\My\sov\extract\Spores\original_img\worst\test\A_best_4x_11.png"  # Replace with your image path
img_color = cv2.imread(image_path)
if img_color is None:
    print("Error loading image!")
    exit()

# Convert the image to grayscale
img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

# Mouse click event handler
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        seed = (x, y)
        print("Seed point selected:", seed)
        seg_mask = region_growing_fixed_seed(img_gray, seed, thresh=15, display_interval=200)
        
        # Create and show final mask window
        final_mask_window = "Final Mask"
        cv2.namedWindow(final_mask_window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(final_mask_window, 800, 600)
        cv2.imshow(final_mask_window, seg_mask)
        
        # Create overlay on original image
        overlay = img_color.copy()
        overlay[seg_mask == 255] = (0, 0, 255)
        overlay_window = "Mask Overlay"
        cv2.namedWindow(overlay_window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(overlay_window, 800, 600)
        cv2.imshow(overlay_window, overlay)
        
        # Save final mask and overlay in the same directory as the source image
        base, ext = os.path.splitext(image_path)
        mask_filename = base + "_mask.png"
        overlay_filename = base + "_overlay.png"
        cv2.imwrite(mask_filename, seg_mask)
        cv2.imwrite(overlay_filename, overlay)
        print("Saved mask to:", mask_filename)
        print("Saved overlay to:", overlay_filename)
        
        # Wait for ESC to exit (if not already pressed)
        print("Press ESC in any window to exit.")
        while True:
            if cv2.waitKey(1) == 27:
                break
        cv2.destroyAllWindows()

# Create a resizable window with an English title for seed selection
select_window = "Select Seed Point"
cv2.namedWindow(select_window, cv2.WINDOW_NORMAL)
cv2.resizeWindow(select_window, 800, 600)
cv2.imshow(select_window, img_color)
cv2.setMouseCallback(select_window, click_event)

print("Click the left mouse button on the spore to start the region growing algorithm.")
# Wait indefinitely until a key is pressed (ESC in the final waiting loop in click_event will break out)
cv2.waitKey(0)
cv2.destroyAllWindows()
