# main.py
from tools.app import *

def main():
    app = QApplication(sys.argv)
    
    window = LibraryApp()
    window.load_saved_csv()  # Chargement du fichier CSV sauvegardé
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()