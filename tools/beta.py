# main.py

from tools.logs import *
create_log_directory()
log_action(f"Importation du fichier 'logs.py'", success=True)
import sys
log_action(f"Importation de la biblioteque 'sys'", success=True)
import csv
log_action(f"Importation de la biblioteque 'csv'", success=True)
import os
log_action(f"Importation de la biblioteque 'os'", success=True)
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QWidget, QComboBox, QMessageBox, QFileDialog, QTreeWidget,
    QTreeWidgetItem, QTableWidgetItem, QHeaderView, QDialog, QAbstractItemView,
    QMenu, QCheckBox, QInputDialog, QTabWidget, QSizePolicy, QAction, QTextBrowser,
    QTableWidget)
log_action(f"Importation de la biblioteque 'PyQt5.QtWidgets' avec comme fonction 'QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout,QHBoxLayout, QWidget, QComboBox, QMessageBox, QFileDialog, QTreeWidget,QTreeWidgetItem, QTableWidgetItem, QHeaderView, QDialog, QAbstractItemView, QMenu, QCheckBox, QInputDialog, QTabWidget, QSizePolicy, QAction, QTextBrowser,QTableWidget'", success=True)
from PyQt5.QtGui import (QPixmap, QIcon)
log_action(f"Importation de la biblioteque 'PyQt5.QtGui' avec comme fonction 'QPixmap, QIcon'", success=True)
from PyQt5.QtCore import Qt, QSettings
log_action(f"Importation de la biblioteque 'PyQt5.QtCore' avec comme fonction 'Qt, QSettings'", success=True)
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
log_action(f"Importation de la biblioteque 'PyQt5.QtPrintSupport' avec comme fonction 'QPrinter, QPrintDialog'", success=True)
from reportlab.pdfgen import canvas
log_action(f"Importation de la biblioteque 'reportlab.pdfgen' avec comme fonction 'canvas'", success=True)
from reportlab.lib.pagesizes import letter
log_action(f"Importation de la biblioteque 'reportlab.lib.pagesizes' avec comme fonction 'letter'", success=True)
from tools.library_logic import *
log_action(f"Importation du fichier 'library_logic.py'", success=True)
from tools.user_logic import *
log_action(f"Importation du fichier 'user_logic.py'", success=True)
from tools.dialog_logic import *
log_action(f"Importation du fichier 'dialog_logic.py'", success=True)


