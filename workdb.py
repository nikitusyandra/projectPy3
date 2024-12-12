from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView
from PyQt5.QtSql import QSqlDatabase, QSqlRelationalTableModel, QSqlRelationalDelegate

def create_connection():
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('example.db')  
    if not db.open():
        print("Ошибка подключения к базе данных")
        return False
    return True

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.model = QSqlRelationalTableModel()
        self.model.setTable('Variants')  
        self.model.setEditStrategy(QSqlRelationalTableModel.OnFieldChange)

        self.model.setRelation(2, QSqlRelationalTableModel.Relation('RelatedTable', 'id', 'name'))

        self.model.select()  

        self.table_view = QTableView()
        self.table_view.setModel(self.model)

        self.table_view.setItemDelegate(QSqlRelationalDelegate(self.table_view))

        self.setCentralWidget(self.table_view)


def add_variant():
    record = model.record()
    record.setValue("name", "New Variant")
    model.insertRecord(-1, record)

def delete_variant(index):
    model.removeRow(index.row())



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    if not create_connection():
        sys.exit(1)

    window = MainWindow()
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec())
