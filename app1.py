from flask import Flask, request, send_file, jsonify
from PIL import Image as PILImage, ExifTags
import io
import os

app = Flask(__name__)

class FileHelper:
    @staticmethod
    def get_extension(file_name):
        # Returns the file extension in uppercase
        return os.path.splitext(file_name)[1][1:].upper()

    @staticmethod
    def is_image(file_name):
        # Checks if the file is of an acceptable image type
        file_extension = FileHelper.get_extension(file_name)
        return file_extension in ['PNG', 'JPEG', 'JPG']

    @staticmethod
    def compress_file(input_stream, output_stream, file_name, rotation_angle=None):
        # Compresses and saves the file to the output stream
        file_extension = FileHelper.get_extension(file_name)
        
        if FileHelper.is_image(file_name):
            img = PILImage.open(input_stream)
            
            # Check and fix the orientation based on EXIF data
            ImageHelper.fix_orientation(img)  # Adjust the orientation based on EXIF data

            # Rotate image if a rotation angle is provided
            if rotation_angle is not None:
                img = img.rotate(rotation_angle, expand=True)
                
            # Resize image and save it
            ImageHelper.resize_image(img, output_stream, file_extension)
        else:
            output_stream.write(input_stream.read())  # Copy as-is if not an image
        
        output_stream.seek(0)  # Reset stream position after writing


class ImageHelper:
    @staticmethod
    def fix_orientation(img):
        """
        Adjusts the orientation of the image based on its EXIF Orientation tag.
        
        Parameters:
            img (PIL.Image): The Pillow image object to be corrected.
        
        Returns:
            PIL.Image: The image with corrected orientation.
        """
        try:
            # Retrieve the EXIF data and get the orientation tag
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation]=='Orientation':
                    break

            exif = img._getexif()
            if exif is not None:
                orientation = exif.get(orientation)
                if orientation == 3:
                    img = img.rotate(180, expand=True)  # Rotate 180 degrees
                elif orientation == 6:
                    img = img.rotate(270, expand=True)  # Rotate 270 degrees (clockwise)
                elif orientation == 8:
                    img = img.rotate(90, expand=True)   # Rotate 90 degrees (clockwise)
        except Exception as e:
            print(f"Error while fixing orientation: {e}")
        return img

    @staticmethod
    def resize_image(img, output_stream, file_extension, max_width=1080, max_height=1920):
        # Resize image to fit within max dimensions while preserving aspect ratio
        img.thumbnail((max_width, max_height))  # Resize to fit within the max width/height
        img.save(output_stream, format=file_extension)  # Save image to the output stream


    @staticmethod
    def get_blank_image(output_stream, width, height):
        # Creates and returns a blank white image
        img = PILImage.new('RGB', (width, height), color='white')
        img.save(output_stream, format='JPEG')  # Automatically saves as JPEG


@app.route('/compress', methods=['POST'])
def compress_image():
    # API endpoint to compress an uploaded image
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    file_name = file.filename
    input_stream = io.BytesIO(file.read())
    output_stream = io.BytesIO()

    # Get rotation angle if provided
    rotation_angle = request.form.get('rotation_angle', type=int)

    # Compress and handle image orientation
    FileHelper.compress_file(input_stream, output_stream, file_name, rotation_angle)
    output_stream.seek(0)

    return send_file(output_stream, as_attachment=True, download_name=f"compressed_{file_name}")


@app.route('/blank_image', methods=['GET'])
def blank_image():
    # API endpoint to generate a blank white image of specified dimensions
    width = int(request.args.get('width', 1080))
    height = int(request.args.get('height', 1920))
    output_stream = io.BytesIO()

    ImageHelper.get_blank_image(output_stream, width, height)
    output_stream.seek(0)

    return send_file(output_stream, as_attachment=True, download_name="blank_image.jpg")


if __name__ == '__main__':
    app.run(debug=True)
