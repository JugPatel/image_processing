### **README for Flask Image Compression API with Pillow**

---

#### **Overview**
This project is a Flask-based API for compressing, rotating, and handling image files. It utilizes the **Pillow library** (a fork of the Python Imaging Library) to perform operations like resizing and correcting image orientations based on EXIF metadata.

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
- **Pillow**: For image manipulation.
- **io**: For handling input/output streams.

---

### **Setup Instructions**

1. **Create and Activate a Virtual Environment**:
   - **Create**:
     ```bash
     python -m venv venv
     ```
   - **Activate**:
     - **Windows**: 
       ```bash
       venv\Scripts\activate
       ```
     - **macOS/Linux**:
       ```bash
       source venv/bin/activate
       ```

2. **Install Dependencies**:
   ```bash
   pip install flask pillow
   ```

3. **Run the Application**:
   ```bash
   python app.py
   ```

4. **API Endpoints**:
   - **Compress Image**: `/compress` (POST)
   - **Generate Blank Image**: `/blank_image` (GET)

---

### **Using the Pillow Library**

Pillow provides an easy-to-use API for image manipulation. Here's how it's used in this project:

1. **EXIF Orientation Correction**:
   ```python
   exif = img._getexif()
   if exif:
       orientation = exif.get(274)  # 274 is the EXIF tag for Orientation
       if orientation == 3:
           img = img.rotate(180, expand=True)  # Upside down
       elif orientation == 6:
           img = img.rotate(270, expand=True)  # Clockwise 270
       elif orientation == 8:
           img = img.rotate(90, expand=True)   # Clockwise 90
   ```

2. **Image Rotation**:
   ```python
   img = img.rotate(rotation_angle, expand=True)  # Custom rotation if specified
   ```

3. **Image Resizing**:
   ```python
   img.thumbnail((new_width, new_height))  # Resize while maintaining aspect ratio
   ```

4. **Saving the Image**:
   ```python
   img.save(output_stream, format=file_extension)  # Save manipulated image to output stream
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
1. **Unexpected Errors with Pillow**:
   - Ensure Pillow is properly installed.
   - Verify the image format is supported (e.g., JPG, PNG).

2. **Image Orientation Not Corrected**:
   - Ensure the image contains valid EXIF data (not all images may have EXIF tags).
   - Check if the EXIF orientation tag is properly handled.

---

### **References**
- [Pillow Documentation](https://pillow.readthedocs.io/en/stable/)
- [ExifTags in Pillow](https://pillow.readthedocs.io/en/stable/releasenotes/7.0.0.html#support-for-exif-orientation)

---
