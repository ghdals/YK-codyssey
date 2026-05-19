
# 카이사르 암호 해독 프로그램

# 수행 과제
# 1. password.txt 파일을 읽는다.
# 2. 카이사르 암호를 0~25까지 모든 자리수로 해독한다.
# 3. 매 반복마다 결과를 출력하여 눈으로 확인한다.
# 4. 올바른 해독 결과의 번호를 입력받는다.
# 5. 해당 결과를 result.txt 파일로 저장한다.


import os  # 파일 경로를 안정적으로 처리하기 위한 기본 라이브러리



# 카이사르 암호 해독 함수

def caesar_cipher_decode(target_text):
    """
    target_text: 해독할 문자열

    역할:
    - 알파벳 개수(26)만큼 반복하면서
    - 각 자리수(shift)에 대해 해독된 결과를 생성
    - 모든 결과를 리스트로 저장 후 반환
    """

    decoded_list = []  # 모든 해독 결과를 저장할 리스트

    # 0~25까지 반복 (알파벳 개수만큼)
    for shift in range(26):
        decoded_text = ""  # 현재 shift에서 해독된 문자열

        # 문자열을 한 글자씩 처리
        for char in target_text:

            # 소문자 처리
            if 'a' <= char <= 'z':
                # ord() : 문자를 아스키 코드로 변환
                # chr() : 아스키 코드를 문자로 변환
                # (현재 문자 - shift) 만큼 이동
                decoded_text += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))

            # 대문자 처리
            elif 'A' <= char <= 'Z':
                decoded_text += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))

            # 알파벳이 아닌 경우 (공백, 숫자, 특수문자 등)
            else:
                decoded_text += char  # 그대로 유지

        # 결과 리스트에 저장
        decoded_list.append(decoded_text)

        # 매 반복마다 결과 출력 (눈으로 확인 가능하도록)
        print(f"[{shift}] {decoded_text}")

    # 모든 경우의 수 반환
    return decoded_list


base_dir = os.path.dirname(os.path.abspath(__file__))
password_path = os.path.join(base_dir, "password.txt")


# password.txt 파일 읽기
try:
    with open(password_path, "r", encoding="utf-8") as file:
        password_text = file.read()

# 파일이 없는 경우 예외 처리
except FileNotFoundError:
    print("password.txt 파일을 찾을 수 없습니다.")
    print("확인 경로:", password_path)  # 디버깅용 경로 출력

# 그 외 모든 예외 처리
except Exception as e:
    print("파일을 읽는 중 오류가 발생했습니다.")
    print(e)

# 파일 읽기가 정상적으로 끝났을 때 실행
else:
    # 카이사르 암호 해독 실행
    decoded_results = caesar_cipher_decode(password_text)

    # 사용자 입력 받기
    try:
        # 어떤 shift 값이 정답인지 사용자에게 입력 받음
        shift_number = int(input("해독된 자리수 번호를 입력하세요: "))

        # 유효한 범위인지 검사 (0~25)
        if 0 <= shift_number < 26:

            # 선택된 결과 가져오기
            final_password = decoded_results[shift_number]

            
            # result.txt 파일 저장
            result_path = os.path.join(base_dir, "result.txt")

            try:
                with open(result_path, "w", encoding="utf-8") as file:
                    file.write(final_password)

                print("최종 암호가 result.txt 파일로 저장되었습니다.")
                print("저장 위치:", result_path)

            # 파일 저장 중 오류 발생 시
            except Exception as e:
                print("result.txt 파일 저장 중 오류가 발생했습니다.")
                print(e)

        # 범위를 벗어난 경우
        else:
            print("0부터 25 사이의 번호를 입력해야 합니다.")

    # 숫자가 아닌 값을 입력했을 경우
    except ValueError:
        print("숫자를 입력해야 합니다.")
