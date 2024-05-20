from PIL import Image
import os

def calculate_compression_rate(image_path):
    # Load the image
    image = Image.open(image_path)
    width, height = image.size

    # Print the size of the image
    print("Image Size: {} x {}".format(width, height))

    # Calculate the uncompressed size (Assuming 24 bits means 3 bytes per pixel)
    uncompressed_size = width * height * 3  # in bytes
    
    # Get the file size
    compressed_size = os.path.getsize(image_path) 

    # Calculate the compression rate
    compression_rate = uncompressed_size / compressed_size
    return compression_rate


def adjust_brightness_YCbCr(image_path, brightness_increase=40):
    # Load and convert to YCbCr
    image = Image.open(image_path)
    ycbcr_image = image.convert('YCbCr')

    # Split the image into its components
    y, cb, cr = ycbcr_image.split()

    # Increase the Y component (brightness)
    y = y.point(lambda p: min(255, p + brightness_increase))  # Increase brightness by adding to Y component

    # Merge back and convert to RGB
    brighter_image = Image.merge('YCbCr', (y, cb, cr)).convert('RGB')
    return brighter_image

def modify_red_areas(image_path):
    # Load and convert to YCbCr
    image = Image.open(image_path)
    ycbcr_image = image.convert('YCbCr')
    y, cb, cr = ycbcr_image.split()

    # Modify Cr values where red is predominant
    def modify_cr(value):
        if value > 140:  # Assuming Cr > 140 indicates red shades
            return 0
        else:
            return value

    cr_modified = cr.point(modify_cr)

    # Merge back and convert to RGB
    modified_image = Image.merge('YCbCr', (y, cb, cr_modified)).convert('RGB')
    return modified_image

def jpeg_compression_simulation(image_path):
    # Load and convert to YCbCr
    image = Image.open(image_path)
    ycbcr_image = image.convert('YCbCr')
    y, cb, cr = ycbcr_image.split()

    # Downsample Cb and Cr by reducing resolution
    cb_downsampled = cb.resize((cb.width // 2, cb.height // 2),  Image.LANCZOS)
    cr_downsampled = cr.resize((cr.width // 2, cr.height // 2),  Image.LANCZOS)

    # Upsample to original size
    cb_upsampled = cb_downsampled.resize(cb.size, Image.LANCZOS)
    cr_upsampled = cr_downsampled.resize(cr.size,  Image.LANCZOS)
    # Merge and convert to RGB
    jpeg_simulated_image = Image.merge('YCbCr', (y, cb_upsampled, cr_upsampled)).convert('RGB')
    return jpeg_simulated_image

def fully_downsample_components(image_path):
    # Load and convert to YCbCr
    image = Image.open(image_path)
    ycbcr_image = image.convert('YCbCr')
    y, cb, cr = ycbcr_image.split()
    # Downsample all components
    y_downsampled = y.resize((y.width // 2, y.height // 2), Image.LANCZOS)
    cb_downsampled = cb.resize((cb.width // 2, cb.height // 2), Image.LANCZOS)
    cr_downsampled = cr.resize((cr.width // 2, cr.height // 2), Image.LANCZOS)
    # Upsample to original size
    y_upsampled = y_downsampled.resize(y.size, Image.LANCZOS)
    cb_upsampled = cb_downsampled.resize(cb.size, Image.LANCZOS)
    cr_upsampled = cr_downsampled.resize(cr.size, Image.LANCZOS)

    # Merge and convert to RGB
    fully_downsampled_image = Image.merge('YCbCr', (y_upsampled, cb_upsampled, cr_upsampled)).convert('RGB')
    return fully_downsampled_image
if __name__ == "__main__":
    input_image_path = 'D:\LongNguyen\Multi Media System\Lena.jpg'
    # Step 1: Calculate compression rate
    compression_rate = calculate_compression_rate(input_image_path)
    print("Compression Rate: {:.2f}".format(compression_rate))

    # Step 2: Adjust brightness
    brighter_image = adjust_brightness_YCbCr(input_image_path)
    brighter_image.show()  # Display the modified image

    # Step 3: Modify red areas
    modified_red_areas_image = modify_red_areas(input_image_path)
    modified_red_areas_image.show()  # Display the modified image
    # Step 4: JPEG compression simulation
    jpeg_compression_simulation_image = jpeg_compression_simulation(input_image_path)
    jpeg_compression_simulation_image.show()  # Display the modified image
    # Step 5: Fully downsample components
    fully_downsampled_image = fully_downsample_components(input_image_path)
    fully_downsampled_image.show()  # Display the modified image
