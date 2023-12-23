# PDF Merger

## Overview

The PDF Merger is a simple application built with PyQt5 that allows users to merge PDF files, Word documents, and images into a single PDF file. It provides a user-friendly interface for selecting files, arranging their order, and merging them seamlessly.

## Features

- **PDF Merging:** Merge multiple PDF files into a single PDF document.
- **Word to PDF Conversion:** Convert Word documents (`.docx`) to PDF before merging.
- **Image to PDF Conversion:** Convert images (`.jpg`, `.jpeg`, `.png`, `.gif`) to PDF before merging.
- **Drag and Drop:** Easily arrange the order of files by dragging and dropping them in the list.
- **Selective Removal:** Remove selected items from the list with a click or by pressing the 'Delete' key.
- **Clear Function:** Clear the list and start fresh with a click of a button.

## Getting Started

1. **Installation:**
   - Ensure you have Python installed.
   - Install required dependencies using:
     ```bash
     pip install -r requirements.txt
     ```

2. **Running the Application:**
   - Execute the following command in the terminal:
     ```bash
     python PDFmerger.py
     ```

3. **Selecting Files:**
   - Click the **"Select"** button to choose the files you want to merge.

4. **Merging Files:**
   - Click the **"Merge"** button to start the merging process. Choose the destination for the merged PDF file.

5. **Changing Order:**
   - Drag and drop files in the list to change their order before merging.

6. **Removing Items:**
   - Select items and press the **'Delete'** key or click the **"Remove"** button to remove them from the list.

7. **Clearing the List:**
   - Click the **"Clear"** button to clear the list and start fresh.

## TODO

- [ ] Add support for more file types.
  - [ ] doc
  - [ ] html
  - [ ] md
  - [ ] source code
  - [ ] and more...
- [ ] Beutify the UI.
- [ ] Portability.
- [ ] Python to executable.

## Contributions

Contributions are welcome! If you have any suggestions, bug reports, or want to contribute to the project, feel free to open an issue or create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
