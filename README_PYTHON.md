# WAZ GIF Maker Pro - Desktop Application

A professional desktop application for creating animated GIFs with text overlays, built with Python and PyQt5.

## Features

✨ **Easy to Use Interface**
- Modern, intuitive GUI built with PyQt5
- Drag-and-drop file upload support
- Visual thumbnail preview with reordering capability

🎨 **Customization Options**
- Adjustable frame delay (50ms - 5000ms)
- Text overlay with custom positioning (Top/Center/Bottom)
- Color picker for text customization
- Multiple font size options (24px - 96px)

🌓 **Dark Mode**
- Toggle between light and dark themes for comfortable viewing

⚡ **High Performance**
- Fast GIF generation using Pillow
- Real-time preview of animation
- Optimized image processing

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Step 1: Install Dependencies

Open a terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install:
- PyQt5 (GUI framework)
- Pillow (Image processing)

### Step 2: Run the Application

```bash
python gif_maker_app.py
```

## Usage

### Creating a GIF

1. **Upload Images**
   - Click the "Browse Files" button or drag-and-drop images into the upload area
   - Supports PNG, JPG, and JPEG formats
   - Upload multiple images at once

2. **Reorder Images** (Optional)
   - Drag and drop thumbnails to change the order of frames

3. **Configure Settings**
   - **Frame Delay**: Set the time between frames in milliseconds (default: 200ms)
   - **Text Overlay**: Add optional text to appear on all frames
   - **Text Color**: Choose the color for your text
   - **Font Size**: Select from Small (24px) to Huge (96px)
   - **Text Position**: Place text at Top, Center, or Bottom

4. **Preview Animation**
   - Click "Preview" button to see how your GIF will look
   - The preview will cycle through your images with the specified delay

5. **Create GIF**
   - Click "Create GIF" button to generate the final GIF
   - A success message will appear when done

6. **Download**
   - Click "Download GIF" button
   - Choose where to save your GIF file

## Features Comparison

### Web Version → Desktop Version

| Feature | Web | Desktop |
|---------|-----|---------|
| Drag & Drop Upload | ✅ | ✅ |
| Image Reordering | ✅ | ✅ |
| Frame Delay Control | ✅ | ✅ |
| Text Overlay | ✅ | ✅ |
| Color Picker | ✅ | ✅ |
| Font Size Options | ✅ | ✅ |
| Text Positioning | ✅ | ✅ |
| Dark Mode | ✅ | ✅ |
| Preview Animation | ✅ | ✅ |
| Offline Support | ❌ | ✅ |
| No Browser Required | ❌ | ✅ |
| Native Performance | ❌ | ✅ |

## Keyboard Shortcuts

- **Ctrl+O**: Open file browser (when focused on window)
- **Drag & Drop**: Works on main window and drop area

## Troubleshooting

### Issue: "No module named PyQt5"
**Solution**: Run `pip install PyQt5`

### Issue: "No module named PIL"
**Solution**: Run `pip install Pillow`

### Issue: Font not found warning
**Solution**: The app will use the default system font if Arial is not available. This is normal and won't affect functionality.

### Issue: GIF creation fails
**Solution**: 
- Check that all images are valid and not corrupted
- Try using fewer images or smaller image sizes
- Ensure you have write permissions in the directory

## System Requirements

- **Operating System**: Windows 10/11, macOS 10.13+, or Linux
- **RAM**: 2GB minimum, 4GB recommended
- **Python**: Version 3.7 or higher
- **Disk Space**: 100MB for application and dependencies

## Development

### Project Structure

```
GIF/
├── gif_maker_app.py      # Main application file
├── requirements.txt      # Python dependencies
├── README_PYTHON.md      # This file
└── [image files]         # Your GIF frames
```

### Building an Executable (Optional)

To create a standalone executable that doesn't require Python:

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Build the executable:
```bash
pyinstaller --onefile --windowed --name="GIF_Maker_Pro" gif_maker_app.py
```

The executable will be in the `dist/` folder.

## Credits

Created by WAZ
- Converted from web application to desktop application
- Built with PyQt5 and Pillow

## License

Free to use for personal and commercial projects.

## Support

For issues or questions, please check the troubleshooting section above.

---

**Enjoy creating amazing GIFs! 🎬✨**
