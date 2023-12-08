# main.py

from logs import *
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
    QTreeWidgetItem, QTableWidgetItem, QHeaderView, QDialog, QAbstractItemView, QMenu, QCheckBox, QInputDialog)
<<<<<<< Updated upstream
from PyQt5.QtGui import (QPixmap, QIcon)
from PyQt5.QtCore import Qt, QSettings
=======
log_action(f"Importation de la biblioteque 'PyQt5.QtWidgets' avec comme fonction 'QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout,QHBoxLayout, QWidget, QComboBox, QMessageBox, QFileDialog, QTreeWidget,QTreeWidgetItem, QTableWidgetItem, QHeaderView, QDialog, QAbstractItemView, QMenu, QCheckBox, QInputDialog'", success=True)
from PyQt5.QtGui import (QPixmap, QIcon)
log_action(f"Importation de la biblioteque 'PyQt5.QtGui' avec comme fonction 'QPixmap, QIcon'", success=True)
from PyQt5.QtCore import Qt, QSettings
log_action(f"Importation de la biblioteque 'PyQt5.QtCore' avec comme fonction 'Qt, QSettings'", success=True)
>>>>>>> Stashed changes
from library_logic import *
log_action(f"Importation du fichier 'library_logic.py'", success=True)

def load_stylesheet(file_path):
    with open(file_path, 'r') as file:
        return file.read()

class ConfirmationDialog(QDialog):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirmation de suppression")
        self.resize(300, 150)

        layout = QVBoxLayout()
        
        # Définir l'icône de l'application dans la barre des tâches
        self.setWindowIcon(QIcon('icon.png'))

        self.message_label = QLabel(message)
        layout.addWidget(self.message_label)

        self.never_show_checkbox = QCheckBox("Ne plus afficher")
        layout.addWidget(self.never_show_checkbox)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)
        
        self.setStyleSheet(load_stylesheet('content\css\style_confirmeDialog.css'))

        self.setLayout(layout)

def load_stylesheet(file_path):
    with open(file_path, 'r') as file:
        return file.read()

class ConfirmationDialog(QDialog):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirmation de suppression")
        self.resize(300, 150)

        layout = QVBoxLayout()
        
        # Définir l'icône de l'application dans la barre des tâches
        self.setWindowIcon(QIcon('icon.png'))
        
        # Afficher le logo dans la bannière
        self.logo_label = QLabel(self)
        self.pixmap = QPixmap(os.path.join(current_dir, 'logo.png'))  # Assurez-vous que 'logo.png' est dans le même répertoire que votre script
        self.logo_label.setPixmap(self.pixmap)

        self.message_label = QLabel(message)
        layout.addWidget(self.message_label)

        self.never_show_checkbox = QCheckBox("Ne plus afficher")
        layout.addWidget(self.never_show_checkbox)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)
        
        self.setStyleSheet(load_stylesheet('content\css\style_confirmeDialog.css'))

        self.setLayout(layout)

class AddBookDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter un livre")
        self.resize(300, 100)

        self.layout = QVBoxLayout()

        self.entry_title = QLineEdit()
        self.entry_title.setPlaceholderText("Titre du livre")
        self.layout.addWidget(self.entry_title)

        self.entry_author = QLineEdit()
        self.entry_author.setPlaceholderText("Auteur")
        self.layout.addWidget(self.entry_author)

        self.entry_publisher = QLineEdit()  # Champ pour la maison d'édition
        self.entry_publisher.setPlaceholderText("Maison d'édition")
        self.layout.addWidget(self.entry_publisher)

        self.entry_isbn = QLineEdit()
        self.entry_isbn.setPlaceholderText("ISBN")
        self.layout.addWidget(self.entry_isbn)

        self.entry_copies = QLineEdit()
        self.entry_copies.setPlaceholderText("Nombre d'exemplaires")
        self.layout.addWidget(self.entry_copies)

        buttons_layout = QHBoxLayout()

        self.btn_add = QPushButton("Ajouter")
        self.btn_add.clicked.connect(self.add_book_to_list)
        buttons_layout.addWidget(self.btn_add)

        self.btn_cancel = QPushButton("Annuler")
        self.btn_cancel.clicked.connect(self.close)
        buttons_layout.addWidget(self.btn_cancel)

        self.layout.addLayout(buttons_layout)
        self.setLayout(self.layout)
        
