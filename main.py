
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QWidget
from PySide6.QtWidgets import QVBoxLayout
import sys



class ProjectWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Basic variables viewer (Python)")
        

class PythonConsoleWidget(QWidget):
    def __init__(self, code_editor_class, custom_btn_class, output_display_class):
        super().__init__()
        self.code_editor = code_editor_class()
        self.run_button = custom_btn_class("Run")
        self.output_display = output_display_class()
        self.clear_namespace_btn = custom_btn_class("Clear namespace")
        
        self.layout_widgets()
        
        self.namespace = dict()
        
    def layout_widgets(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.code_editor)
        layout.addWidget(self.run_button)
        layout.addWidget(self.clear_namespace_btn)
        layout.addWidget(self.output_display)
        
    def run_code(self):
        code = self.code_editor.toPlainText()
        
        # Guard against errors like zero division error. (Display in output)
        
        has_error_warning = False
        try:
            exec(code, self.namespace)
        except Exception as error:
            has_error_warning = True
            error_object = error
        
        final_table_as_str = ""
        for k, v in self.namespace.items():
            
            # Skip the big wall of text for builtins in the namespace.
            if k == "__builtins__":
                continue
            
            final_table_as_str += f"\n{k}: {v}"
        if has_error_warning:
            final_table_as_str += f"\n{type(error_object).__name__}: {error_object}"
            
        self.output_display.setPlainText(final_table_as_str)
        
    def clear_namespace(self):
        user_variables = {k: v for k, v in self.namespace.items() if k != "__builtins__"}
        if not user_variables:
            self.output_display.setPlainText("[CLEAR]: No user variables to delete.")
        else:
            self.namespace.clear()
            self.output_display.setPlainText("[CLEAR]: Done clearing the namespace.")

class CodeEditor(QTextEdit):
    def __init__(self):
        super().__init__()
        

class CustomButton(QPushButton):
    def __init__(self, text_to_place):
        super().__init__()
        self.setText(text_to_place)
        
class OutputDisplay(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)


if __name__ == "__main__":
    
    # The idea is to have this whole script be the actual controller.
    # So work through everything here.
    
    app = QApplication(sys.argv)
    python_console_widget = PythonConsoleWidget(code_editor_class=CodeEditor, custom_btn_class=CustomButton, output_display_class=OutputDisplay)
    python_console_widget.run_button.clicked.connect(python_console_widget.run_code)
    python_console_widget.clear_namespace_btn.clicked.connect(python_console_widget.clear_namespace)
    
    my_window = ProjectWindow(app=app)
    my_window.setCentralWidget(python_console_widget)
    
    my_window.show()
    
    app.exec()