import boto3
from PyQt5 import QtWidgets, QtGui


class AWSValidation(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.client = boto3.client('iam')
        self.init_ui()

    def init_ui(self):
        self.file_label = QtWidgets.QLabel("File:", self)
        self.file_input = QtWidgets.QLineEdit(self)
        self.browse_button = QtWidgets.QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.select_file)
        self.check_button = QtWidgets.QPushButton("Check", self)
        self.check_button.clicked.connect(self.check_credentials)

        layout = QtWidgets.QFormLayout(self)
        layout.addRow(self.file_label, self.file_input)
        layout.addRow(self.browse_button)
        layout.addRow(self.check_button)

    def select_file(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Credentials File", "",
                                                             "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            self.file_input.setText(file_name)

    def check_credentials(self):
        file_path = self.file_input.text()

        try:
            with open(file_path, 'r') as f:
                for line in f:
                    email, password = line.strip().split(':')
                    self.client = boto3.client('iam', aws_access_key_id=email,
                                               aws_secret_access_key=password)
                    self.client.get_user()
                    print(f"Credentials for {email} are valid.")
        except Exception as e:
            print(f"Invalid AWS credentials: {e}")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    validation = AWSValidation()
    validation.setWindowTitle("IAM Credentials Validation")
    validation.show()
    app.exec_()
