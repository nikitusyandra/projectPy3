import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableView, QLineEdit, QLabel, QHBoxLayout
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt5.QtCore import Qt


class TeacherApp(QMainWindow):
    def __init__(self):
        super().__init__()

        
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("teachers.db")
        if not self.db.open():
            print("Не удалось открыть базу данных")
            sys.exit(1)

        
        self.init_ui()

        
        self.model = QSqlTableModel(self)
        self.model.setTable("Teacher")
        self.model.select()

        
        self.table_view.setModel(self.model)

    def init_ui(self):
        
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        
        form_layout = QVBoxLayout()

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Имя преподавателя")
        form_layout.addWidget(self.name_input)

        self.subject_input = QLineEdit(self)
        self.subject_input.setPlaceholderText("Предмет")
        form_layout.addWidget(self.subject_input)

        self.age_input = QLineEdit(self)
        self.age_input.setPlaceholderText("Возраст")
        form_layout.addWidget(self.age_input)

        
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Добавить преподавателя", self)
        self.add_button.clicked.connect(self.add_teacher)
        button_layout.addWidget(self.add_button)

        self.update_button = QPushButton("Обновить данные", self)
        self.update_button.clicked.connect(self.update_teacher)
        button_layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Удалить преподавателя", self)
        self.delete_button.clicked.connect(self.delete_teacher)
        button_layout.addWidget(self.delete_button)

        form_layout.addLayout(button_layout)

        
        self.table_view = QTableView(self)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)

        
        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.table_view)

        central_widget.setLayout(layout)

        self.setWindowTitle("Приложение для работы с преподавателями")
        self.setGeometry(100, 100, 800, 600)

    def add_teacher(self):
        """Добавление нового преподавателя в базу данных"""
        name = self.name_input.text()
        subject = self.subject_input.text()
        age = self.age_input.text()

        if name and subject and age.isdigit():  
            query = QSqlQuery()
            query.prepare("INSERT INTO Teacher (name, subject, age) VALUES (?, ?, ?)")
            query.addBindValue(name)
            query.addBindValue(subject)
            query.addBindValue(int(age))
            if query.exec_():
                self.model.select()  
                self.clear_inputs()   
            else:
                print("Ошибка при добавлении преподавателя:", query.lastError().text())
        else:
            print("Заполните все поля корректно.")

    def update_teacher(self):
        """Обновление данных преподавателя"""
        selected_row = self.table_view.selectionModel().selectedRows()
        if selected_row:
            row = selected_row[0].row()
            teacher_id = self.model.data(self.model.index(row, 0))  
            name = self.name_input.text()
            subject = self.subject_input.text()
            age = self.age_input.text()

            if name and subject and age.isdigit():  
                query = QSqlQuery()
                query.prepare("UPDATE Teacher SET name = ?, subject = ?, age = ? WHERE id = ?")
                query.addBindValue(name)
                query.addBindValue(subject)
                query.addBindValue(int(age))
                query.addBindValue(teacher_id)
                if query.exec_():
                    self.model.select()  
                    self.clear_inputs()   
                else:
                    print("Ошибка при обновлении данных преподавателя:", query.lastError().text())
            else:
                print("Заполните все поля корректно.")

    def delete_teacher(self):
        """Удаление преподавателя"""
        selected_row = self.table_view.selectionModel().selectedRows()
        if selected_row:
            row = selected_row[0].row()
            teacher_id = self.model.data(self.model.index(row, 0))  

            query = QSqlQuery()
            query.prepare("DELETE FROM Teacher WHERE id = ?")
            query.addBindValue(teacher_id)
            if query.exec_():
                self.model.select()  
                self.clear_inputs()   
            else:
                print("Ошибка при удалении преподавателя:", query.lastError().text())

    def clear_inputs(self):
        """Очистка полей ввода"""
        self.name_input.clear()
        self.subject_input.clear()
        self.age_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TeacherApp()
    window.show()
    sys.exit(app.exec_())
