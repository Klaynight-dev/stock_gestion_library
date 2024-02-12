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
    QMenu, QCheckBox, QInputDialog, QTabWidget, QSizePolicy, QAction, QTextBrowser)
log_action(f"Importation de la biblioteque 'PyQt5.QtWidgets' avec comme fonction 'QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout,QHBoxLayout, QWidget, QComboBox, QMessageBox, QFileDialog, QTreeWidget,QTreeWidgetItem, QTableWidgetItem, QHeaderView, QDialog, QAbstractItemView, QMenu, QCheckBox, QInputDialog, QTabWidget, QSizePolicy, QAction, QTextBrowser'", success=True)
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
from library_logic import *
log_action(f"Importation du fichier 'library_logic.py'", success=True)
from user_logic import *
log_action(f"Importation du fichier 'user_logic.py'", success=True)
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
        self.setWindowIcon(QIcon('icon.png'))

        # Create a central widget to hold the layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Apply CSS styles to certain components
        self.setStyleSheet(load_stylesheet('content\\css\\style.css'))

        # Create a main layout for the central widget
        self.layout = QVBoxLayout(self.central_widget)

        # Determine the current directory
        current_dir = os.path.dirname(os.path.realpath(__file__))

        self.file_path = None
        self.file_path_book = None
        self.file_path_user = None
        self.file_path_take = None

        # Display the logo in the banner
        self.logo_label = QLabel(self)
        self.pixmap = QPixmap(os.path.join(current_dir, 'icon.png'))
        self.logo_label.setPixmap(self.pixmap)

        self.settings = QSettings("Jobi", "gestion_library_app")

        self.library = Library()
        self.user_gestion = User_gestion()

        # Create a tab widget without specifying geometry
        self.tab_widget = QTabWidget(self.central_widget)
        self.tab_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Books Tab
        self.books_tab = QWidget()
        books_layout = QVBoxLayout()
        self.setup_search_section()
        self.setup_table("book_table",7,["ID", "Titre", "Auteur", "Maison d'édition", "ISBN", "Exemplaires", "Exemplaires Disponibles"])
        self.book_table.itemChanged.connect(self.update_book_info)
        books_layout.addWidget(self.book_table)
        self.books_tab.setLayout(books_layout)
        self.tab_widget.addTab(self.books_tab, "Gestion des Livres")

        # Users Tab
        self.users_tab = QWidget()
        user_layout = QVBoxLayout()
        self.setup_user_tab()
        self.user_table.itemChanged.connect(self.update_user_info)
        self.users_tab.setLayout(user_layout)
        self.tab_widget.addTab(self.users_tab, "Gestion des Utilisateurs")

        # Take Tab
        self.take_tab = QWidget()
        take_layout = QVBoxLayout()
        self.setup_take_tab()
        self.take_tab.setLayout(take_layout)
        self.tab_widget.addTab(self.take_tab, "Gestion des Empreints")

        # Set up stretch factors to prioritize the content in the layout
        self.layout.addWidget(self.tab_widget, stretch=1)

        # Load saved CSV data
        self.load_saved_csv()

        # Add the bottom layout to the central layout
        self.layout.addLayout(self.setup_bottom_layout())

        # Initialize bottom_layout as an instance attribute
        self.bottom_layout = None

        self.tab_widget.currentChanged.connect(self.onTabChanged)

        self.create_menu()
        
         #Zone de text pour n'import quelle fonctionnalisté
#         self.text_browser = QTextBrowser(self)
#         books_layout.addWidget(self.text_browser)
    
    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
    
    def create_menu(self):
        # Menu Fichier
        file_menu = self.menuBar().addMenu("Fichier")
        
        open_action = QAction(QIcon(), "Importer", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.import_from_csv)
        log_action("Importation d'un fichier depuis le menu fichier")
        file_menu.addAction(open_action)

