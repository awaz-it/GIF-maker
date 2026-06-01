"""
WAZ GIF Maker Pro - Desktop Application
A professional GIF creation tool with drag-and-drop support and text overlays
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QFileDialog,
                             QSpinBox, QLineEdit, QColorDialog, QComboBox,
                             QScrollArea, QGridLayout, QFrame, QMessageBox,
                             QCheckBox, QGroupBox, QShortcut)
from PyQt5.QtCore import Qt, QSize, QTimer, pyqtSignal, QMimeData
from PyQt5.QtGui import QPixmap, QImage, QDrag, QPainter, QFont, QColor, QPalette, QIcon, QKeySequence
from PIL import Image, ImageDraw, ImageFont
import io


class DraggableLabel(QLabel):
    """Custom QLabel that supports drag and drop for reordering"""
    position_changed = pyqtSignal(int, int)
    
    def __init__(self, index, parent=None):
        super().__init__(parent)
        self.index = index
        self.setAcceptDrops(True)
        self.setScaledContents(True)
        self.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.setLineWidth(3)
        self.setStyleSheet("""
            border: 3px solid #cbd5e1; 
            border-radius: 12px;
            background: white;
        """)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(str(self.index))
            drag.setMimeData(mime_data)
            drag.exec_(Qt.MoveAction)
            
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
            self.setStyleSheet("""
                border: 3px solid #3b82f6; 
                border-radius: 12px;
                background: #dbeafe;
            """)
        else:
            event.ignore()
            
    def dragLeaveEvent(self, event):
        self.setStyleSheet("""
            border: 3px solid #cbd5e1; 
            border-radius: 12px;
            background: white;
        """)
        
    def dropEvent(self, event):
        source_index = int(event.mimeData().text())
        self.position_changed.emit(source_index, self.index)
        self.setStyleSheet("""
            border: 3px solid #cbd5e1; 
            border-radius: 12px;
            background: white;
        """)


class GIFMakerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image_paths = []
        self.preview_labels = []
        self.preview_timer = QTimer()
        self.preview_index = 0
        self.dark_mode = False
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('WAZ GIF Maker Pro')
        self.setAcceptDrops(True)
        # Start in fullscreen mode
        self.showFullScreen()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Title section
        title_label = QLabel('Create Stunning Animated GIFs')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Segoe UI', 28, QFont.Bold))
        main_layout.addWidget(title_label)
        
        subtitle_label = QLabel('Professional GIF creation tool with advanced customization')
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setFont(QFont('Segoe UI', 11))
        main_layout.addWidget(subtitle_label)
        
        # Upload section
        upload_group = self.create_upload_section()
        main_layout.addWidget(upload_group)
        
        # Preview thumbnails
        self.preview_scroll = QScrollArea()
        self.preview_scroll.setWidgetResizable(True)
        self.preview_scroll.setMinimumHeight(200)
        self.preview_scroll.setMaximumHeight(200)
        self.preview_widget = QWidget()
        self.preview_layout = QGridLayout(self.preview_widget)
        self.preview_layout.setSpacing(15)
        self.preview_scroll.setWidget(self.preview_widget)
        main_layout.addWidget(self.preview_scroll)
        
        # Drag hint
        drag_hint = QLabel('🔄 Drag thumbnails to reorder images')
        drag_hint.setAlignment(Qt.AlignCenter)
        drag_hint.setFont(QFont('Segoe UI', 10))
        main_layout.addWidget(drag_hint)
        
        # Controls section
        controls_group = self.create_controls_section()
        main_layout.addWidget(controls_group)
        
        # Preview section
        preview_group = self.create_preview_section()
        main_layout.addWidget(preview_group)
        
        # Add ESC key shortcut to exit fullscreen
        self.esc_shortcut = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.esc_shortcut.activated.connect(self.toggle_fullscreen)
        
        # Apply light theme by default
        self.apply_theme()
        
    def create_header(self):
        """Create header with logo and dark mode toggle"""
        header = QFrame()
        header.setMinimumHeight(70)
        header.setMaximumHeight(70)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(30, 10, 30, 10)
        
        # Logo
        logo_label = QLabel('🎬 WAZ GIF Maker Pro')
        logo_label.setFont(QFont('Segoe UI', 18, QFont.Bold))
        header_layout.addWidget(logo_label)
        
        header_layout.addStretch()
        
        # Dark mode toggle with modern switch design
        toggle_container = QWidget()
        toggle_layout = QHBoxLayout(toggle_container)
        toggle_layout.setContentsMargins(0, 0, 0, 0)
        toggle_layout.setSpacing(10)
        
        mode_label = QLabel('☀️ Light')
        mode_label.setFont(QFont('Segoe UI', 10))
        toggle_layout.addWidget(mode_label)
        
        self.dark_mode_checkbox = QCheckBox()
        self.dark_mode_checkbox.setFixedSize(60, 30)
        self.dark_mode_checkbox.stateChanged.connect(self.toggle_dark_mode)
        toggle_layout.addWidget(self.dark_mode_checkbox)
        
        self.mode_label_dark = QLabel('🌙 Dark')
        self.mode_label_dark.setFont(QFont('Segoe UI', 10))
        toggle_layout.addWidget(self.mode_label_dark)
        
        header_layout.addWidget(toggle_container)
        
        return header
        
    def create_upload_section(self):
        """Create file upload section"""
        group = QGroupBox()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Drop area
        self.drop_label = QLabel('☁️\n\nDrop your images here or click to browse\n\nSupports PNG, JPG, JPEG')
        self.drop_label.setAlignment(Qt.AlignCenter)
        self.drop_label.setMinimumHeight(180)
        self.drop_label.setFont(QFont('Segoe UI', 12))
        self.drop_label.mousePressEvent = lambda e: self.browse_files()
        layout.addWidget(self.drop_label)
        
        # Browse button
        browse_btn = QPushButton('📁  Browse Files')
        browse_btn.setFont(QFont('Segoe UI', 11, QFont.Bold))
        browse_btn.setMinimumHeight(45)
        browse_btn.setCursor(Qt.PointingHandCursor)
        browse_btn.clicked.connect(self.browse_files)
        layout.addWidget(browse_btn)
        
        group.setLayout(layout)
        return group
        
    def create_controls_section(self):
        """Create controls for GIF settings"""
        group = QGroupBox()
        layout = QGridLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Frame Delay
        delay_label = QLabel('⏱️  Frame Delay (ms)')
        delay_label.setFont(QFont('Segoe UI', 11, QFont.Bold))
        layout.addWidget(delay_label, 0, 0)
        self.delay_spin = QSpinBox()
        self.delay_spin.setRange(50, 5000)
        self.delay_spin.setValue(200)
        self.delay_spin.setMinimumHeight(40)
        self.delay_spin.setFont(QFont('Segoe UI', 10))
        layout.addWidget(self.delay_spin, 0, 1)
        
        # Text Overlay
        text_label = QLabel('📝  Text Overlay')
        text_label.setFont(QFont('Segoe UI', 11, QFont.Bold))
        layout.addWidget(text_label, 1, 0)
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText('Add text to your GIF')
        self.text_input.setMinimumHeight(40)
        self.text_input.setFont(QFont('Segoe UI', 10))
        layout.addWidget(self.text_input, 1, 1)
        
        # Text Color
        color_label = QLabel('🎨  Text Color')
        color_label.setFont(QFont('Segoe UI', 11, QFont.Bold))
        layout.addWidget(color_label, 2, 0)
        self.color_btn = QPushButton('Choose Color')
        self.color_btn.setMinimumHeight(40)
        self.color_btn.setFont(QFont('Segoe UI', 10, QFont.Bold))
        self.color_btn.setCursor(Qt.PointingHandCursor)
        self.text_color = QColor(255, 0, 0)
        self.color_btn.clicked.connect(self.choose_color)
        layout.addWidget(self.color_btn, 2, 1)
        
        # Font Size
        font_label = QLabel('🔤  Font Size')
        font_label.setFont(QFont('Segoe UI', 11, QFont.Bold))
        layout.addWidget(font_label, 3, 0)
        self.font_combo = QComboBox()
        self.font_combo.addItems(['24px - Small', '36px - Medium', '48px - Large', 
                                  '64px - XL', '72px - XXL', '96px - Huge'])
        self.font_combo.setCurrentIndex(2)
        self.font_combo.setMinimumHeight(40)
        self.font_combo.setFont(QFont('Segoe UI', 10))
        layout.addWidget(self.font_combo, 3, 1)
        
        # Text Position
        pos_label = QLabel('📍  Text Position')
        pos_label.setFont(QFont('Segoe UI', 11, QFont.Bold))
        layout.addWidget(pos_label, 4, 0)
        self.position_combo = QComboBox()
        self.position_combo.addItems(['Top', 'Center', 'Bottom'])
        self.position_combo.setMinimumHeight(40)
        self.position_combo.setFont(QFont('Segoe UI', 10))
        layout.addWidget(self.position_combo, 4, 1)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        
        preview_btn = QPushButton('👁️  Preview Animation')
        preview_btn.setFont(QFont('Segoe UI', 12, QFont.Bold))
        preview_btn.setMinimumHeight(50)
        preview_btn.setCursor(Qt.PointingHandCursor)
        preview_btn.clicked.connect(self.preview_animation)
        btn_layout.addWidget(preview_btn)
        
        create_btn = QPushButton('✨  Create GIF')
        create_btn.setFont(QFont('Segoe UI', 12, QFont.Bold))
        create_btn.setMinimumHeight(50)
        create_btn.setCursor(Qt.PointingHandCursor)
        create_btn.clicked.connect(self.create_gif)
        btn_layout.addWidget(create_btn)
        
        layout.addLayout(btn_layout, 5, 0, 1, 2)
        
        group.setLayout(layout)
        return group
        
    def create_preview_section(self):
        """Create preview section"""
        group = QGroupBox()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        title = QLabel('▶️  Preview')
        title.setFont(QFont('Segoe UI', 16, QFont.Bold))
        layout.addWidget(title)
        
        self.preview_label = QLabel('Your GIF preview will appear here')
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumHeight(400)
        self.preview_label.setFont(QFont('Segoe UI', 11))
        layout.addWidget(self.preview_label)
        
        self.download_btn = QPushButton('💾  Download GIF')
        self.download_btn.setFont(QFont('Segoe UI', 12, QFont.Bold))
        self.download_btn.setMinimumHeight(50)
        self.download_btn.setCursor(Qt.PointingHandCursor)
        self.download_btn.clicked.connect(self.download_gif)
        self.download_btn.hide()
        layout.addWidget(self.download_btn)
        
        group.setLayout(layout)
        return group
        
    def toggle_dark_mode(self, state):
        """Toggle between light and dark theme"""
        self.dark_mode = state == Qt.Checked
        self.apply_theme()
        
    def toggle_fullscreen(self):
        """Toggle between fullscreen and normal window mode"""
        if self.isFullScreen():
            self.showNormal()
            self.showMaximized()
        else:
            self.showFullScreen()
        
    def apply_theme(self):
        """Apply light or dark theme with professional styling"""
        if self.dark_mode:
            # Dark Mode - Modern Professional Design
            self.setStyleSheet("""
                QMainWindow {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #0f172a, stop:1 #1e293b);
                }
                QLabel {
                    color: #e2e8f0;
                }
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #1e293b, stop:1 #334155);
                    border-radius: 12px;
                    border: 1px solid #475569;
                }
                QGroupBox {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #1e293b, stop:1 #0f172a);
                    border: 2px solid #334155;
                    border-radius: 16px;
                    padding: 10px;
                }
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #3b82f6, stop:1 #2563eb);
                    color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 12px 24px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #60a5fa, stop:1 #3b82f6);
                }
                QPushButton:pressed {
                    background: #1d4ed8;
                }
                QLineEdit, QSpinBox, QComboBox {
                    background: #0f172a;
                    color: #e2e8f0;
                    border: 2px solid #475569;
                    border-radius: 8px;
                    padding: 10px;
                    selection-background-color: #3b82f6;
                }
                QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
                    border: 2px solid #3b82f6;
                    background: #1e293b;
                }
                QComboBox::drop-down {
                    border: none;
                    width: 30px;
                }
                QComboBox::down-arrow {
                    image: none;
                    border-left: 5px solid transparent;
                    border-right: 5px solid transparent;
                    border-top: 5px solid #e2e8f0;
                    margin-right: 10px;
                }
                QScrollArea {
                    background: transparent;
                    border: 2px solid #334155;
                    border-radius: 12px;
                }
                QScrollBar:vertical {
                    background: #1e293b;
                    width: 12px;
                    border-radius: 6px;
                }
                QScrollBar::handle:vertical {
                    background: #475569;
                    border-radius: 6px;
                    min-height: 20px;
                }
                QScrollBar::handle:vertical:hover {
                    background: #64748b;
                }
                QCheckBox {
                    spacing: 8px;
                    color: #e2e8f0;
                }
                QCheckBox::indicator {
                    width: 50px;
                    height: 26px;
                    border-radius: 13px;
                    background: #475569;
                    border: 2px solid #64748b;
                }
                QCheckBox::indicator:checked {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #3b82f6, stop:1 #2563eb);
                    border: 2px solid #3b82f6;
                }
                QCheckBox::indicator:checked:after {
                    content: "";
                }
            """)
            # Update drop label for dark mode
            self.drop_label.setStyleSheet("""
                QLabel {
                    border: 3px dashed #475569;
                    border-radius: 16px;
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #1e293b, stop:1 #0f172a);
                    color: #94a3b8;
                    padding: 20px;
                }
                QLabel:hover {
                    border-color: #3b82f6;
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #1e3a8a, stop:1 #1e293b);
                    color: #e2e8f0;
                }
            """)
            # Update preview label for dark mode
            self.preview_label.setStyleSheet("""
                QLabel {
                    border: 2px solid #334155;
                    border-radius: 12px;
                    background: #0f172a;
                    color: #94a3b8;
                    padding: 20px;
                }
            """)
            # Update color button
            self.color_btn.setStyleSheet(f"""
                QPushButton {{
                    background: {self.text_color.name()};
                    color: white;
                    border: 2px solid #475569;
                    border-radius: 8px;
                    padding: 10px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    border: 2px solid #3b82f6;
                }}
            """)
        else:
            # Light Mode - Clean Professional Design
            self.setStyleSheet("""
                QMainWindow {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #f8fafc, stop:1 #e2e8f0);
                }
                QLabel {
                    color: #1e293b;
                }
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #ffffff, stop:1 #f8fafc);
                    border-radius: 12px;
                    border: 1px solid #cbd5e1;
                }
                QGroupBox {
                    background: white;
                    border: 2px solid #e2e8f0;
                    border-radius: 16px;
                    padding: 10px;
                }
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #3b82f6, stop:1 #2563eb);
                    color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 12px 24px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #60a5fa, stop:1 #3b82f6);
                }
                QPushButton:pressed {
                    background: #1d4ed8;
                }
                QLineEdit, QSpinBox, QComboBox {
                    background: white;
                    color: #1e293b;
                    border: 2px solid #cbd5e1;
                    border-radius: 8px;
                    padding: 10px;
                    selection-background-color: #3b82f6;
                }
                QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
                    border: 2px solid #3b82f6;
                    background: #f8fafc;
                }
                QComboBox::drop-down {
                    border: none;
                    width: 30px;
                }
                QComboBox::down-arrow {
                    image: none;
                    border-left: 5px solid transparent;
                    border-right: 5px solid transparent;
                    border-top: 5px solid #1e293b;
                    margin-right: 10px;
                }
                QScrollArea {
                    background: transparent;
                    border: 2px solid #e2e8f0;
                    border-radius: 12px;
                }
                QScrollBar:vertical {
                    background: #f1f5f9;
                    width: 12px;
                    border-radius: 6px;
                }
                QScrollBar::handle:vertical {
                    background: #cbd5e1;
                    border-radius: 6px;
                    min-height: 20px;
                }
                QScrollBar::handle:vertical:hover {
                    background: #94a3b8;
                }
                QCheckBox {
                    spacing: 8px;
                    color: #1e293b;
                }
                QCheckBox::indicator {
                    width: 50px;
                    height: 26px;
                    border-radius: 13px;
                    background: #cbd5e1;
                    border: 2px solid #94a3b8;
                }
                QCheckBox::indicator:checked {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #3b82f6, stop:1 #2563eb);
                    border: 2px solid #3b82f6;
                }
            """)
            # Update drop label for light mode
            self.drop_label.setStyleSheet("""
                QLabel {
                    border: 3px dashed #cbd5e1;
                    border-radius: 16px;
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #ffffff, stop:1 #f8fafc);
                    color: #64748b;
                    padding: 20px;
                }
                QLabel:hover {
                    border-color: #3b82f6;
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #dbeafe, stop:1 #eff6ff);
                    color: #1e293b;
                }
            """)
            # Update preview label for light mode
            self.preview_label.setStyleSheet("""
                QLabel {
                    border: 2px solid #e2e8f0;
                    border-radius: 12px;
                    background: #f8fafc;
                    color: #64748b;
                    padding: 20px;
                }
            """)
            # Update color button
            self.color_btn.setStyleSheet(f"""
                QPushButton {{
                    background: {self.text_color.name()};
                    color: white;
                    border: 2px solid #cbd5e1;
                    border-radius: 8px;
                    padding: 10px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    border: 2px solid #3b82f6;
                }}
            """)
            
    def browse_files(self):
        """Open file dialog to select images"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Images",
            "",
            "Image Files (*.png *.jpg *.jpeg)"
        )
        if files:
            self.image_paths = files
            self.show_thumbnails()
            
    def show_thumbnails(self):
        """Display thumbnails of selected images"""
        # Clear previous thumbnails
        for i in reversed(range(self.preview_layout.count())): 
            self.preview_layout.itemAt(i).widget().setParent(None)
        self.preview_labels.clear()
        
        # Add new thumbnails
        for i, path in enumerate(self.image_paths):
            label = DraggableLabel(i)
            label.position_changed.connect(self.reorder_images)
            pixmap = QPixmap(path)
            scaled = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(scaled)
            label.setFixedSize(150, 150)
            
            row = i // 6
            col = i % 6
            self.preview_layout.addWidget(label, row, col)
            self.preview_labels.append(label)
            
    def reorder_images(self, from_index, to_index):
        """Reorder images when dragged"""
        if from_index != to_index:
            item = self.image_paths.pop(from_index)
            self.image_paths.insert(to_index, item)
            self.show_thumbnails()
            
    def preview_animation(self):
        """Preview the animation"""
        if not self.image_paths:
            QMessageBox.warning(self, 'No Images', 'Please upload images first!')
            return
            
        self.preview_timer.stop()
        self.preview_index = 0
        delay = self.delay_spin.value()
        
        def update_preview():
            pixmap = QPixmap(self.image_paths[self.preview_index])
            scaled = pixmap.scaled(600, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.preview_label.setPixmap(scaled)
            self.preview_index = (self.preview_index + 1) % len(self.image_paths)
            
        self.preview_timer.timeout.connect(update_preview)
        self.preview_timer.start(delay)
        update_preview()
        
    def create_gif(self):
        """Create the GIF with all settings"""
        if not self.image_paths:
            QMessageBox.warning(self, 'No Images', 'Please upload images first!')
            return
            
        try:
            # Load images
            images = []
            for path in self.image_paths:
                img = Image.open(path).convert('RGB')
                
                # Add text overlay if specified
                text = self.text_input.text()
                if text:
                    draw = ImageDraw.Draw(img)
                    
                    # Get font size
                    font_size = int(self.font_combo.currentText().split('px')[0])
                    try:
                        font = ImageFont.truetype("arial.ttf", font_size)
                    except:
                        font = ImageFont.load_default()
                    
                    # Get text position
                    bbox = draw.textbbox((0, 0), text, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    
                    x = (img.width - text_width) // 2
                    
                    position = self.position_combo.currentText()
                    if position == 'Top':
                        y = 30
                    elif position == 'Center':
                        y = (img.height - text_height) // 2
                    else:  # Bottom
                        y = img.height - text_height - 30
                    
                    # Draw text with outline for better visibility
                    outline_color = (0, 0, 0) if sum(self.text_color.getRgb()[:3]) > 384 else (255, 255, 255)
                    for adj_x in range(-2, 3):
                        for adj_y in range(-2, 3):
                            draw.text((x+adj_x, y+adj_y), text, font=font, fill=outline_color)
                    
                    draw.text((x, y), text, font=font, 
                             fill=(self.text_color.red(), self.text_color.green(), self.text_color.blue()))
                
                images.append(img)
            
            # Save as temporary file
            self.gif_path = os.path.join(os.path.dirname(self.image_paths[0]), 'output.gif')
            duration = self.delay_spin.value()
            images[0].save(
                self.gif_path,
                save_all=True,
                append_images=images[1:],
                duration=duration,
                loop=0,
                optimize=False
            )
            
            # Show success and enable download
            QMessageBox.information(self, 'Success', 'GIF created successfully!')
            self.download_btn.show()
            
            # Display the GIF
            pixmap = QPixmap(self.gif_path)
            scaled = pixmap.scaled(600, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.preview_label.setPixmap(scaled)
            
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error creating GIF: {str(e)}')
            
    def download_gif(self):
        """Save the GIF to a chosen location"""
        if hasattr(self, 'gif_path'):
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save GIF",
                "mygif.gif",
                "GIF Files (*.gif)"
            )
            if save_path:
                import shutil
                shutil.copy(self.gif_path, save_path)
                QMessageBox.information(self, 'Success', f'GIF saved to {save_path}')
                
    def choose_color(self):
        """Open color picker dialog"""
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_color = color
            border_color = '#475569' if self.dark_mode else '#cbd5e1'
            self.color_btn.setStyleSheet(f"""
                QPushButton {{
                    background: {color.name()};
                    color: white;
                    border: 2px solid {border_color};
                    border-radius: 8px;
                    padding: 10px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    border: 2px solid #3b82f6;
                }}
            """)
            
    def dragEnterEvent(self, event):
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self, event):
        """Handle drop event for files"""
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if image_files:
            self.image_paths = image_files
            self.show_thumbnails()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Set application font
    font = QFont('Inter', 10)
    app.setFont(font)
    
    window = GIFMakerApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