#         self.secondary_books_table = QTreeWidget()
#         self.secondary_books_table.setColumnCount(4)
#         self.secondary_books_table.setHeaderLabels(["ID", "Titre", "Auteur", "Maison d'édition", "ISBN", "Exemplaires", "Exemplaires Diponibles"])
#         self.layout.addWidget(self.secondary_books_table)
        
    
    def add_book_to_list(self):
        if self.library_app.library.books:  
            last_book = max(self.library_app.library.books, key=lambda x: x.book_id)
            new_book_id = last_book.book_id + 1  
        else:
            new_book_id = 1  

        title = self.entry_title.text()
        author = self.entry_author.text()
        publisher = self.entry_publisher.text()
        isbn = self.entry_isbn.text()
        total_copies = self.entry_copies.text()
        available_copies = total_copies

        if title and author and publisher and isbn and total_copies:
            new_book = Book(
                new_book_id,
                title,
                author,
                publisher,
                isbn,
                int(total_copies),
                int(available_copies)
            )

            self.library_app.library.add(new_book)
#             log_action(f"Ajout d'un livre : ID={new_book_id}, Titre='{title}', Auteur='{author}', ISBN='{isbn}'", success=True)
            books = self.library_app.library.display_books()
            self.library_app.update_book_table(books)

            # Effacer les champs après l'ajout du livre
            self.entry_title.clear()
            self.entry_author.clear()
            self.entry_publisher.clear()
            self.entry_isbn.clear()
            self.entry_copies.clear()


class LibraryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jobi - Gestion de bibliothèque")
        self.setGeometry(100, 100, 800, 500)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Appliquer des styles CSS à certains composants
        self.setStyleSheet(load_stylesheet('content\css\style.css'))

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        # Déterminer le chemin du répertoire actuel
        current_dir = os.path.dirname(os.path.realpath(__file__))

        # Définir l'icône de l'application dans la barre des tâches
        self.setWindowIcon(QIcon('icon.png'))
        
        # Afficher le logo dans la bannière
        self.logo_label = QLabel(self)
        self.pixmap = QPixmap(os.path.join(current_dir, 'icon.png'))  # Assurez-vous que 'logo.png' est dans le même répertoire que votre script
        self.logo_label.setPixmap(self.pixmap)
        
        self.settings = QSettings("Jobi", "gestion_library_app")
        
        self.library = Library()
        self.setup_search_section()
        self.setup_book_table()
        self.setup_borrow_return_remove_sections()
        self.setup_import_export_buttons()
        
        # Connecter la modification de la cellule au signal correspondant
        self.book_table.itemChanged.connect(self.update_book_info)

    def open_add_book_dialog(self):
        dialog = AddBookDialog(self)
        dialog.library_app = self
        dialog.exec_()

        
    def setup_search_section(self):
        search_layout = QHBoxLayout()

        self.search_label = QLabel("Recherche:")
        self.entry_search = QLineEdit()
        self.entry_search.setObjectName("entry_search")

        self.entry_search.textChanged.connect(self.search_books)
        search_layout.addWidget(self.search_label)
        search_layout.addWidget(self.entry_search)

        self.search_type_label = QLabel("Type :")
        self.search_combobox = QComboBox()
        self.search_combobox.setObjectName("search_combobox")

        search_options = ["Titre", "Auteur", "Maison d'édition", "ISBN", "Exemplaires", "Exemplaires Diponibles"]#, "ID"]
        self.search_combobox.addItems(search_options)
        self.search_combobox.currentIndexChanged.connect(self.search_books)
        search_layout.addWidget(self.search_type_label)
        search_layout.addWidget(self.search_combobox)

        self.layout.addLayout(search_layout)

    def setup_book_table(self):
        self.book_table = QTreeWidget()
        self.book_table.setColumnCount(7)  # Il y a 7 colonnes dans votre cas
        self.book_table.setHeaderLabels(["ID", "Titre", "Auteur", "Maison d'édition", "ISBN", "Exemplaires", "Exemplaires Disponibles"])
        header = self.book_table.header()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.layout.addWidget(self.book_table)

        # Rendre tous les éléments éditables dans le tableau
        self.book_table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked | QAbstractItemView.EditKeyPressed)
        
<<<<<<< Updated upstream
         # Activer la détection du clic droit pour le menu contextuel
