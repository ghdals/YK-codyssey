## 설치 확인
print('Hello Mars')

def print_log():
    # 파일 읽기
    try:
        file = open('mission_computer_main.log', 'r')

        for line in file:
            print(line)

        file.close()

    # 예외(파일을 찾을 수 없음.)
    except FileNotFoundError:
        print('로그 파일을 찾을 수 없습니다.')