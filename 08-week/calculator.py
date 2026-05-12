import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


# =========================
# 계산기의 핵심 로직 클래스
# =========================
class Calculator:
    def __init__(self):
        # 생성 시 초기 상태 설정
        self.reset()

    # 전체 초기화 (AC 버튼)
    def reset(self):
        self.current = "0"           # 현재 입력 값 (문자열)
        self.previous = None         # 이전 값
        self.operator = None         # 연산자 (+, -, *, /)
        self.waiting_new_number = False  # 다음 숫자 입력 대기 상태
        return self.current

    # 숫자 입력 처리
    def input_number(self, number):
        # 연산 직후라면 새 숫자 시작
        if self.waiting_new_number:
            self.current = number
            self.waiting_new_number = False

        # 기본값이 0이면 교체
        elif self.current == "0":
            self.current = number

        # 그 외에는 숫자 이어붙이기
        else:
            self.current += number

        return self.current

    # 소수점 입력 처리
    def input_decimal(self):
        # 연산 직후라면 0.부터 시작
        if self.waiting_new_number:
            self.current = "0."
            self.waiting_new_number = False

        # 이미 소수점이 없을 때만 추가
        elif "." not in self.current:
            self.current += "."

        return self.current

    # +/- 부호 변경
    def negative_positive(self):
        if self.current != "0":
            # 음수 → 양수
            if self.current.startswith("-"):
                self.current = self.current[1:]
            # 양수 → 음수
            else:
                self.current = "-" + self.current

        return self.current

    # 퍼센트 계산 (현재값 / 100)
    def percent(self):
        try:
            value = float(self.current) / 100
            self.current = self.format_result(value)
            return self.current
        except Exception:
            return "Error"

    # 각 연산자 설정
    def add(self):
        return self.set_operator("+")

    def subtract(self):
        return self.set_operator("-")

    def multiply(self):
        return self.set_operator("*")

    def divide(self):
        return self.set_operator("/")

    # 연산자 공통 처리
    def set_operator(self, operator):
        # 이미 연산자가 있는 상태라면 먼저 계산 수행
        if self.operator is not None and not self.waiting_new_number:
            self.equal()

        self.previous = float(self.current)  # 현재값을 이전값으로 저장
        self.operator = operator            # 연산자 저장
        self.waiting_new_number = True      # 다음 숫자 입력 대기

        return self.current

    # = 버튼 (결과 계산)
    def equal(self):
        # 계산할 값이 없으면 그대로 반환
        if self.operator is None or self.previous is None:
            return self.current

        try:
            current_value = float(self.current)

            # 사칙연산 수행
            if self.operator == "+":
                result = self.previous + current_value

            elif self.operator == "-":
                result = self.previous - current_value

            elif self.operator == "*":
                result = self.previous * current_value

            elif self.operator == "/":
                # 0으로 나누기 예외 처리
                if current_value == 0:
                    self.reset()
                    return "Error"
                result = self.previous / current_value

            # 숫자 범위 초과 처리
            if abs(result) > 1e100:
                self.reset()
                return "Overflow"

            # 결과 포맷팅
            self.current = self.format_result(result)

            # 상태 초기화
            self.previous = None
            self.operator = None
            self.waiting_new_number = True

            return self.current

        except Exception:
            self.reset()
            return "Error"

    # 결과 포맷 (소수점 6자리 + 불필요한 0 제거)
    def format_result(self, value):
        # 정수라면 소수점 제거
        if value == int(value):
            return str(int(value))

        # 소수점 6자리 반올림 후 불필요한 0 제거
        return str(round(value, 6)).rstrip("0").rstrip(".")


# =========================
# UI 클래스 (PyQt)
# =========================
class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.calculator = Calculator()  # 계산 로직 연결
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Calculator")
        self.setFixedSize(320, 460)

        # 결과 출력창
        self.display = QLineEdit("0")
        self.display.setAlignment(Qt.AlignRight)  # 오른쪽 정렬
        self.display.setReadOnly(True)            # 입력 불가
        self.display.setFont(QFont("Arial", 32))

        layout = QGridLayout()
        layout.addWidget(self.display, 0, 0, 1, 4)

        # 버튼 구성 (텍스트, 행, 열, 행병합, 열병합)
        buttons = [
            ("AC", 1, 0), ("+/-", 1, 1), ("%", 1, 2), ("/", 1, 3),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("*", 2, 3),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("-", 3, 3),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("+", 4, 3),
            ("0", 5, 0), (".", 5, 1), ("=", 5, 2, 1, 2)
        ]

        # 버튼 생성 및 이벤트 연결
        for button_info in buttons:
            text = button_info[0]
            row = button_info[1]
            col = button_info[2]
            row_span = button_info[3] if len(button_info) > 3 else 1
            col_span = button_info[4] if len(button_info) > 4 else 1

            button = QPushButton(text)
            button.setFont(QFont("Arial", 18))

            # 클릭 시 handle_button 함수 호출
            button.clicked.connect(lambda checked, value=text: self.handle_button(value))

            layout.addWidget(button, row, col, row_span, col_span)

        self.setLayout(layout)

    # 버튼 클릭 처리
    def handle_button(self, value):
        if value.isdigit():
            result = self.calculator.input_number(value)

        elif value == ".":
            result = self.calculator.input_decimal()

        elif value == "AC":
            result = self.calculator.reset()

        elif value == "+/-":
            result = self.calculator.negative_positive()

        elif value == "%":
            result = self.calculator.percent()

        elif value == "+":
            result = self.calculator.add()

        elif value == "-":
            result = self.calculator.subtract()

        elif value == "*":
            result = self.calculator.multiply()

        elif value == "/":
            result = self.calculator.divide()

        elif value == "=":
            result = self.calculator.equal()

        else:
            result = self.calculator.current

        self.update_display(result)

    # 화면 업데이트 + 폰트 자동 조절
    def update_display(self, text):
        self.display.setText(text)

        length = len(text)

        # 글자 길이에 따라 폰트 크기 조절
        if length <= 8:
            font_size = 32
        elif length <= 12:
            font_size = 26
        elif length <= 16:
            font_size = 20
        else:
            font_size = 16

        self.display.setFont(QFont("Arial", font_size))


# =========================
# 프로그램 실행
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalculatorUI()
    window.show()
    sys.exit(app.exec_())