=======
        # Activer la détection du clic droit pour le menu contextuel
>>>>>>> Stashed changes
        self.book_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.book_table.customContextMenuRequested.connect(self.show_context_menu)
        
        # Détection du double-clic sur l'en-tête de colonne pour le renommage
        header = self.book_table.header()
        header.sectionDoubleClicked.connect(self.rename_column)
        
        
    def setup_borrow_return_remove_sections(self):
        borrow_return_layout = QHBoxLayout()

        self.borrow_label = QLabel("ID à emprunter:")
        self.entry_take = QLineEdit()
        borrow_return_layout.addWidget(self.borrow_label)
        borrow_return_layout.addWidget(self.entry_take)

        self.btn_take = QPushButton("Emprunter")
        self.btn_take.clicked.connect(self.take_book)
        borrow_return_layout.addWidget(self.btn_take)

        self.return_label = QLabel("ID à retourner:")
        self.entry_return = QLineEdit()
        borrow_return_layout.addWidget(self.return_label)
        borrow_return_layout.addWidget(self.entry_return)

        self.btn_return = QPushButton("Retourner")
        self.btn_return.clicked.connect(self.return_book)
        borrow_return_layout.addWidget(self.btn_return)

        self.remove_label = QLabel("ID à supprimer:")
        self.entry_remove = QLineEdit()
        borrow_return_layout.addWidget(self.remove_label)
        borrow_return_layout.addWidget(self.entry_remove)

        self.btn_remove = QPushButton("Supprimer livre")
        self.btn_remove.clicked.connect(self.remove_book)
        borrow_return_layout.addWidget(self.btn_remove)

        self.layout.addLayout(borrow_return_layout)

    def setup_import_export_buttons(self):
        self.import_export_layout = QHBoxLayout()

        self.btn_import = QPushButton("Importer depuis CSV")
        self.btn_import.clicked.connect(self.import_from_csv)
        self.import_export_layout.addWidget(self.btn_import)

        self.btn_export = QPushButton("Exporter vers CSV")
        self.btn_export.clicked.connect(self.export_to_csv)
        self.import_export_layout.addWidget(self.btn_export)

        self.btn_open_add_book_dialog = QPushButton("Ajouter un livre")
        self.btn_open_add_book_dialog.clicked.connect(self.open_add_book_dialog)
        self.import_export_layout.addWidget(self.btn_open_add_book_dialog)

        self.layout.addLayout(self.import_export_layout)
        self.layout.update()
        
    # Ajoute cette méthode dans AddBookDialog
    def set_library_app_reference(self, library_app):
        self.library_app = library_app

    
    # Fonction pour afficher le menu contextuel lors du clic droit
    def show_context_menu(self, pos):
        menu = QMenu(self)
        copy_action = menu.addAction("Copier")
        delete_action = menu.addAction("Supprimer")
        modify_action = menu.addAction("Modifier")
