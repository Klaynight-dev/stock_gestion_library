from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QWidget, QComboBox, QMessageBox, QFileDialog, QTreeWidget,
    QTreeWidgetItem, QTableWidgetItem, QHeaderView, QDialog, QAbstractItemView, QMenu, QCheckBox, QInputDialog)
from logs import *
from library_logic import *

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
            log_action(f"Ajout d'un livre : ID={new_book_id}, Titre='{title}', Auteur='{author}', ISBN='{isbn}'", success=True)
            books = self.library_app.library.display_books()
            self.library_app.update_book_table(books)

            # Effacer les champs après l'ajout du livre
            self.entry_title.clear()
            self.entry_author.clear()
            self.entry_publisher.clear()
            self.entry_isbn.clear()
            self.entry_copies.clear()
            
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