class LibraryApp(QMainWindow):
    def __init__(self):
        super(LibraryApp, self).__init__()
        self.library = Library()
        self.user_gestion = User_gestion()

        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Application Bibliothèque")
        self.setGeometry(100, 100, 800, 600)
        self.setup_tabs()
        self.setup_menus()
        self.setup_layout()
        self.setup_bottom_layout()
        self.update_tables()

    def setup_tabs(self):
        self.tab_widget = QTabWidget()
        self.book_tab = QWidget()
        self.user_tab = QWidget()
        self.tab_widget.addTab(self.book_tab, "Livres")
        self.tab_widget.addTab(self.user_tab, "Utilisateurs")
        self.setup_book_tab()
        self.setup_user_tab()

    def setup_book_tab(self):
        self.setup_book_table()
        self.setup_borrow_return_remove_buttons()

    def setup_user_tab(self):
        self.setup_user_table()

    def setup_book_table(self):
        self.book_table = QTableWidget()
        self.book_table.doubleClicked.connect(self.edit_cell)

    def setup_user_table(self):
        self.user_table = QTableWidget()
        self.user_table.doubleClicked.connect(self.edit_cell)

    def setup_menus(self):
        self.setup_file_menu()
        self.setup_edit_menu()

    def setup_layout(self):
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tab_widget)
        self.layout.addLayout(self.setup_bottom_layout())
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def setup_bottom_layout(self):
        self.bottom_layout = QHBoxLayout()
        self.setup_borrow_return_remove_buttons()
        self.setup_import_export_buttons()
        self.bottom_layout.addStretch(1)
        return self.bottom_layout

    def setup_borrow_return_remove_buttons(self):
        borrow_return_layout = QHBoxLayout()
        self.borrow_label, self.return_label, self.remove_label = QLabel("ID à emprunter:"), QLabel(
            "ID à retourner:"), QLabel("ID à supprimer:")
        self.entry_take, self.entry_return, self.entry_remove = QLineEdit(), QLineEdit(), QLineEdit()
        self.btn_take, self.btn_return, self.btn_remove = QPushButton("Emprunter"), QPushButton("Retourner"), QPushButton(
            "Supprimer livre")

        self.btn_take.clicked.connect(self.take_book)
        self.btn_return.clicked.connect(self.return_book)
        self.btn_remove.clicked.connect(self.remove_book)

        borrow_return_layout.addWidget(self.borrow_label)
        borrow_return_layout.addWidget(self.entry_take)
        borrow_return_layout.addWidget(self.btn_take)
        borrow_return_layout.addWidget(self.return_label)
        borrow_return_layout.addWidget(self.entry_return)
        borrow_return_layout.addWidget(self.btn_return)
        borrow_return_layout.addWidget(self.remove_label)
        borrow_return_layout.addWidget(self.entry_remove)
        borrow_return_layout.addWidget(self.btn_remove)

        self.layout.addLayout(borrow_return_layout)

    def setup_import_export_buttons(self):
        self.import_export_layout = QHBoxLayout()
        self.btn_import, self.btn_export, self.btn_open_add_book_dialog = QPushButton(
            "Importer depuis CSV"), QPushButton("Exporter vers CSV"), QPushButton("Ajouter un livre")
        self.btn_import.clicked.connect(self.import_from_csv)
        self.btn_export.clicked.connect(self.export_to_csv)
        self.btn_open_add_book_dialog.clicked.connect(self.open_add_book_dialog)
        self.import_export_layout.addWidget(self.btn_import)
        self.import_export_layout.addWidget(self.btn_export)
        self.import_export_layout.addWidget(self.btn_open_add_book_dialog)
        self.layout.addLayout(self.import_export_layout)

    def set_library_app_reference(self, library_app):
        self.library_app = library_app

    def show_context_menu(self, pos):
        menu = QMenu(self)
        actions = {"Copier": self.copy_selected_item, "Supprimer": self.delete_selected_item, "Modifier": self.edit_selected_item}
        for action_text, action_method in actions.items():
            menu.addAction(action_text, action_method)
        action = menu.exec_(self.book_table.mapToGlobal(pos))
        if action:
            actions[action.text()]()

    def copy_selected_item(self):
        selected_item = self.book_table.currentItem()
        if selected_item:
            clipboard = QApplication.clipboard()
            clipboard.setText(selected_item.text(self.book_table.currentColumn()))

    def edit_selected_item(self):
        selected_item = self.book_table.currentItem()
        if selected_item:
            self.edit_cell(selected_item)

    def update_table_item(self, item, old_value, new_value):
        column = self.book_table.currentColumn()
        column_name = self.book_table.horizontalHeaderItem(column).text() if self.book_table == item.treeWidget() else self.user_table.horizontalHeaderItem(column).text()

        element_id = int(item.text(0))
        if isinstance(item, QTreeWidgetItem) and item.treeWidget() == self.book_table:
            element = self.library.get_book_by_id(element_id)
        elif isinstance(item, QTreeWidgetItem) and item.treeWidget() == self.user_table:
            element = self.user_gestion.get_user_by_id(element_id)

        if column == 1:
            element.title = new_value
        elif column == 2:
            element.author = new_value
        elif column == 3:
            element.publisher = new_value
        elif column == 4:
            element.isbn = new_value
        elif column == 5:
            element.total_copies = int(new_value) if self.book_table == item.treeWidget() else None
            element.take = new_value if self.user_table == item.treeWidget() else None
        elif column == 6:
            element.available_copies = int(new_value) if self.book_table == item.treeWidget() else None

        self.library.update_book(element) if self.book_table == item.treeWidget() else self.user_gestion.update_user(
            element)

    def open_add_book_dialog(self):
        add_book_dialog = AddBookDialog(self)
        add_book_dialog.set_library_app_reference(self)
        add_book_dialog.exec_()

    def open_add_user_dialog(self):
        add_user_dialog = AddUserDialog(self)
        add_user_dialog.set_library_app_reference(self)
        add_user_dialog.exec_()

    def update_tables(self):
        self.update_book_table()
        self.update_user_table()

    def update_book_table(self):
        self.book_table.setRowCount(0)
        for book in self.library.get_books():
            self.add_book_to_table(book)

    def update_user_table(self):
        self.user_table.setRowCount(0)
        for user in self.user_gestion.get_users():
            self.add_user_to_table(user)

    def add_book_to_table(self, book):
        row_position = self.book_table.rowCount()
        self.book_table.insertRow(row_position)
        self.book_table.setItem(row_position, 0, QTableWidgetItem(str(book.id)))
        self.book_table.setItem(row_position, 1, QTableWidgetItem(book.title))
        self.book_table.setItem(row_position, 2, QTableWidgetItem(book.author))
        self.book_table.setItem(row_position, 3, QTableWidgetItem(book.publisher))
        self.book_table.setItem(row_position, 4, QTableWidgetItem(book.isbn))
        self.book_table.setItem(row_position, 5, QTableWidgetItem(str(book.total_copies)))
        self.book_table.setItem(row_position, 6, QTableWidgetItem(str(book.available_copies)))

    def add_user_to_table(self, user):
        row_position = self.user_table.rowCount()
        self.user_table.insertRow(row_position)
        self.user_table.setItem(row_position, 0, QTableWidgetItem(str(user.id)))
        self.user_table.setItem(row_position, 1, QTableWidgetItem(user.first_name))
        self.user_table.setItem(row_position, 2, QTableWidgetItem(user.last_name))
        self.user_table.setItem(row_position, 3, QTableWidgetItem(user.email))
        self.user_table.setItem(row_position, 4, QTableWidgetItem(user.address))
        self.user_table.setItem(row_position, 5, QTableWidgetItem(str(user.borrowed_books)))

    def edit_cell(self, item):
        row, column = item.row(), item.column()
        old_value = item.text()
        new_value, ok = QInputDialog.getText(self, "Édition de cellule",
                                            f"Entrez une nouvelle valeur pour {self.book_table.horizontalHeaderItem(column).text()}:" if
                                            self.book_table == item.treeWidget() else f"Entrez une nouvelle valeur pour {self.user_table.horizontalHeaderItem(column).text()}",
                                            QLineEdit.Normal, old_value)
        if ok and new_value != old_value:
            item.setText(new_value)
            self.update_table_item(item, old_value, new_value)

    def import_from_csv(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Importer depuis un fichier CSV", "", "CSV Files (*.csv)")
        if file_path:
            self.library.import_from_csv(file_path)
            self.update_tables()

    def export_to_csv(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, "Exporter vers un fichier CSV", "", "CSV Files (*.csv)")
        if file_path:
            self.library.export_to_csv(file_path)

    def take_book(self):
        book_id = self.entry_take.text()
        if book_id:
            book_id = int(book_id)
            success = self.library.take_book(book_id)
            if success:
                self.update_tables()
            else:
                QMessageBox.warning(self, "Emprunt de livre",
                                    f"Impossible d'emprunter le livre avec l'ID {book_id}.")

    def return_book(self):
        book_id = self.entry_return.text()
        if book_id:
            book_id = int(book_id)
            success = self.library.return_book(book_id)
            if success:
                self.update_tables()
            else:
                QMessageBox.warning(self, "Retour de livre",
                                    f"Impossible de retourner le livre avec l'ID {book_id}.")

    def remove_book(self):
        book_id = self.entry_remove.text()
        if book_id:
            book_id = int(book_id)
            success = self.library.remove_book(book_id)
            if success:
                self.update_tables()
            else:
                QMessageBox.warning(self, "Suppression de livre",
                                    f"Impossible de supprimer le livre avec l'ID {book_id}.")


if __name__ == "__main__":
    app = QApplication([])
    window = LibraryApp()
    window.show()
    app.exec_()
