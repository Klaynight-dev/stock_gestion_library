from tools.logs import *
from PyQt5.QtWidgets import QAction, QMenuBar
from PyQt5.QtGui import QIcon

def create_menu(window):
    # Menu Fichier
    file_menu = window.menuBar().addMenu("Fichier")
    
    open_action = QAction(QIcon(), "Importer", window)
    open_action.setShortcut("Ctrl+O")
    open_action.triggered.connect(window.import_from_csv)
    log_action("Importation d'un fichier depuis le menu fichier")
    file_menu.addAction(open_action)

    # save_action = QAction(QIcon(), "Enregistrer", window)
    # save_action.setShortcut("Ctrl+S")
    # save_action.triggered.connect(window.save_file)
    # file_menu.addAction(save_action)

    save_as_action = QAction(QIcon(), "Enregistrer sous", window)
    save_as_action.setShortcut("Ctrl+Shift+S")
    save_as_action.triggered.connect(window.export_to_csv)
    log_action("Exportation du fichier depuis le menu fichier")
    file_menu.addAction(save_as_action)
    
    file_menu.addSeparator()
    
    print_action = QAction(QIcon(), "Imprimer toute la librairie", window)
    print_action.setShortcut("Ctrl+P")
    print_action.triggered.connect(window.print_all_files)
    log_action("Impression de la librairie depuis le menu fichier")
    file_menu.addAction(print_action)
    
    print_action = QAction(QIcon(), "Imprimer un livre par ID", window)
    print_action.setShortcut("Ctrl+Shift+P")
    print_action.triggered.connect(window.print_selected_file)
    log_action("Impression d'un livre depuis le menu fichier")
    file_menu.addAction(print_action)
    
    file_menu.addSeparator()
    
    quit_action = QAction(QIcon(), "Quitter", window)
    quit_action.setShortcut("Ctrl+Q")
    quit_action.triggered.connect(window.close)
    log_action("Fermeture de l'application depuis le menu fichier")
    file_menu.addAction(quit_action)
    
    # Menu Option
    option_menu = window.menuBar().addMenu("Option")
    
    fullscreen = QAction(QIcon(), "Pleine écran", window)
    fullscreen.setShortcut("F11")
    fullscreen.triggered.connect(window.toggle_fullscreen)
    log_action("Mise en pleine écran/Mise en fenêtré")
    option_menu.addAction(fullscreen)
    
    option_menu.addSeparator()
    
    vider_cache = QAction(QIcon(), "Vider le cache", window)
    vider_cache.setShortcut("Ctrl+Shift+D")
    vider_cache.triggered.connect(window.supprimer_logs)
    log_action("Suppression logs")
    option_menu.addAction(vider_cache)

    # Menu Édition
    # edit_menu = window.menuBar().addMenu("Édition")
    # undo_action = QAction(QIcon(), "Annuler", window)
    # undo_action.setShortcut("Ctrl+Z")
    # undo_action.triggered.connect(window.text_edit.undo)
    # edit_menu.addAction(undo_action)
    # redo_action = QAction(QIcon(), "Rétablir", window)
    # redo_action.setShortcut("Ctrl+Y")
    # redo_action.triggered.connect(window.text_edit.redo)
    # edit_menu.addAction(redo_action)
    # copy_action = QAction(QIcon(), "Copier", window)
    # copy_action.setShortcut("Ctrl+C")
    # copy_action.triggered.connect(window.text_edit.copy)
    # edit_menu.addAction(copy_action)
    # paste_action = QAction(QIcon(), "Coller", window)
    # paste_action.setShortcut("Ctrl+V")
    # paste_action.triggered.connect(window.text_edit.paste)
    # edit_menu.addAction(paste_action)
