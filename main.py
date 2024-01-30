# main.py

from logs import *
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
    QMenu, QCheckBox, QInputDialog, QTabWidget, QSizePolicy)
log_action(f"Importation de la biblioteque 'PyQt5.QtWidgets' avec comme fonction 'QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout,QHBoxLayout, QWidget, QComboBox, QMessageBox, QFileDialog, QTreeWidget,QTreeWidgetItem, QTableWidgetItem, QHeaderView, QDialog, QAbstractItemView, QMenu, QCheckBox, QInputDialog, QTabWidget, QSizePolicy'", success=True)
from PyQt5.QtGui import (QPixmap, QIcon)
log_action(f"Importation de la biblioteque 'PyQt5.QtGui' avec comme fonction 'QPixmap, QIcon'", success=True)
from PyQt5.QtCore import Qt, QSettings
log_action(f"Importation de la biblioteque 'PyQt5.QtCore' avec comme fonction 'Qt, QSettings'", success=True)
from library_logic import *
log_action(f"Importation du fichier 'library_logic.py'", success=True)
from dialog_logic import *
log_action(f"Importation du fichier 'dialog_logic.py'", success=True)

def load_stylesheet(file_path):
    with open(file_path, 'r') as file:
        return file.read()

class LibraryApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Jobi - Gestionnaire de bibliothèque")
        self.setGeometry(100, 100, 800, 500)

        # Create a central widget to hold the layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Apply CSS styles to certain components
        self.setStyleSheet(load_stylesheet('content\css\style.css'))

        # Create a main layout for the central widget
        self.layout = QVBoxLayout(self.central_widget)

        # Determine the current directory
        current_dir = os.path.dirname(os.path.realpath(__file__))

        self.file_path = None

        # Set the application icon in the taskbar
        self.setWindowIcon(QIcon('icon.png'))

        # Display the logo in the banner
        self.logo_label = QLabel(self)
        self.pixmap = QPixmap(os.path.join(current_dir, 'icon.png'))
        self.logo_label.setPixmap(self.pixmap)

        self.settings = QSettings("Jobi", "gestion_library_app")

        self.library = Library()

        # Create a tab widget without specifying geometry
        self.tab_widget = QTabWidget(self.central_widget)

        # Set the size policy to Expanding
        self.tab_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Books Tab
        self.books_tab = QWidget()

        # Set up the book management components in the books tab
        books_layout = QVBoxLayout()

        self.setup_search_section()
        self.setup_book_table()

        self.book_table.itemChanged.connect(self.update_book_info)

        books_layout.addWidget(self.book_table)

        # Add more book management-related components if needed

        self.books_tab.setLayout(books_layout)
        self.tab_widget.addTab(self.books_tab, "Gestion des Livres")

        # Users Tab
        self.users_tab = QWidget()
        user_layout = QVBoxLayout()

        # Add user-specific widgets and functionality here
        self.users_tab.setLayout(user_layout)
        self.tab_widget.addTab(self.users_tab, "Gestion des Utilisateurs")

        # Set up stretch factors to prioritize the content in the layout
        self.layout.addWidget(self.tab_widget, stretch=1)

        # Add the borrow/return/remove sections directly to the main layout
        self.layout.addStretch(1)

        # Load saved CSV data
        self.load_saved_csv()

        # Add the bottom layout to the central layout
        self.layout.addLayout(self.setup_bottom_layout())

        # Initialize bottom_layout as an instance attribute
        self.bottom_layout = None

            
    def closeEvent(self, event):
        # Sauvegarde du fichier CSV avant de fermer l'application
        log_action("Fermeture de l'application. Tentative de sauvegarde...")
        try:
            save_directory = os.path.join("data", "save")
            os.makedirs(save_directory, exist_ok=True)  # Création du répertoire de sauvegarde s'il n'existe pas
            save_path = os.path.join(save_directory, "saved_books.csv")
            self.export_save_to_csv(save_path, librairy.books)  # Utilisation de la fonction d'exportation existante
        except Exception as e:
            log_action(f"Erreur lors de la sauvegarde du fichier : {str(e)}", False, str(e))
            print(f"Erreur lors de la sauvegarde du fichier : {str(e)}", False, str(e))

    def load_saved_csv(self):
        saved_file_path = os.path.join("data", "save", "saved_books.csv")
        if os.path.exists(saved_file_path):
            self.file_path = saved_file_path
            books = self.library.import_from_csv(saved_file_path)
            print(books)  # Ajoutez ce print pour vérifier les données chargées depuis le CSV
            self.update_book_table()
        else:
            log_action("Aucun fichier sauvegardé trouvé.", False)


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
        
        # Activer la détection du clic droit pour le menu contextuel
        self.book_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.book_table.customContextMenuRequested.connect(self.show_context_menu)
        
        # Détection du double-clic sur l'en-tête de colonne pour le renommage
        header = self.book_table.header()
        header.sectionDoubleClicked.connect(self.rename_column)
        
    def setup_books_tab(self):
        # Set up the book management components in the books tab
        books_layout = QVBoxLayout()

        # Set up the book management table and related components in the books tab
        self.setup_search_section()
        self.setup_book_table()
        self.setup_borrow_return_remove_sections()
        self.setup_import_export_buttons()
        self.book_table.itemChanged.connect(self.update_book_info)

        books_layout.addWidget(self.book_table)

        self.books_tab.setLayout(books_layout)

    def setup_user_tab(self):
        # Set up the user management components in the users tab
        user_layout = QVBoxLayout()

        # Add user-specific widgets and functionality here
        # Example: user_label = QLabel("User ID:")
        #          user_entry = QLineEdit()
        #          user_layout.addWidget(user_label)
        #          user_layout.addWidget(user_entry)

        self.users_tab.setLayout(user_layout)
    
    def setup_borrow_return_remove_sections(self):
        # Add the borrow/return/remove sections directly to the main layout
        self.setup_borrow_return_remove_buttons()
        self.setup_import_export_buttons()
    
    def setup_borrow_return_remove_buttons(self):
        borrow_return_layout = QHBoxLayout()

        self.borrow_label = QLabel("ID à emprunter:")
        self.return_label = QLabel("ID à retourner:")
        self.btn_take   = QPushButton("Emprunter")
        self.btn_return = QPushButton("Retourner")
        
        self.entry_take = QLineEdit()
        self.entry_return = QLineEdit()
        
        self.btn_take.clicked.connect(self.take_book)
        
        borrow_return_layout.addWidget(self.borrow_label)
        borrow_return_layout.addWidget(self.entry_take)

        borrow_return_layout.addWidget(self.btn_take)

        borrow_return_layout.addWidget(self.return_label)
        borrow_return_layout.addWidget(self.entry_return)

        
        self.btn_return.clicked.connect(self.return_book)
        borrow_return_layout.addWidget(self.btn_return)

        self.remove_label = QLabel("ID à supprimer:")
        self.entry_remove = QLineEdit()
        borrow_return_layout.addWidget(self.remove_label)
        borrow_return_layout.addWidget(self.entry_remove)

        self.btn_remove = QPushButton("Supprimer livre")
        self.btn_remove.clicked.connect(self.remove_book)
        borrow_return_layout.addWidget(self.btn_remove)

        # Add the borrow/return/remove layout to the main layout
        self.layout.addLayout(borrow_return_layout)
        
    def setup_bottom_layout(self):
        # Create a layout for the buttons at the bottom
        self.bottom_layout = QHBoxLayout()

        # Add the borrow, return, and remove buttons to the bottom layout
        self.setup_borrow_return_remove_buttons()

        # Add the import and export buttons to the bottom layout
        self.setup_import_export_buttons()

        # Add stretch factor to push buttons to the right
        self.bottom_layout.addStretch(1)

        return self.bottom_layout

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
                book_id = int(item.text(0))
                book = self.library.get_book_by_id(book_id)

                column = self.book_table.currentColumn()
                column_name = self.book_table.headerItem().text(column)  # Récupération du nom de la colonne

                # Mettre à jour les détails du livre selon la colonne
                if column == 1:  # Supposez que la colonne 1 correspond au titre du livre
                    old_value = book.title
                    new_value = item.text(column)
                    book.title = new_value
                elif column == 2:  # Colonne pour l'auteur
                    old_value = book.author
                    new_value = item.text(column)
                    book.author = new_value
                elif column == 3:  # Colonne pour la maison d'édition
                    old_value = book.publisher
                    new_value = item.text(column)
                    book.publisher = new_value
                elif column == 4:  # Colonne pour l'ISBN
                    old_value = book.isbn
                    new_value = item.text(column)
                    book.isbn = new_value
                elif column == 5:  # Colonne pour le nombre total d'exemplaires
                    old_value = book.total_copies
                    new_value = int(item.text(column))
                    book.total_copies = new_value
                elif column == 6:  # Colonne pour le nombre d'exemplaires disponibles
                    old_value = book.available_copies
                    new_value = int(item.text(column))
                    book.available_copies = new_value
                    # Mise à jour du nombre d'exemplaires disponibles si nécessaire
                    # book.available_copies = ... (calcul pour déterminer les exemplaires disponibles)

                # Appel à la méthode de la classe Library pour mettre à jour les détails du livre
                self.library.update_book_details(book)
                self.update_book_table()
                
                # Log action pour indiquer la modification de la colonne
                log_action(f"Modification sur la colonne '{column_name}': '{old_value}' -> '{new_value}'", success=True)

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
            # Utilisez la fonction remove_book_by_id de la bibliothèque pour supprimer l'élément
            success, message = self.library.remove_book_by_id(book_id)
            if success:
                # Enregistrement de l'action dans les logs
                log_action(f"Suppression d'un livre avec l'ID={book_id}", success=True)
                QMessageBox.information(self, "Suppression", message)
                self.update_book_table()  # Mettre à jour l'interface utilisateur après la suppression
            else:
                # Enregistrement de l'erreur dans les logs
                log_action(f"Erreur lors de la suppression d'un livre avec l'ID={book_id}: {message}", success=False)
                QMessageBox.warning(self, "Suppression impossible", message)

    def import_from_csv(self):
        new_book_id = None  # Initialisation de new_book_id en dehors du bloc try

        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier CSV", "", "CSV Files (*.csv)")
            self.setWindowTitle(f"Jobi  -  {file_path}")
            log_action(f"Modification de la banniere superieur par : {file_path}", success=False)
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
    
    def export_save_to_csv(self, file_path, books):
        # Exporter les données des livres dans un fichier CSV
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['ID', 'Title', 'Author', 'Publisher', 'ISBN', 'Total Copies', 'Available Copies'])

                for book in books:
                    writer.writerow([
                        book.book_id,
                        book.title,
                        book.author,
                        book.publisher,
                        book.isbn,
                        book.total_copies,
                        book.available_copies
                    ])

            log_action(f"Sauvegarde réussie vers {file_path}", success=True)
        except Exception as e:
            log_action(f"Erreur lors de la sauvegarde du fichier : {str(e)}", False, str(e))

    
    # Fonction d'importation depuis un fichier CSV save
    def import_save_from_csv(self, file_path):
        try:
            success = self.library.import_from_csv(file_path)
            if success:
                # Enregistrement de l'action dans les logs
                log_action("Importation réussie depuis un fichier CSV", success=True)
                QMessageBox.information(self, "Importation réussie", "Les livres ont été importés avec succès depuis le fichier CSV.")
            else:
                # Enregistrement de l'erreur dans les logs
                log_action("Erreur lors de l'importation depuis un fichier CSV", success=False)
                QMessageBox.critical(self, "Erreur d'importation", "Une erreur est survenue lors de l'importation depuis le fichier CSV.")
        except Exception as e:
            # Enregistrement de l'erreur dans les logs
            log_action(f"Erreur lors de l'importation depuis un fichier CSV : {str(e)}", success=False)
            # Gérer l'erreur (affichage d'un message à l'utilisateur ou autre)
            QMessageBox.critical(self, "Erreur d'importation", "Une erreur est survenue lors de l'importation depuis le fichier CSV.")

    
    # Fonction pour éditer une cellule lors du double-clic
    def edit_cell(self, item):
        current_column = self.book_table.currentColumn()
        self.book_table.editItem(item, current_column)

        
    def rename_column(self, column):
        new_name, ok = QInputDialog.getText(self, "Renommer la colonne", f"Entrez un nouveau nom pour la colonne {column + 1}")
        if ok and new_name:
            self.book_table.headerItem().setText(column, new_name)


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


def main():
    app = QApplication(sys.argv)
    
    # Définir les variables d'environnement pour gérer l'échelle des périphériques
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"  # Activer le facteur d'échelle par écran contrôlé par le plugin de la plateforme
    os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"  # Définir les DPI spécifiques pour chaque écran
    os.environ["QT_SCALE_FACTOR"] = "1"  # Définir le facteur d'échelle global pour l'application
    
    window = LibraryApp()
    window.load_saved_csv()  # Chargement du fichier CSV sauvegardé
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