#         save_action = QAction(QIcon(), "Enregistrer", self)
#         save_action.setShortcut("Ctrl+S")
#         save_action.triggered.connect(self.)
#         file_menu.addAction(save_action)

        save_as_action = QAction(QIcon(), "Enregistrer sous", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.export_to_csv)
        log_action("Exportation du fichier depuis le menu fichier")
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        print_action = QAction(QIcon(), "Imprimer toute la librairie", self)
        print_action.setShortcut("Ctrl+P")
        print_action.triggered.connect(self.print_all_files)
        log_action("Impression de la librairie depuis le menu fichier")
        file_menu.addAction(print_action)
        
        print_action = QAction(QIcon(), "Imprimer un livre par ID", self)
        print_action.setShortcut("Ctrl+Shift+p")
        print_action.triggered.connect(self.print_selected_file)
        log_action("Impression d'un livre depuis le menu fichier")
        file_menu.addAction(print_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction(QIcon(), "Quitter", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        log_action("Fermeture de l'application depuis le menu fichier")
        file_menu.addAction(quit_action)
        
        
        # Menu Option
        file_menu = self.menuBar().addMenu("Option")
        
        fullscreen = QAction(QIcon(), "Pleine écran", self)
        fullscreen.setShortcut("F11")
        fullscreen.triggered.connect(self.toggle_fullscreen)
        log_action("Mise en pleine écrant/Mise en fenétré")
        file_menu.addAction(fullscreen)
        
        # Menu Édition
#         edit_menu = self.menuBar().addMenu("Édition")
# 
#         undo_action = QAction(QIcon(), "Annuler", self)
#         undo_action.setShortcut("Ctrl+Z")
#         undo_action.triggered.connect(self.text_edit.undo)
#         edit_menu.addAction(undo_action)
# 
#         redo_action = QAction(QIcon(), "Rétablir", self)
#         redo_action.setShortcut("Ctrl+Y")
#         redo_action.triggered.connect(self.text_edit.redo)
#         edit_menu.addAction(redo_action)
# 
#         copy_action = QAction(QIcon(), "Copier", self)
#         copy_action.setShortcut("Ctrl+C")
#         copy_action.triggered.connect(self.text_edit.copy)
#         edit_menu.addAction(copy_action)
# 
#         paste_action = QAction(QIcon(), "Coller", self)
#         paste_action.setShortcut("Ctrl+V")
#         paste_action.triggered.connect(self.text_edit.paste)
#         edit_menu.addAction(paste_action)
        
    def print_all_files(self):
        QMessageBox.information(self, "En développement", "Cette fonctionnalité est en cours de développement")
#         if self.tab_widget.currentIndex()==0:
#             # Imprimer tous les livres
#             self.print_files(self.library.books)

    def print_selected_file(self):
        if self.tab_widget.currentIndex()==0:
            # Demander à l'utilisateur d'entrer l'ID du livre
            book_id, ok = QInputDialog.getText(self, 'Entrer l\'ID du livre', 'ID du livre:')
            if ok:
                if book_id:
                    book = self.library.get_book_by_id(book_id)
                    if book:
                        self.print_files([book])
                    else:
                        self.text_browser.setText(f"Aucun livre trouvé avec l'ID {book_id}")
                else:
                    self.text_browser.setText("Veuillez spécifier un ID de livre")

    def print_files(self, books):
        if self.tab_widget.currentIndex() == 0:
            # Demander à l'utilisateur où enregistrer le fichier PDF
            file_path, _ = QFileDialog.getSaveFileName(self, 'Enregistrer le PDF', '', 'PDF Files (*.pdf)')
            if not file_path:
                return  # L'utilisateur a annulé la sauvegarde

            try:
                # Créer un fichier PDF avec la bibliothèque reportlab
                pdf = canvas.Canvas(file_path, pagesize=letter)
                pdf.setFont("Helvetica", 12)

                # Imprimer les détails des livres dans le PDF
                for book in books:
                    pdf.drawString(100, 750, f"Book ID: {book.book_id}")
                    pdf.drawString(100, 730, f"Title: {book.title}")
                    pdf.drawString(100, 710, f"Author: {book.author}")
                    pdf.drawString(100, 690, f"ISBN: {book.isbn}")
                    pdf.drawString(100, 670, f"Total Copies: {book.total_copies}")
                    pdf.drawString(100, 650, f"Available Copies: {book.available_copies}")
                    pdf.drawString(100, 630, f"Publisher: {book.publisher}")
                    pdf.drawString(100, 610, "\n")

                # Sauvegarder et fermer le fichier PDF
                pdf.save()

                # Afficher une boîte de dialogue pour indiquer que le PDF a été créé avec succès
                QMessageBox.information(self, "PDF Créé", "Le PDF a été créé avec succès.", QMessageBox.Ok)

                # Journaliser l'action
                log_action(f"Création du fichier PDF réussie : {file_path}", success=True)
            except Exception as e:
                # Journaliser l'erreur en cas d'échec
                log_action(f"Erreur lors de la création du fichier PDF : {str(e)}", success=False)

        
    def onTabChanged(self, index):
        if index == 0:
            new_text = 'Ajouter un livre'
            self.btn_open_add_book_dialog.setText(new_text)
            log_action('Changement d\'onglet vers \'Ajouter un livre\'', success=True)
            self.setWindowTitle(f"Jobi - {self.file_path_book if self.file_path_book!=None else 'Gestionnaire de bibliothèque'}")
            log_action(f"Changement du Windows Title par 'Jobi - {self.file_path_book if self.file_path_book!=None else 'Gestionnaire de bibliothèque'}'")
        elif index == 1:
            new_text = 'Ajouter un utilisateur'
            self.btn_open_add_book_dialog.setText(new_text)
            log_action('Changement d\'onglet vers \'Ajouter un utilisateur\'', success=True)
            self.setWindowTitle(f"Jobi - {self.file_path_user if self.file_path_user!=None else 'Gestionnaire de bibliothèque'}")
            log_action(f"Changement du Windows Title par 'Jobi - {self.file_path_user if self.file_path_user!=None else 'Gestionnaire de bibliothèque'}'")
        elif index == 2:
            new_text = 'Ajouter un emprunt'
            self.btn_open_add_book_dialog.setText(new_text)
            log_action('Changement d\'onglet vers \'Ajouter un emprunt\'', success=True)
            self.setWindowTitle(f"Jobi - {self.file_path_take if self.file_path_take!=None else 'Gestionnaire de bibliothèque'}")
            log_action(f"Changement du Windows Title par 'Jobi - {self.file_path_take if self.file_path_take!=None else 'Gestionnaire de bibliothèque'}'")
            
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

        search_options = ["Titre", "Auteur", "Maison d'édition", "ISBN", "Exemplaires", "Exemplaires Diponibles", "ID"]
        self.search_combobox.addItems(search_options)
        self.search_combobox.currentIndexChanged.connect(self.search_books)
        search_layout.addWidget(self.search_type_label)
        search_layout.addWidget(self.search_combobox)

        self.layout.addLayout(search_layout)
        
    def setup_table(self, val_name, colomn_nbr, colomn_names):
        # Utilisez setattr pour créer dynamiquement un attribut d'instance avec le nom spécifié
        setattr(self, val_name, QTreeWidget())

        # Utilisez l'attribut d'instance pour accéder à votre QTreeWidget
        getattr(self, val_name).setColumnCount(colomn_nbr)
        getattr(self, val_name).setHeaderLabels(colomn_names)
#         getattr(self, val_name).setSortingEnabled(True) # A resoudre pour eviter le mauvais rangement 

        header = getattr(self, val_name).header()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        # Ajoutez le QTreeWidget au layout de votre classe
        self.layout.addWidget(getattr(self, val_name))

        # Rendre tous les éléments éditables dans le tableau
        getattr(self, val_name).setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked | QAbstractItemView.EditKeyPressed)

        # Activer la détection du clic droit pour le menu contextuel
        getattr(self, val_name).setContextMenuPolicy(Qt.CustomContextMenu)
        getattr(self, val_name).customContextMenuRequested.connect(self.show_user_context_menu)
        

    def setup_user_tab(self):
        # Set up the user management components in the users tab
        user_layout = QVBoxLayout()

        # Set up the user management table and related components in the users tab
        self.setup_table("user_table", 6,["ID", "Nom", "Prénom", "Email", "Addresse", "Nombre d'Empreint"])
        self.user_table.itemChanged.connect(self.update_user_info)

        user_layout.addWidget(self.user_table)

        self.users_tab.setLayout(user_layout)

    def show_user_context_menu(self, pos):
        menu = QMenu(self)
        copy_action = menu.addAction("Copier")
        delete_action = menu.addAction("Supprimer")
        modify_action = menu.addAction("Modifier")

        action = menu.exec_(self.user_table.mapToGlobal(pos))
        if action == copy_action:
            selected_item = self.user_table.currentItem()
            if selected_item is not None:
                clipboard = QApplication.clipboard()
                clipboard.setText(selected_item.text(self.user_table.currentColumn()))
        elif action == modify_action:
            selected_item = self.user_table.currentItem()
            if selected_item is not None:
                self.edit_cell(selected_item)
        elif action == delete_action:
            selected_item = self.user_table.currentItem()
            if selected_item is not None:
                log_action(f"Tentative de suppression de l'utilisateur avec l'ID={selected_item.text(0)}", success=True)
                # Handle deletion confirmation and process similarly to books if needed

    def update_user_info(self):
        try:
            selected_items = self.user_table.selectedItems()
            for item in selected_items:
                user_id = int(item.text(0))
                user = self.user_gestion.get_user_by_id(user_id)

                column = self.user_table.currentColumn()
                column_name = self.user_table.headerItem().text(column)  # Récupération du nom de la colonne

                # Mettre à jour les détails de l'utilisateur selon la colonne
                # Example: if column == 1: user.name = new_value
                # ...

                # Appel à la méthode de la classe Library pour mettre à jour les détails de l'utilisateur
                # self.library.update_user_details(user)
                # ...

                # Log action pour indiquer la modification de la colonne
                log_action(f"Modification sur la colonne '{column_name}': 'old_value' -> 'new_value'", success=True)

        except Exception as e:
            # Enregistrement de l'erreur dans les logs
            log_action(f"Erreur lors de la mise à jour des détails de l'utilisateur : {str(e)}", success=False)
            print("Une erreur s'est produite :", e)
    
    def setup_take_table(self):
        self.take_table = QTreeWidget()
        self.take_table.setColumnCount(3)  # Adjust the number of columns as needed
        self.take_table.setHeaderLabels(["ID", "ID du livre", "Titre", "Auteur", "ISBN", "ID de l'empreinteur", "Nom de l'empreinteur", "Prénom de l'empreinteur"])
        header = self.take_table.header()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.layout.addWidget(self.take_table)

        # Rendre tous les éléments éditables dans le tableau
        self.take_table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked | QAbstractItemView.EditKeyPressed)

        # Activer la détection du clic droit pour le menu contextuel
        self.take_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.take_table.customContextMenuRequested.connect(self.show_take_context_menu)

    def setup_take_tab(self):
        # Set up the user management components in the users tab
        take_layout = QVBoxLayout()

        # Set up the user management table and related components in the users tab
        self.setup_take_table()
        self.take_table.itemChanged.connect(self.update_take_info)

        take_layout.addWidget(self.take_table)

        self.take_tab.setLayout(take_layout)

    def show_take_context_menu(self, pos):
        menu = QMenu(self)
        copy_action = menu.addAction("Copier")
        delete_action = menu.addAction("Supprimer")
        modify_action = menu.addAction("Modifier")

        action = menu.exec_(self.take_table.mapToGlobal(pos))
        if action == copy_action:
            selected_item = self.take_table.currentItem()
            if selected_item is not None:
                clipboard = QApplication.clipboard()
                clipboard.setText(selected_item.text(self.take_table.currentColumn()))
        elif action == modify_action:
            selected_item = self.take_table.currentItem()
            if selected_item is not None:
                self.edit_take_cell(selected_item)
        elif action == delete_action:
            selected_item = self.take_table.currentItem()
            if selected_item is not None:
                log_action(f"Tentative de suppression de l'empreint avec l'ID={selected_item.text(0)}", success=True)
                # Handle deletion confirmation and process similarly to books if needed

    def update_take_info(self):
        try:
            selected_items = self.take_table.selectedItems()
            for item in selected_items:
                take_id = int(item.text(0))
                take = self.library.get_take_by_id(take_id)

                column = self.user_table.currentColumn()
                column_name = self.user_table.headerItem().text(column)  # Récupération du nom de la colonne

                # Mettre à jour les détails de l'utilisateur selon la colonne
                # Example: if column == 1: take.name = new_value
                # ...

                # Appel à la méthode de la classe Library pour mettre à jour les détails de l'empreint
                # self.library.update_take_details(take)
                # ...

                # Log action pour indiquer la modification de la colonne
                log_action(f"Modification sur la colonne '{column_name}': 'old_value' -> 'new_value'", success=True)

        except Exception as e:
            # Enregistrement de l'erreur dans les logs
            log_action(f"Erreur lors de la mise à jour des détails de l'empreint : {str(e)}", success=False)
            print("Une erreur s'est produite :", e)
    
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
        
