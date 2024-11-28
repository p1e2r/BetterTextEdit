import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QMessageBox, QToolBar, QMenu, QComboBox, QSpinBox
)
from PyQt5.QtGui import QKeySequence, QFont
from PyQt5.QtCore import Qt


class TextEditor(QMainWindow):
    MAX_RECENTS = 5  # Maximum number of recent files to store

    def __init__(self, initial_file=None):
        super().__init__()
        self.current_file = initial_file
        self.recent_files = []  # List to store recent files
        self.init_ui()

        # Load the file if provided via command-line argument
        if self.current_file:
            self.load_file(self.current_file)

    def init_ui(self):
        self.setWindowTitle("Text Editor")
        self.setGeometry(100, 100, 800, 600)

        # Create a text edit widget
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        # Create a menu bar
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        # New File action
        new_action = QAction("New File", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        # Open action
        open_action = QAction("Open", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        # Save action
        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Add a toolbar
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)

        # Add new file button to toolbar
        new_toolbar_action = QAction("New File", self)
        new_toolbar_action.setShortcut(QKeySequence.New)
        new_toolbar_action.triggered.connect(self.new_file)
        self.toolbar.addAction(new_toolbar_action)

        # Add open button to toolbar
        open_toolbar_action = QAction("Open", self)
        open_toolbar_action.setShortcut(QKeySequence.Open)
        open_toolbar_action.triggered.connect(self.open_file)
        self.toolbar.addAction(open_toolbar_action)

        # Add save button to toolbar
        save_toolbar_action = QAction("Save", self)
        save_toolbar_action.setShortcut(QKeySequence.Save)
        save_toolbar_action.triggered.connect(self.save_file)
        self.toolbar.addAction(save_toolbar_action)

        # Add recents button to toolbar
        self.recents_menu = QMenu("Recents", self)
        recents_toolbar_action = QAction("Recents", self)
        recents_toolbar_action.setMenu(self.recents_menu)
        self.toolbar.addAction(recents_toolbar_action)

        # Add a second toolbar for font editing
        self.font_toolbar = QToolBar("Font Toolbar")
        self.addToolBar(Qt.TopToolBarArea, self.font_toolbar)

        # Font family dropdown
        self.font_combobox = QComboBox(self)
        self.font_combobox.addItems(["Arial", "Times New Roman", "Courier New", "Verdana"])
        self.font_combobox.currentTextChanged.connect(self.change_font)
        self.font_toolbar.addWidget(self.font_combobox)

        # Font size spinbox
        self.font_size_spinner = QSpinBox(self)
        self.font_size_spinner.setValue(12)
        self.font_size_spinner.setRange(1, 100)
        self.font_size_spinner.valueChanged.connect(self.change_font_size)
        self.font_toolbar.addWidget(self.font_size_spinner)

        # Bold action
        bold_action = QAction("Bold", self)
        bold_action.setShortcut(QKeySequence.Bold)
        bold_action.triggered.connect(self.toggle_bold)
        self.font_toolbar.addAction(bold_action)

        # Italic action
        italic_action = QAction("Italic", self)
        italic_action.setShortcut(QKeySequence.Italic)
        italic_action.triggered.connect(self.toggle_italic)
        self.font_toolbar.addAction(italic_action)

        # Underline action
        underline_action = QAction("Underline", self)
        underline_action.setShortcut(QKeySequence.Underline)
        underline_action.triggered.connect(self.toggle_underline)
        self.font_toolbar.addAction(underline_action)

    def new_file(self):
        """Creates and opens a new file."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "New File", "", "Text Files (*.txt);;All Files (*)", options=options
        )
        if file_path:
            try:
                # Create an empty file to initialize it
                with open(file_path, 'w') as file:
                    pass
                self.load_file(file_path)  # Load the new file for editing
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not create file: {e}")

    def load_file(self, file_path):
        """Loads the content of a file into the text editor."""
        try:
            with open(file_path, 'r') as file:
                self.text_edit.setText(file.read())
            self.current_file = file_path
            self.add_to_recents(file_path)
            self.setWindowTitle(f"Text Editor - {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open file: {e}")

    def open_file(self):
        """Opens a file using a file dialog."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "Text Files (*.txt);;All Files (*)", options=options
        )
        if file_path:
            self.load_file(file_path)

    def save_file(self):
        """Saves the content to the current file or triggers Save As if no file is loaded."""
        if self.current_file:
            try:
                with open(self.current_file, 'w') as file:
                    file.write(self.text_edit.toPlainText())
                QMessageBox.information(self, "Saved", "File saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file: {e}")
        else:
            self.save_as_file()

    def save_as_file(self):
        """Opens a Save As dialog to save the content to a new file."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save File As", "", "Text Files (*.txt);;All Files (*)", options=options
        )
        if file_path:
            self.current_file = file_path
            self.save_file()

    def add_to_recents(self, file_path):
        """Adds a file path to the recent files list."""
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        self.recent_files.insert(0, file_path)

        # Keep the list limited to MAX_RECENTS
        if len(self.recent_files) > self.MAX_RECENTS:
            self.recent_files = self.recent_files[:self.MAX_RECENTS]

        self.update_recents_menu()

    def update_recents_menu(self):
        """Updates the recents menu with the latest file paths."""
        self.recents_menu.clear()
        for file_path in self.recent_files:
            file_name = os.path.splitext(os.path.basename(file_path))[0]  # Extract file name without extension
            action = QAction(file_name, self)
            action.setToolTip(file_path)  # Show the full path as a tooltip
            # Use a lambda with default argument to bind file_path correctly
            action.triggered.connect(lambda checked, path=file_path: self.load_file(path))
            self.recents_menu.addAction(action)

    def change_font(self):
        """Changes the font family based on the selected option."""
        font = QFont(self.font_combobox.currentText(), self.font_size_spinner.value())
        self.text_edit.setFont(font)

    def change_font_size(self):
        """Changes the font size based on the selected value."""
        font = self.text_edit.font()
        font.setPointSize(self.font_size_spinner.value())
        self.text_edit.setFont(font)

    def toggle_bold(self):
        """Toggles the bold style of the text."""
        font = self.text_edit.font()
        font.setBold(not font.bold())
        self.text_edit.setFont(font)

    def toggle_italic(self):
        """Toggles the italic style of the text."""
        font = self.text_edit.font()
        font.setItalic(not font.italic())
        self.text_edit.setFont(font)

    def toggle_underline(self):
        """Toggles the underline style of the text."""
        font = self.text_edit.font()
        font.setUnderline(not font.underline())
        self.text_edit.setFont(font)


def main():
    app = QApplication(sys.argv)

    # Check if a file path is provided as a command-line argument
    initial_file = sys.argv[1] if len(sys.argv) > 1 else None
    editor = TextEditor(initial_file)
    editor.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
