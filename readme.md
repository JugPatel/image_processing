### README for Flask Image Compression API with Wand (ImageMagick)

---

#### **Overview**
This project is a Flask-based API for compressing, rotating, and handling image files. It utilizes the **Wand library**, a Python wrapper for ImageMagick, to perform operations like resizing and correcting image orientations based on EXIF metadata.

---

### **Key Features**
1. **Image Orientation Correction**:
   - Automatically adjusts image orientation using EXIF metadata to ensure the correct display.
   
2. **Rotation**:
   - Provides an option to rotate images by a specified angle.

3. **Compression**:
   - Compresses images while maintaining their quality within specified dimensions.

4. **Blank Image Generator**:
   - Creates blank images of user-defined dimensions.

---

### **Dependencies**
- **Flask**: For building the API endpoints.
- **Wand**: For image manipulation (requires ImageMagick installed).
- **io**: For handling input/output streams.

---

### **Setup Instructions**

1. **Install Dependencies**:
   ```bash
   pip install flask Wand
   ```

2. **Install ImageMagick**:
   - **Windows**: Download and install from [ImageMagick's official website](https://imagemagick.org/script/download.php).
   - Make sure the `MAGICK_HOME` environment variable is set, and the ImageMagick binaries are in your `PATH`.

3. **Run the Application**:
   ```bash
   python app.py
   ```

4. **API Endpoints**:
   - **Compress Image**: `/compress` (POST)
   - **Generate Blank Image**: `/blank_image` (GET)

---

### **Using the Wand Library**

The Wand library is a powerful tool for image manipulation, built on top of ImageMagick. Here’s how it’s used in this project:

1. **EXIF Orientation Correction**:
   ```python
   exif = img.metadata.get('exif:Orientation')  # Extract orientation
   if exif == '3':
       img.rotate(degree=180)  # Upside down
   elif exif == '6':
       img.rotate(degree=270)  # Clockwise 270
   elif exif == '8':
       img.rotate(degree=90)   # Clockwise 90
   ```

2. **Image Rotation**:
   ```python
   img.rotate(degree=rotation_angle)  # Custom rotation if specified
   ```

3. **Image Resizing**:
   ```python
   img.resize(width=new_width, height=new_height)  # Resize while maintaining aspect ratio
   ```

4. **Saving the Image**:
   ```python
   img.save(file=output_stream)  # Save manipulated image to output stream
   ```

---

### **Code Explanation**

#### **Compress Image Logic**
- **Input**: A file stream containing an image.
- **Process**:
  - Identify if the file is an image.
  - Correct its orientation using EXIF data.
  - Resize it to specified dimensions while maintaining aspect ratio.
  - Optionally rotate the image.
- **Output**: A compressed image saved to the output stream.

#### **Blank Image Generator**
- **Input**: Width and height via query parameters.
- **Process**: Creates a blank white image of the specified dimensions.
- **Output**: A blank image file.

---

### **API Examples**

#### **Compress Image**
```bash
curl -X POST -F "file=@input_image.jpg" -F "rotation_angle=90" http://127.0.0.1:5000/compress -o compressed_image.jpg
```

#### **Generate Blank Image**
```bash
curl "http://127.0.0.1:5000/blank_image?width=500&height=500" -o blank_image.jpg
```

---

### **Troubleshooting**
1. **ImageMagick Not Found**:
   - Ensure ImageMagick is installed and added to your system's `PATH`.
   - Verify using: `magick --version`.

2. **Unexpected Errors with Wand**:
   - Check if `MAGICK_HOME` is properly set.
   - Update to the latest Wand and ImageMagick versions.

---

### **References**
- [Wand Documentation](https://docs.wand-py.org/en/stable/)
- [ImageMagick Official Website](https://imagemagick.org/)

---