#         self.current = QPushButton("onglet")
#         self.current.clicked.connect(self.currentonglet)
#         self.import_export_layout.addWidget(self.current)

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
    
#     def currentonglet(self):
#         print(self.tab_widget.currentIndex())
    
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
    
    def update_user_table(self, users=None):
        self.user_table.clear()
        if not users:
            users = self.user_gestion.display_users()

        for user in users:
            item = QTreeWidgetItem(self.user_table)
            item.setText(0, str(user.user_id))
            item.setText(1, user.fname)
            item.setText(2, user.name)
            item.setText(3, str(user.mail))
            item.setText(4, user.take)

            # Rendre tous les éléments de cet item éditables
            for column in range(self.user_table.columnCount()):
                item.setFlags(item.flags() | Qt.ItemIsEditable)

    def take_book(self):
        current_tab_index = self.tab_widget.currentIndex()
        if current_tab_index == 0:
            book_id = self.entry_take.text()
            if book_id=='':
                log_action("Aucune ID de livre n'a été défini !", success=False, error_message="ID non défini")
                QMessageBox.warning(self, "ID non défini", "Aucune ID de livre n'a été défini !")
                
            else:
                success, message = self.library.take_book_by_id(book_id)
                if success:
                    # Enregistrement de l'action dans les logs
                    log_action(f"Emprunt d'un livre avec l'ID={book_id}", success=True)
                    QMessageBox.information(self, "Emprunt", message)
                    self.update_book_table()
                else:
                    # Enregistrement de l'erreur dans les logs
                    log_action(f"Erreur lors de l'emprunt d'un livre avec l'ID={book_id}: {str(message)}", success=False)
                    QMessageBox.warning(self, "Emprunt impossible", message)
    
    def return_book(self):
        current_tab_index = self.tab_widget.currentIndex()
        if current_tab_index == 0:
            book_id = self.entry_return.text()
            if book_id=='':
                log_action("Aucune ID de livre n'a été défini !", success=False, error_message="ID non défini")
                QMessageBox.warning(self, "ID non défini", "Aucune ID de livre n'a été défini !")
                
            else:
                success, message = self.library.return_book_by_id(book_id)
                if success:
                    # Enregistrement de l'action dans les logs
                    log_action(f"Retour d'un livre avec l'ID={book_id}", success=True)
                    QMessageBox.information(self, "Retour", message)
                    self.update_book_table()
                else:
                    # Enregistrement de l'erreur dans les logs
                    log_action(f"Erreur lors du retour d'un livre avec l'ID={book_id}: {str(message)}", success=False)
                    QMessageBox.warning(self, "Retour impossible", message)

    def remove_book(self):
        current_tab_index = self.tab_widget.currentIndex()
        if current_tab_index == 0:
            book_id = self.entry_remove.text()
            if book_id=='':
                log_action("Aucune ID de livre n'a été défini !", success=False, error_message="ID non défini")
                QMessageBox.warning(self, "ID non défini", "Aucune ID de livre n'a été défini !")
                
            else:
                success, message = self.library.remove_book_by_id(book_id)
                if success:
                    # Enregistrement de l'action dans les logs
                    log_action(f"Suppression d'un livre avec l'ID={book_id}", success=True)
                    QMessageBox.information(self, "Suppression", message)
                    self.update_book_table()
                else:
                    # Enregistrement de l'erreur dans les logs
                    log_action(f"Erreur lors de la suppression d'un livre avec l'ID={book_id}: {str(message)}", success=False)
                    QMessageBox.warning(self, "Suppression impossible", message)
        
    def delete_selected_item(self):
        current_tab_index = self.tab_widget.currentIndex()
        if current_tab_index == 0:
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
        current_tab_index = self.tab_widget.currentIndex()
        if current_tab_index == 0:
            new_book_id = None  # Initialisation de new_book_id en dehors du bloc try

            try:
                file_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier CSV", "", "CSV Files (*.csv)")
                self.setWindowTitle(f"Jobi - {file_path}")
                log_action(f"Changement du Windows Title par 'Jobi - {file_path}'")
                self.file_path_book = file_path
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
        
        if current_tab_index == 1:
            new_user_id = None  # Initialisation de new_user_id en dehors du bloc try

            try:
                file_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier CSV", "", "CSV Files (*.csv)")
                self.setWindowTitle(f"Jobi  -  {file_path}")
                self.file_path_user = file_path
                log_action(f"Modification de la banniere superieur par : {file_path}", success=False)
                if file_path:
                    success = self.user_gestion.import_from_csv(file_path)
                    if success:
                        # Enregistrement de l'action dans les logs
                        log_action("Importation réussie depuis un fichier CSV", success=True)
                        QMessageBox.information(self, "Importation réussie", "Les utilisateurs ont été importés avec succès depuis le fichier CSV.")
                        self.update_user_table()
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
        current_tab_index = self.tab_widget.currentIndex()

        try:
            if current_tab_index == 0:  # Export books
                file_path, _ = QFileDialog.getSaveFileName(self, "Enregistrer le fichier CSV", "", "CSV Files (*.csv)")
                if file_path:
                    with open(file_path, 'w', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow(['Title', 'Author', 'Publisher', 'ISBN', 'Total Copies'])
                        for book in self.library.display_books():
                            writer.writerow([book.title, book.author, book.publisher, book.isbn, book.available_copies])
                    log_action("Exportation réussie des livres vers un fichier CSV", success=True)
                    QMessageBox.information(self, "Exportation réussie", "Les données des livres ont été exportées avec succès vers un fichier CSV.")
                    
            elif current_tab_index == 1:  # Export users
                file_path, _ = QFileDialog.getSaveFileName(self, "Enregistrer le fichier CSV", "", "CSV Files (*.csv)")
                if file_path:
                    with open(file_path, 'w', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow(['Fname', 'Name', 'Email', 'Address', 'Empreint'])
                        for user in self.user_gestion.display_users():
                            writer.writerow([user.fname, user.name, user.mail, user.address, user.take])
                    log_action("Exportation réussie des utilisateurs vers un fichier CSV", success=True)
                    QMessageBox.information(self, "Exportation réussie", "Les données des utilisateurs ont été exportées avec succès vers un fichier CSV.")

        except Exception as e:
            log_action(f"Erreur lors de l'exportation vers un fichier CSV : {str(e)}", success=False)
            QMessageBox.critical(self, "Erreur d'exportation", f"Une erreur est survenue lors de l'exportation : {str(e)}")

        
    def export_save_to_csv(self, file_path, books):
        current_tab_index = self.tab_widget.currentIndex()
        if current_tab_index == 0:
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
        current_tab_index = self.tab_widget.currentIndex()
        if current_tab_index==0:
            current_column = self.book_table.currentColumn()
            self.book_table.editItem(item, current_column)
            
        if current_tab_index==1:
            current_column = self.user_table.currentColumn()
            self.user_table.editItem(item, current_column)
            
        if current_tab_index==2:
            current_column = self.take_table.currentColumn()
            self.take_table.editItem(item, current_column)
        
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
        elif search_type == "Exemplaires Disponible":
            books = self.library.display_books(query=query, by_available_copies=True)
        elif search_type == "Exemplaires":
            books = self.library.display_books(query=query, by_total_copies=True)
        elif search_type == "Maison d'édition":
            books = self.library.display_books(query=query, by_publisher=True)
        elif search_type == "ID":
            books = self.library.display_books(query=query, by_ID=True)
        
        else:
            books = self.library.display_books(query=query)

        self.update_book_table(books)
    #"Titre", "Auteur", "Maison d'édition", "ISBN", "Exemplaires", "Exemplaires Diponibles", "ID"

def main():
    app = QApplication(sys.argv)
    
    window = LibraryApp()
    window.load_saved_csv()  # Chargement du fichier CSV sauvegardé
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
