# main.py
from ui_manager import OpticsShopUI
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = OpticsShopUI()
    main_window.show()
    sys.exit(app.exec_())
