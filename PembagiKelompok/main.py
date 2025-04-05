from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
import csv
import os
import random
import math
import time
import sys

COLORS = {
    'primary': '#2563eb',      
    'secondary': '#7c3aed',    
    'success': '#059669',      
    'warning': '#d97706',      
    'error': '#dc2626',        
    'background': '#f8fafc',   
    'surface': '#ffffff',      
    'text': '#1e293b',         
}

class StyledButton(QPushButton):
    def __init__(self, text, color=COLORS['primary'], parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {self.adjust_color(color, -20)};
            }}
            QPushButton:pressed {{
                background-color: {self.adjust_color(color, -40)};
            }}
        """)
        self.setCursor(Qt.PointingHandCursor)
        
    def adjust_color(self, hex_color, factor):
        c = QColor(hex_color)
        h = c.hue()
        s = c.saturation()
        l = max(0, min(255, c.lightness() + factor))
        c.setHsl(h, s, l)
        return c.name()

class StyledListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QListWidget {{
                background-color: {COLORS['surface']};
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 4px;
            }}
            QListWidget::item {{
                background-color: {COLORS['surface']};
                border-radius: 4px;
                padding: 8px;
                margin: 2px 0px;
            }}
            QListWidget::item:selected {{
                background-color: {COLORS['primary']};
                color: white;
            }}
            QListWidget::item:hover {{
                background-color: #f1f5f9;
            }}
        """)

class StyledLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['surface']};
                border: 2px solid #e2e8f0;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border: 2px solid {COLORS['primary']};
            }}
        """)

class ModernGroupDividerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Group Divider")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {COLORS['background']};
            }}
            QLabel {{
                color: {COLORS['text']};
                font-size: 14px;
                font-weight: 500;
            }}
            QMenuBar {{
                background-color: {COLORS['surface']};
                color: {COLORS['text']};
                border-bottom: 1px solid #e2e8f0;
            }}
            QMenuBar::item:selected {{
                background-color: {COLORS['primary']};
                color: white;
            }}
        """)
        
        self.students = []
        self.current_combination_file = None
        
        self.setup_ui()
        
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                background: white;
            }
            QTabBar::tab {
                background: #f8fafc;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-size: 14px;  /* Increased font size for better emoji display */
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 2px solid #2563eb;
            }
        """)

        student_tab = self.create_student_tab()
        groups_tab = self.create_groups_tab()
        view_tab = self.create_view_tab()

        tab_widget.addTab(student_tab, "👥 Students")     
        tab_widget.addTab(groups_tab, "✨ Create Groups")  
        tab_widget.addTab(view_tab, "👀 View Groups")     

        tab_widget.setTabToolTip(0, "Manage your student list")
        tab_widget.setTabToolTip(1, "Create new group combinations")
        tab_widget.setTabToolTip(2, "View generated groups")
        
        main_layout.addWidget(tab_widget)
            
    def create_student_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(16)

        header = QLabel("👥 Student Management")
        header.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 16px;")
        layout.addWidget(header)

        input_layout = QHBoxLayout()
        self.name_entry = StyledLineEdit()
        self.name_entry.setPlaceholderText("Enter student name...")
        add_button = StyledButton("Add Student")
        add_button.clicked.connect(self.add_student)
        
        input_layout.addWidget(self.name_entry)
        input_layout.addWidget(add_button)
        layout.addLayout(input_layout)

        self.student_listbox = StyledListWidget()
        layout.addWidget(self.student_listbox)

        button_layout = QHBoxLayout()
        delete_button = StyledButton("Delete Selected", COLORS['error'])
        save_button = StyledButton("Save to CSV", COLORS['success'])
        load_button = StyledButton("Load from CSV", COLORS['secondary'])
        
        delete_button.clicked.connect(self.delete_selected_student)
        save_button.clicked.connect(self.save_students)
        load_button.clicked.connect(self.load_students)
        
        button_layout.addWidget(delete_button)
        button_layout.addWidget(save_button)
        button_layout.addWidget(load_button)
        layout.addLayout(button_layout)
        
        return tab
        
    def create_groups_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        header = QLabel("✨ Group Creation")
        header.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 24px;")
        layout.addWidget(header)
        
        form_layout = QVBoxLayout()
        form_layout.setSpacing(16)  
        
        groups_section = QVBoxLayout()
        groups_section.setSpacing(8) 
        
        groups_label = QLabel("Enter number of groups:")
        groups_label.setStyleSheet("font-weight: 500;")
        
        group_input = QHBoxLayout()
        self.group_entry = StyledLineEdit()
        self.group_entry.setPlaceholderText("Enter number of groups...")
        confirm_button = StyledButton("Calculate Possibilities")
        confirm_button.clicked.connect(self.calculate_combinations)
        
        group_input.addWidget(self.group_entry)
        group_input.addWidget(confirm_button)
        
        groups_section.addWidget(groups_label)
        groups_section.addLayout(group_input)
        form_layout.addLayout(groups_section)
        
        self.possible_combination_label = QLabel("")
        self.possible_combination_label.setStyleSheet("""
            padding: 16px;
            background: #f1f5f9;
            border-radius: 6px;
            font-weight: bold;
            margin: 8px 0;
        """)
        form_layout.addWidget(self.possible_combination_label)
        
        combinations_section = QVBoxLayout()
        combinations_section.setSpacing(8)  
        
        combinations_label = QLabel("Number of combinations to generate:")
        combinations_label.setStyleSheet("font-weight: 500;")
        
        combination_input = QHBoxLayout()
        self.combination_entry = StyledLineEdit()
        self.combination_entry.setPlaceholderText("Enter number of combinations...")
        generate_button = StyledButton("Generate Groups", COLORS['success'])
        generate_button.clicked.connect(self.generate_combinations)
        
        combination_input.addWidget(self.combination_entry)
        combination_input.addWidget(generate_button)
        
        combinations_section.addWidget(combinations_label)
        combinations_section.addLayout(combination_input)
        form_layout.addLayout(combinations_section)

        layout.addLayout(form_layout)

        layout.addStretch(1)
        
        return tab
        
    def create_view_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(16)

        header = QLabel("👀 View Groups")
        header.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 16px;")
        layout.addWidget(header)

        self.combination_listbox = StyledListWidget()
        layout.addWidget(self.combination_listbox)

        button_layout = QHBoxLayout()
        view_button = StyledButton("View Selected Groups", COLORS['primary'])
        load_button = StyledButton("Load Combinations", COLORS['secondary'])
        
        view_button.clicked.connect(self.view_groups)
        load_button.clicked.connect(self.load_combinations_file)
        
        button_layout.addWidget(view_button)
        button_layout.addWidget(load_button)
        layout.addLayout(button_layout)

        self.group_table = QTextEdit()
        self.group_table.setReadOnly(True)
        self.group_table.setStyleSheet(f"""
            QTextEdit {{
                background-color: {COLORS['surface']};
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 16px;
                font-size: 14px;
                line-height: 1.5;
            }}
        """)
        layout.addWidget(self.group_table)
        
        return tab
    
    def show_message(self, title, text, icon=QMessageBox.Information):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(icon)
        msg.setStyleSheet(f"""
            QMessageBox {{
                background-color: {COLORS['surface']};
            }}
            QPushButton {{
                background-color: {COLORS['primary']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.adjust_color(COLORS['primary'], -20)};
            }}
        """)
        return msg.exec_()

    def add_student(self):
        student_name = self.name_entry.text().strip()
        if student_name:
            self.students.append(student_name)
            self.update_student_listbox()
            self.name_entry.clear()
        else:
            self.show_message("Input Error", "Please enter a student's name.", QMessageBox.Warning)
            
    def update_student_listbox(self):
        self.student_listbox.clear()
        for index, student in enumerate(self.students, start=1):
            self.student_listbox.addItem(f"{index}. {student}")
            
    def delete_selected_student(self):
        selected_items = self.student_listbox.selectedItems()
        if not selected_items:
            self.show_message("Selection Error", "Please select a student to delete.", QMessageBox.Warning)
            return
            
        selected_index = self.student_listbox.row(selected_items[0])
        student_name = self.students[selected_index]
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Confirm Deletion")
        msg.setText(f"Are you sure you want to delete {student_name}?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        
        if msg.exec_() == QMessageBox.Yes:
            del self.students[selected_index]
            self.update_student_listbox()
            self.show_message("Success", "Student deleted successfully.")
            
    def save_students(self):
        if not self.students:
            self.show_message(
                "Save Error",
                "No students to save. Please add students first.",
                QMessageBox.Warning
            )
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Students List",
            "",
            "CSV Files (*.csv);;All Files (*.*)"
        )
        
        if file_path:
            try:
                with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows([[student] for student in self.students])
                
                self.show_message(
                    "Success",
                    f"Student list saved successfully to:\n{file_path}",
                    QMessageBox.Information
                )
            except Exception as e:
                self.show_message(
                    "Save Error",
                    f"Failed to save file:\n{str(e)}",
                    QMessageBox.Critical
                )
            
    def load_students(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Students List",
            "",
            "CSV Files (*.csv);;All Files (*.*)"
        )
        
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, mode='r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    self.students = [row[0] for row in reader if row]  # Skip empty rows
                
                self.update_student_listbox()
                self.show_message(
                    "Success",
                    f"Successfully loaded {len(self.students)} students",
                    QMessageBox.Information
                )
            except Exception as e:
                self.show_message(
                    "Load Error",
                    f"Failed to load file:\n{str(e)}",
                    QMessageBox.Critical
                )
        else:
            self.show_message(
                "Load Error",
                "No file selected or file does not exist.",
                QMessageBox.Warning
            )
            
    def calculate_combinations(self):
        try:
            num_students = len(self.students)
            if num_students == 0:
                self.show_message(
                    "Input Error",
                    "Please add students before calculating combinations.",
                    QMessageBox.Warning
                )
                return
                
            num_groups = int(self.group_entry.text())
            
            if num_groups <= 0:
                self.show_message(
                    "Input Error",
                    "Number of groups must be positive.",
                    QMessageBox.Warning
                )
                return
                
            if num_groups > num_students:
                self.show_message(
                    "Input Error",
                    "Number of groups cannot be larger than number of students.",
                    QMessageBox.Warning
                )
                return
                
            num_combinations = math.comb(num_students, num_groups)
            
            self.possible_combination_label.setText(
                f"""
                <div style='text-align: center;'>
                    <p style='font-size: 16px; margin: 4px;'>Possible Combinations</p>
                    <p style='font-size: 24px; color: {COLORS['primary']}; margin: 4px;'>
                        {num_combinations:,}
                    </p>
                    <p style='font-size: 12px; color: #64748b; margin: 4px;'>
                        Based on {num_students} students in {num_groups} groups
                    </p>
                </div>
                """
            )
            
        except ValueError:
            self.show_message(
                "Input Error",
                "Please enter a valid number of groups.",
                QMessageBox.Warning
            )
            
    def generate_combinations(self):
        try:
            num_combinations = int(self.combination_entry.text())
            if num_combinations <= 0:
                self.show_message(
                    "Input Error",
                    "Number of combinations must be positive.",
                    QMessageBox.Warning
                )
                return
                
            num_students = len(self.students)
            if num_students == 0:
                self.show_message(
                    "Input Error",
                    "Please add students before generating combinations.",
                    QMessageBox.Warning
                )
                return
                
            num_groups = int(self.group_entry.text())
            if num_groups <= 0 or num_groups > num_students:
                self.show_message(
                    "Input Error",
                    "Invalid number of groups.",
                    QMessageBox.Warning
                )
                return

            progress = QProgressDialog("Generating combinations...", None, 0, num_combinations, self)
            progress.setWindowModality(Qt.WindowModal)
            progress.setStyleSheet(f"""
                QProgressDialog {{
                    background-color: {COLORS['surface']};
                    min-width: 300px;
                }}
                QProgressBar {{
                    border: 1px solid #e2e8f0;
                    border-radius: 4px;
                    text-align: center;
                }}
                QProgressBar::chunk {{
                    background-color: {COLORS['primary']};
                    border-radius: 3px;
                }}
            """)
            
            groups_list = []
            for i in range(num_combinations):
                shuffled_students = self.students.copy()
                random.shuffle(shuffled_students)
                groups = [shuffled_students[i::num_groups] for i in range(num_groups)]
                groups_list.append(groups)
                progress.setValue(i + 1)

            timestamp = time.strftime("%Y%m%d_%H%M%S")
            file_path = f"combinations_{timestamp}.csv"
            
            try:
                with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows([[str(groups)] for groups in groups_list])
                    
                self.current_combination_file = file_path
                self.show_combinations_from_file(file_path)
                
                self.show_message(
                    "Success",
                    f"Generated {num_combinations} combinations successfully!\n\nSaved to: {file_path}",
                    QMessageBox.Information
                )
                
            except Exception as e:
                self.show_message(
                    "Save Error",
                    f"Failed to save combinations:\n{str(e)}",
                    QMessageBox.Critical
                )
                
        except ValueError:
            self.show_message(
                "Input Error",
                "Please enter valid numbers for groups and combinations.",
                QMessageBox.Warning
            )
            
    def load_combinations_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Combinations File",
            "",
            "CSV Files (*.csv);;All Files (*.*)"
        )
        
        if not file_path:
            return
            
        try:
            self.show_combinations_from_file(file_path)
            self.current_combination_file = file_path
            
            self.show_message(
                "Success",
                f"Combinations loaded successfully from:\n{file_path}",
                QMessageBox.Information
            )
            
        except Exception as e:
            self.show_message(
                "Load Error",
                f"Failed to load combinations file:\n{str(e)}",
                QMessageBox.Critical
            )
            
    def show_combinations_from_file(self, file_path):
        self.combination_listbox.clear()
        
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for i, row in enumerate(reader, 1):
                    if row:  
                        item_text = f"Combination {i}"
                        self.combination_listbox.addItem(item_text)
                        
        except FileNotFoundError:
            self.show_message(
                "File Error",
                f"File not found:\n{file_path}",
                QMessageBox.Critical
            )
        except Exception as e:
            self.show_message(
                "Load Error",
                f"Failed to read combinations:\n{str(e)}",
                QMessageBox.Critical
            )
            
    def view_groups(self):
        selected_items = self.combination_listbox.selectedItems()
        if not selected_items:
            self.show_message(
                "Selection Error",
                "Please select a combination to view.",
                QMessageBox.Warning
            )
            return
            
        if not self.current_combination_file:
            self.show_message(
                "File Error",
                "No combinations file loaded. Please load a file first.",
                QMessageBox.Warning
            )
            return
            
        combination_index = self.combination_listbox.row(selected_items[0])
        
        try:
            with open(self.current_combination_file, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                groups = None
                for i, row in enumerate(reader):
                    if i == combination_index:
                        groups = eval(row[0])
                        break
                        
            if groups:
                self.group_table.clear()
                self.group_table.setHtml("""
                    <style>
                        .group-header {
                            color: """ + COLORS['primary'] + """;
                            font-size: 16px;
                            font-weight: bold;
                            margin: 12px 0 8px 0;
                        }
                        .student-item {
                            margin: 4px 0;
                            padding: 4px 0 4px 20px;
                            color: """ + COLORS['text'] + """;
                        }
                    </style>
                """)

                for group_num, group in enumerate(groups, 1):
                    self.group_table.append(f'<div class="group-header">Group {group_num}</div>')
                    for student in group:
                        self.group_table.append(
                            f'<div class="student-item">• {student}</div>'
                        )
                    self.group_table.append("")
                    
        except FileNotFoundError:
            self.show_message(
                "File Error",
                "Combinations file not found. Please load a file.",
                QMessageBox.Critical
            )
        except Exception as e:
            self.show_message(
                "Error",
                f"An error occurred while viewing groups:\n{str(e)}",
                QMessageBox.Critical
            )
            
    def adjust_color(self, hex_color, factor):
        """Utility method to adjust color brightness"""
        c = QColor(hex_color)
        h = c.hue()
        s = c.saturation()
        l = max(0, min(255, c.lightness() + factor))
        c.setHsl(h, s, l)
        return c.name()
    
def main():
    app = QApplication(sys.argv)

    app.setStyle("Fusion")

    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = ModernGroupDividerApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()