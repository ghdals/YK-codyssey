import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QPushButton,
    QLabel,
)


# [핵심 설명]
# QWidget : 하나의 "창"을 의미 (계산기 전체 화면)
class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.current_text = "0"  # 현재 화면에 표시될 값
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("iPhone Style Calculator")
        self.setFixedSize(360, 640)
        self.setStyleSheet("background-color: black;")

        # [핵심 설명]
        # QVBoxLayout : 위 → 아래로 쌓는 레이아웃
        main_layout = QVBoxLayout()

        # =========================
        # [수행과제 2]
        # 아이폰 계산기와 유사한 "출력 화면(UI)" 생성
        # =========================
        self.display = QLabel("0")  # 숫자를 표시하는 영역
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display.setStyleSheet(
            """
            QLabel {
                color: white;
                font-size: 48px;
                padding: 20px;
                background-color: black;
            }
            """
        )
        self.display.setFixedHeight(150)
        main_layout.addWidget(self.display)

        # =========================
        # [수행과제 2]
        # 버튼들을 아이폰 계산기처럼 배치 (Grid 구조)
        # =========================
        # [핵심 설명]
        # QGridLayout : 표처럼 (행, 열)로 버튼 배치
        grid = QGridLayout()

        # 버튼 배열 (아이폰 계산기 구조)
        buttons = [
            ["AC", "+/-", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
        ]

        # =========================
        # [수행과제 3]
        # 버튼 생성 + 클릭 이벤트 연결
        # =========================
        for row, button_row in enumerate(buttons):
            for col, text in enumerate(button_row):
                button = QPushButton(text)

                # 버튼 스타일
                button.setFixedSize(70, 70)
                button.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #333;
                        color: white;
                        font-size: 24px;
                        border-radius: 35px;
                    }
                    """
                )

                # [핵심 설명]
                # clicked.connect() :
                # 버튼을 눌렀을 때 실행할 함수 연결
                button.clicked.connect(
                    lambda _, value=text: self.button_clicked(value)
                )

                grid.addWidget(button, row, col)

        # =========================
        # [수행과제 2]
        # 마지막 줄 (0 버튼은 2칸 차지)
        # =========================
        zero_button = QPushButton("0")
        zero_button.setFixedSize(150, 70)
        zero_button.setStyleSheet(
            """
            QPushButton {
                background-color: #333;
                color: white;
                font-size: 24px;
                border-radius: 35px;
                text-align: left;
                padding-left: 20px;
            }
            """
        )
        zero_button.clicked.connect(lambda: self.button_clicked("0"))

        dot_button = QPushButton(".")
        dot_button.setFixedSize(70, 70)
        dot_button.setStyleSheet(
            """
            QPushButton {
                background-color: #333;
                color: white;
                font-size: 24px;
                border-radius: 35px;
            }
            """
        )
        dot_button.clicked.connect(lambda: self.button_clicked("."))

        equal_button = QPushButton("=")
        equal_button.setFixedSize(70, 70)
        equal_button.setStyleSheet(
            """
            QPushButton {
                background-color: orange;
                color: white;
                font-size: 24px;
                border-radius: 35px;
            }
            """
        )
        equal_button.clicked.connect(lambda: self.button_clicked("="))

        grid.addWidget(zero_button, 4, 0, 1, 2)
        grid.addWidget(dot_button, 4, 2)
        grid.addWidget(equal_button, 4, 3)

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    # =========================
    # [수행과제 3]
    # 버튼 클릭 시 숫자가 입력되도록 처리
    # =========================
    def button_clicked(self, value):
        # [핵심 설명]
        # value : 눌린 버튼의 값 (예: "1", "+", "AC")

        # AC → 초기화
        if value == "AC":
            self.current_text = "0"

        # 숫자 입력
        elif value.isdigit():
            if self.current_text == "0":
                self.current_text = value
            else:
                self.current_text += value

        # 소수점 입력
        elif value == ".":
            if "." not in self.current_text:
                self.current_text += "."

        # 연산자 입력 (계산은 하지 않고 표시만)
        elif value in ["+", "-", "×", "÷", "%"]:
            self.current_text += " " + value + " "

        # +/- 처리 (간단하게 앞에 - 붙이기)
        elif value == "+/-":
            if self.current_text.startswith("-"):
                self.current_text = self.current_text[1:]
            else:
                self.current_text = "-" + self.current_text

        # =========================
        # [수행과제 4]
        # "=" 버튼은 계산 기능 구현하지 않음
        # =========================
        elif value == "=":
            pass  # 아무 동작 없음

        # 화면 업데이트
        self.display.setText(self.current_text)


# =========================
# [수행과제 1]
# PyQt 실행을 위한 기본 코드
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())