<<<<<<< Updated upstream
=======

        action = menu.exec_(self.book_table.mapToGlobal(pos))
        if action == copy_action:
            selected_item = self.book_table.currentItem()
            if selected_item is not None:
                clipboard = QApplication.clipboard()
                clipboard.setText(selected_item.text(self.book_table.currentColumn()))
        elif action == modify_action:
            selected_item = self.book_table.currentItem()
            if selected_item is not None:
                self.edit_cell(selected_item)
        elif action == delete_action:
            selected_item = self.book_table.currentItem()
            if selected_item is not None:
                log_action(f"Tentative de suppression de l'élément avec l'ID={selected_item.text(0)}", success=True)
                # Vérifie si la case à cocher "Ne plus afficher" est déjà cochée
                never_show_checked = self.settings.value("NeverShowConfirmation", False, type=bool)
                if not never_show_checked:
                    confirmation_dialog = ConfirmationDialog("Êtes-vous sûr de vouloir supprimer cet élément ?")
                    result = confirmation_dialog.exec_()
                    if result == QDialog.Accepted:
                        should_hide_dialog = confirmation_dialog.never_show_checkbox.isChecked()
                        if should_hide_dialog:
                            self.settings.setValue("NeverShowConfirmation", True)  # Enregistrer le choix utilisateur
                        self.delete_selected_item()  # Appel à la fonction de suppression
                        confirmation_dialog.deleteLater()  # Supprimer la boîte de dialogue après utilisation
                else:
                    self.delete_selected_item()  # Si "Ne plus afficher" est déjà coché, supprime directement l'élément
    
    def update_book_info(self):
        try:
            selected_items = self.book_table.selectedItems()
            for item in selected_items:
                book_id = int(item.text(0))  # Supposons que la première colonne contienne l'ID du livre
                book = self.library.get_book_by_id(book_id)

                column = self.book_table.currentColumn()
                # Mettre à jour les détails du livre selon la colonne
                if column == 1:  # Supposez que la colonne 1 correspond au titre du livre
                    book.title = item.text(column)
                elif column == 2:  # Colonne pour l'auteur
                    book.author = item.text(column)
                elif column == 3:  # Colonne pour la maison d'édition
                    book.publisher = item.text(column)
                elif column == 4:  # Colonne pour l'ISBN
                    book.isbn = item.text(column)
                elif column == 5:  # Colonne pour le nombre total d'exemplaires
                    book.total_copies = int(item.text(column))
                elif column == 6:  # Colonne pour le nombre d'exemplaires disponibles
                    book.available_copies = int(item.text(column))
                    # Mise à jour du nombre d'exemplaires disponibles si nécessaire
                    # book.available_copies = ... (calcul pour déterminer les exemplaires disponibles)

                # Appel à la méthode de la classe Library pour mettre à jour les détails du livre
                self.library.update_book_details(book)
                self.update_book_table()
        except Exception as e:
            # Enregistrement de l'erreur dans les logs
            log_action(f"Erreur lors de la mise à jour des détails du livre : {str(e)}", success=False)
            print("Une erreur s'est produite :", e)
    
    def update_book_table(self, books=None):
        self.book_table.clear()
        if not books:
            books = self.library.display_books()

        for book in books:
            item = QTreeWidgetItem(self.book_table)
            item.setText(0, str(book.book_id))
            item.setText(1, book.title)
            item.setText(2, book.author)
            item.setText(3, str(book.publisher))
            item.setText(4, book.isbn)
            item.setText(5, str(book.total_copies))
            item.setText(6, str(book.available_copies))

            # Rendre tous les éléments de cet item éditables
            for column in range(self.book_table.columnCount()):
                item.setFlags(item.flags() | Qt.ItemIsEditable)

    def take_book(self):
        book_id = self.entry_take.text()
        success, message = self.library.take_book_by_id(book_id)
        if success:
            # Enregistrement de l'action dans les logs
            log_action(f"Emprunt d'un livre avec l'ID={book_id}", success=True)
            QMessageBox.information(self, "Emprunt", message)
            self.update_book_table()
        else:
            # Enregistrement de l'erreur dans les logs
            log_action(f"Erreur lors de l'emprunt d'un livre avec l'ID={book_id}: {str(e)}", success=False)
            QMessageBox.warning(self, "Emprunt impossible", message)

    def return_book(self):
        book_id = self.entry_return.text()
        success, message = self.library.return_book_by_id(book_id)
        if success:
            # Enregistrement de l'action dans les logs
            log_action(f"Retour d'un livre avec l'ID={book_id}", success=True)
            QMessageBox.information(self, "Retour", message)
            self.update_book_table()
        else:
            # Enregistrement de l'erreur dans les logs
            log_action(f"Erreur lors du retour d'un livre avec l'ID={book_id}: {str(e)}", success=False)
            QMessageBox.warning(self, "Retour impossible", message)

    def remove_book(self):
        book_id = self.entry_remove.text()
        success, message = self.library.remove_book_by_id(book_id)
        if success:
            # Enregistrement de l'action dans les logs
            log_action(f"Suppression d'un livre avec l'ID={book_id}", success=True)
            QMessageBox.information(self, "Suppression", message)
            self.update_book_table()
        else:
            # Enregistrement de l'erreur dans les logs
            log_action(f"Erreur lors de la suppression d'un livre avec l'ID={book_id}: {str(e)}", success=False)
            QMessageBox.warning(self, "Suppression impossible", message)
    
    def delete_selected_item(self):
        selected_item = self.book_table.currentItem()
        if selected_item is not None:
            book_id = selected_item.text(0)
            self.library.remove_book_by_id(book_id)  # Supprimer l'élément dans la bibliothèque
            self.book_table.takeTopLevelItem(self.book_table.indexOfTopLevelItem(selected_item))  # Supprimer visuellement dans le tableau


    def import_from_csv(self):
        new_book_id = None  # Initialisation de new_book_id en dehors du bloc try

        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier CSV", "", "CSV Files (*.csv)")
            if file_path:
                success = self.library.import_from_csv(file_path)
                if success:
                    # Enregistrement de l'action dans les logs
                    log_action("Importation réussie depuis un fichier CSV", success=True)
                    QMessageBox.information(self, "Importation réussie", "Les livres ont été importés avec succès depuis le fichier CSV.")
                    self.update_book_table()
                else:
                    # Enregistrement de l'erreur dans les logs
                    log_action("Erreur lors de l'importation depuis un fichier CSV", success=False)
                    QMessageBox.critical(self, "Erreur d'importation", "Une erreur est survenue lors de l'importation depuis le fichier CSV.")
        except Exception as e:
            # Enregistrement de l'erreur dans les logs
            log_action(f"Erreur lors de l'importation depuis un fichier CSV : {str(e)}", success=False)
            # Gérer l'erreur (affichage d'un message à l'utilisateur ou autre)
            QMessageBox.critical(self, "Erreur d'importation", "Une erreur est survenue lors de l'importation depuis le fichier CSV.")
                
    def export_to_csv(self):
        try:
            file_path, _ = QFileDialog.getSaveFileName(self, "Enregistrer le fichier CSV", "", "CSV Files (*.csv)")
            if file_path:
                with open(file_path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Title', 'Author', 'Publisher', 'ISBN', 'Total Copies'])
                    for book in self.library.display_books():
                        writer.writerow([book.title, book.author, book.isbn, book.available_copies])
                # Enregistrement de l'action dans les logs
                log_action("Exportation réussie vers un fichier CSV", success=True)
                QMessageBox.information(self, "Exportation réussie", "Les données ont été exportées avec succès vers un fichier CSV.")
        except Exception as e:
            # Enregistrement de l'erreur dans les logs
            log_action(f"Erreur lors de l'exportation vers un fichier CSV : {str(e)}", success=False)
            # Gérer l'erreur (affichage d'un message à l'utilisateur ou autre)
            QMessageBox.critical(self, "Erreur d'exportation", f"Une erreur est survenue lors de l'exportation : {str(e)}")
                
    # Fonction pour éditer une cellule lors du double-clic
    def edit_cell(self, item):
        current_column = self.book_table.currentColumn()
        self.book_table.editItem(item, current_column)

        
    def rename_column(self, column):
        new_name, ok = QInputDialog.getText(self, "Renommer la colonne", f"Entrez un nouveau nom pour la colonne {column + 1}")
        if ok and new_name:
            self.book_table.headerItem().setText(column, new_name)
            
    def delete_selected_item(self):
        selected_item = self.book_table.currentItem()
        if selected_item is not None:
            self.book_table.takeTopLevelItem(self.book_table.indexOfTopLevelItem(selected_item))

>>>>>>> Stashed changes

        action = menu.exec_(self.book_table.mapToGlobal(pos))
        if action == copy_action:
            selected_item = self.book_table.currentItem()
            if selected_item is not None:
                clipboard = QApplication.clipboard()
                clipboard.setText(selected_item.text(self.book_table.currentColumn()))
        elif action == modify_action:
            selected_item = self.book_table.currentItem()
            if selected_item is not None:
                self.edit_cell(selected_item)
        elif action == delete_action:
            selected_item = self.book_table.currentItem()
            if selected_item is not None:
                # Vérifie si la case à cocher "Ne plus afficher" est déjà cochée
                never_show_checked = self.settings.value("NeverShowConfirmation", False, type=bool)
                if not never_show_checked:
                    confirmation_dialog = ConfirmationDialog("Êtes-vous sûr de vouloir supprimer cet élément ?")
                    result = confirmation_dialog.exec_()
                    if result == QDialog.Accepted:
                        should_hide_dialog = confirmation_dialog.never_show_checkbox.isChecked()
                        if should_hide_dialog:
                            self.settings.setValue("NeverShowConfirmation", True)  # Enregistrer le choix utilisateur
                        self.delete_selected_item()  # Appel à la fonction de suppression
                        confirmation_dialog.deleteLater()  # Supprimer la boîte de dialogue après utilisation
                else:
                    self.delete_selected_item()  # Si "Ne plus afficher" est déjà coché, supprime directement l'élément

<<<<<<< Updated upstream
    def update_book_table(self, books=None):
        self.book_table.clear()
        if not books:
            books = self.library.display_books()

        for book in books:
            item = QTreeWidgetItem(self.book_table)
            item.setText(0, str(book.book_id))
            item.setText(1, book.title)
            item.setText(2, book.author)
            item.setText(3, str(book.publisher))
            item.setText(4, book.isbn)
            item.setText(5, str(book.total_copies))
            item.setText(6, str(book.available_copies))

            # Rendre tous les éléments de cet item éditables
            for column in range(self.book_table.columnCount()):
                item.setFlags(item.flags() | Qt.ItemIsEditable)

    def take_book(self):
        book_id = self.entry_take.text()
        success, message = self.library.take_book_by_id(book_id)
        if success:
            QMessageBox.information(self, "Emprunt", message)
            self.update_book_table()
        else:
            QMessageBox.warning(self, "Emprunt impossible", message)

    def return_book(self):
        book_id = self.entry_return.text()
        success, message = self.library.return_book_by_id(book_id)
        if success:
            QMessageBox.information(self, "Retour", message)
            self.update_book_table()
        else:
            QMessageBox.warning(self, "Retour impossible", message)

    def remove_book(self):
        book_id = self.entry_remove.text()
        success, message = self.library.remove_book_by_id(book_id)
        if success:
            QMessageBox.information(self, "Suppression", message)
            self.update_book_table()
        else:
            QMessageBox.warning(self, "Suppression impossible", message)

    def import_from_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier CSV", "", "CSV Files (*.csv)")
        if file_path:
            success = self.library.import_from_csv(file_path)
            if success:
                QMessageBox.information(self, "Importation réussie", "Les livres ont été importés avec succès depuis le fichier CSV.")
                self.update_book_table()
            else:
                QMessageBox.critical(self, "Erreur d'importation", "Une erreur est survenue lors de l'importation depuis le fichier CSV.")
                
    def export_to_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Enregistrer le fichier CSV", "", "CSV Files (*.csv)")
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Title', 'Author', 'Publisher', 'ISBN', 'Total Copies'])
                    for book in self.library.display_books():
                        writer.writerow([book.title, book.author, book.isbn, book.available_copies])
                QMessageBox.information(self, "Exportation réussie", "Les données ont été exportées avec succès vers un fichier CSV.")
            except Exception as e:
                QMessageBox.critical(self, "Erreur d'exportation", f"Une erreur est survenue lors de l'exportation : {str(e)}")
    # Fonction pour éditer une cellule lors du double-clic
    def edit_cell(self, item):
        current_column = self.book_table.currentColumn()
        self.book_table.editItem(item, current_column)

        
    def rename_column(self, column):
        new_name, ok = QInputDialog.getText(self, "Renommer la colonne", f"Entrez un nouveau nom pour la colonne {column + 1}")
        if ok and new_name:
            self.book_table.headerItem().setText(column, new_name)
            
    def delete_selected_item(self):
        selected_item = self.book_table.currentItem()
        if selected_item is not None:
            self.book_table.takeTopLevelItem(self.book_table.indexOfTopLevelItem(selected_item))


    def search_books(self):
        query = self.entry_search.text()
        search_type = self.search_combobox.currentText()

        if search_type == "ISBN":
            books = self.library.display_books(query=query, by_isbn=True)
        elif search_type == "Titre":
            books = self.library.display_books(query=query, by_title=True)
        elif search_type == "Auteur":
            books = self.library.display_books(query=query, by_author=True)
        elif search_type == "Exemplaires":
            books = self.library.display_books(query=query, by_copies=True)
        else:
            books = self.library.display_books(query=query)

        self.update_book_table(books)

=======
>>>>>>> Stashed changes

def main():
    app = QApplication(sys.argv)
    
    # Définir les variables d'environnement pour gérer l'échelle des périphériques
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"  # Activer le facteur d'échelle par écran contrôlé par le plugin de la plateforme
    os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"  # Définir les DPI spécifiques pour chaque écran
    os.environ["QT_SCALE_FACTOR"] = "1"  # Définir le facteur d'échelle global pour l'application
    
    window = LibraryApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()