import os
import sys
from PyPDF2 import PdfMerger
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
from docx import Document
from docx2pdf import convert
from PIL import Image

white_list = ['.docx', '.pdf', '.jpg', '.jpeg', '.png', '.gif']

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.file_name_lst = []
        self.file_path = ""
        self.file_lst = []
        self.pdf_lst = []
        self.pdf_order = 0
        self.temp_file_path = []

        self.initUI()

    def initUI(self):
        self.setWindowTitle("File Merger")
        self.setGeometry(100, 100, 400, 300)

        self.list_widget = DragDropListWidget(self)
        self.list_widget.setDragDropMode(QListWidget.InternalMove)
        self.list_widget.setAcceptDrops(True)

        self.button1 = QPushButton("Select", self)
        self.button1.clicked.connect(self.get_directory)

        self.button2 = QPushButton("Merge", self)
        self.button2.clicked.connect(self.merge_files)

        self.button3 = QPushButton("Clear", self)
        self.button3.clicked.connect(self.clear)

        self.button4 = QPushButton("Remove", self)
        self.button4.clicked.connect(self.remove_selected_item)

        layout = QVBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.button4)
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

    def get_directory(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_dialog = QFileDialog()
        file_dialog.setOptions(options)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setViewMode(QFileDialog.Detail)

        if file_dialog.exec_() == QFileDialog.Accepted:
            for file_path in file_dialog.selectedFiles():
                if not file_path.lower().endswith(tuple(white_list)):
                    print(f"[!] Unsupported file format: {file_path}")
                    continue
                self.file_name_lst.append(os.path.basename(file_path))
                self.file_lst.append(file_path)
                item = QListWidgetItem(os.path.basename(file_path))
                self.list_widget.addItem(item)
            self.file_path = os.path.dirname(file_dialog.selectedFiles()[0])
            print(f"[+] {len(self.file_lst)} files found!")

    def merge_files(self):
        self.pdf_lst = []

        for file_path in self.file_lst:
            if file_path.lower().endswith(('.doc', '.docx')):
                pdf_path = self.convert_to_pdf(file_path)
                if pdf_path:
                    self.pdf_lst.append(pdf_path)
            elif file_path.lower().endswith('.pdf'):
                self.pdf_lst.append(file_path)
            elif file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                pdf_path = self.convert_image_to_pdf(file_path)
                if pdf_path:
                    self.pdf_lst.append(pdf_path)
            else:
                print(f"[!] Unsupported file format: {file_path}")

        self.pdf_merger_lst = list(self.pdf_lst)

        pdf_merger = PdfMerger()
        for pdf_file in self.pdf_merger_lst:
            pdf_merger.append(pdf_file)

        output_file = QFileDialog.getSaveFileName(self, "Save Merged PDF", self.file_path, "PDF Files (*.pdf)")[0]
        if output_file:
            pdf_merger.write(output_file)
            pdf_merger.close()
            for file_path in self.temp_file_path:
                os.remove(file_path)
            self.temp_file_path = []
            print(f"[+] Files merged successfully to {output_file}")

    def convert_to_pdf(self, doc_file):
        if doc_file.lower().endswith('.docx'):
            pdf_file = doc_file.replace('.docx', '.pdf')

        try:
            if doc_file.lower().endswith('.docx'):
                doc = Document(doc_file)
                convert(doc_file, pdf_file)
            self.temp_file_path.append(pdf_file)

            print(f"[+] Converted {doc_file} to {pdf_file}")
            return pdf_file
        except Exception as e:
            print(f"[!] Error converting {doc_file} to PDF: {e}")
            return None

    def convert_image_to_pdf(self, image_file):
        pdf_file = image_file.replace(image_file[image_file.rfind('.'):], '.pdf')

        try:
            img = Image.open(image_file)
            if img.mode == "RGBA":
                img = img.convert("RGB")
            img.save(pdf_file, "PDF")
            self.temp_file_path.append(pdf_file)
            print(f"[+] Converted {image_file} to {pdf_file}")
            return pdf_file
        except Exception as e:
            print(f"[!] Error converting {image_file} to PDF: {e}")
            return None

    def clear(self):
        self.file_lst.clear()
        self.file_name_lst.clear()
        self.file_path = ""
        self.pdf_order = 0
        self.list_widget.clear()
        print("[+] Cleared successfully!")

    def change_order(self):
        selected_items = self.list_widget.selectedItems()

        if not selected_items:
            print("[+] No item selected for changing order.")
            return

        for item in selected_items:
            index = self.list_widget.row(item)
            if index < len(self.file_lst):
                self.file_lst.insert(self.pdf_order, self.file_lst.pop(index))
                self.file_name_lst.insert(self.pdf_order, self.file_name_lst.pop(index))
                self.pdf_order += 1
                self.list_widget.insertItem(self.pdf_order, item)

        print("[+] Selected item(s) order changed successfully.")

    def remove_selected_item(self):
        selected_items = self.list_widget.selectedItems()

        if not selected_items:
            print("[+] No item selected for removal.")
            return

        for item in selected_items:
            index = self.list_widget.row(item)
            if index < len(self.file_lst):
                removed_file = self.file_lst.pop(index)
                self.file_name_lst.pop(index)
                self.pdf_lst = [pdf for pdf in self.pdf_lst if pdf != removed_file]
                self.list_widget.takeItem(index)

        print("[+] Selected item(s) removed successfully.")


class DragDropListWidget(QListWidget):
    def __init__(self, parent=None):
        super(DragDropListWidget, self).__init__(parent)
        self.setDragDropMode(QListWidget.InternalMove)
        self.setAcceptDrops(True)
        self.setSelectionMode(QListWidget.ExtendedSelection)

    def dropEvent(self, event):
        super(DragDropListWidget, self).dropEvent(event)
        self.parent().change_order()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.parent().remove_selected_item()
        else:
            super(DragDropListWidget, self).keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWindow()
    ex.show()
    sys.exit(app.exec_())