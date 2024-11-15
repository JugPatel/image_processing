from wand.image import Image

def fix_image_orientation(image_path, output_path):
    # Open the image using Wand (ImageMagick)
    with Image(filename=image_path) as img:
        # Check if the image has EXIF data (orientation)
        exif = img.metadata.get('exif:Orientation')  # Check EXIF orientation

        # Rotate based on EXIF orientation
        if exif == '3':
            img.rotate(degree=180)
        elif exif == '6':
            img.rotate(degree=270)  # Rotate 270 degrees clockwise
        elif exif == '8':
            img.rotate(degree=90)   # Rotate 90 degrees clockwise

        # Save the image with the correct orientation
        img.save(filename=output_path)

# Example usage
fix_image_orientation("input_image.jpg", "output_image.jpg")
