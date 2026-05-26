import os
import wave
from datetime import datetime

try:
    import sounddevice as sd
except ModuleNotFoundError:
    print('sounddevice 라이브러리가 설치되어 있지 않습니다.')
    print('터미널에서 다음 명령어를 실행하세요: pip install sounddevice')
    exit()


RECORDS_DIR = 'records'
SAMPLE_RATE = 44100
CHANNELS = 1


def create_records_dir():
    # 녹음 파일을 저장할 records 폴더가 없으면 새로 생성한다.
    if not os.path.exists(RECORDS_DIR):
        os.makedirs(RECORDS_DIR)


def get_record_file_name():
    # 현재 날짜와 시간을 기준으로 파일 이름을 만든다.
    # 예: 20260526-183015.wav
    now = datetime.now()
    file_name = now.strftime('%Y%m%d-%H%M%S') + '.wav'
    return os.path.join(RECORDS_DIR, file_name)


def show_microphones():
    # 시스템에서 인식 가능한 오디오 장치를 출력한다.
    print('\n[인식된 오디오 장치 목록]')
    devices = sd.query_devices()

    for index, device in enumerate(devices):
        if device['max_input_channels'] > 0:
            print(f'{index}: {device["name"]}')


def record_audio():
    # 사용자에게 녹음 시간을 입력받는다.
    try:
        seconds = int(input('녹음할 시간을 초 단위로 입력하세요: '))
    except ValueError:
        print('숫자만 입력해야 합니다.')
        return

    if seconds <= 0:
        print('녹음 시간은 1초 이상이어야 합니다.')
        return

    create_records_dir()
    file_path = get_record_file_name()

    print('녹음을 시작합니다.')
    print(f'{seconds}초 동안 녹음합니다.')

    try:
        # 마이크 입력을 받아 음성 데이터를 녹음한다.
        audio_data = sd.rec(
            int(seconds * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype='int16'
        )
        sd.wait()

        # 녹음된 데이터를 wav 파일로 저장한다.
        with wave.open(file_path, 'wb') as audio_file:
            audio_file.setnchannels(CHANNELS)
            audio_file.setsampwidth(2)
            audio_file.setframerate(SAMPLE_RATE)
            audio_file.writeframes(audio_data.tobytes())

        print('녹음이 완료되었습니다.')
        print(f'저장 위치: {file_path}')

    except Exception as error:
        print('녹음 중 오류가 발생했습니다.')
        print(error)


def list_records_by_date():
    # 특정 날짜 범위 안에 있는 녹음 파일을 보여준다.
    create_records_dir()

    start_date_text = input('시작 날짜를 입력하세요. 예: 20260501: ')
    end_date_text = input('종료 날짜를 입력하세요. 예: 20260526: ')

    try:
        start_date = datetime.strptime(start_date_text, '%Y%m%d')
        end_date = datetime.strptime(end_date_text, '%Y%m%d')
    except ValueError:
        print('날짜 형식이 올바르지 않습니다. 예: 20260526')
        return

    if start_date > end_date:
        print('시작 날짜는 종료 날짜보다 늦을 수 없습니다.')
        return

    print('\n[검색된 녹음 파일 목록]')
    found = False

    for file_name in os.listdir(RECORDS_DIR):
        if not file_name.endswith('.wav'):
            continue

        try:
            record_date_text = file_name.split('-')[0]
            record_date = datetime.strptime(record_date_text, '%Y%m%d')
        except ValueError:
            continue

        if start_date <= record_date <= end_date:
            print(file_name)
            found = True

    if not found:
        print('해당 날짜 범위에 녹음 파일이 없습니다.')


def show_menu():
    print('\n[Javis 음성 기록 프로그램]')
    print('1. 마이크 목록 확인')
    print('2. 음성 녹음하기')
    print('3. 날짜 범위로 녹음 파일 보기')
    print('4. 종료')


def main():
    while True:
        show_menu()
        menu = input('메뉴를 선택하세요: ')

        if menu == '1':
            show_microphones()
        elif menu == '2':
            record_audio()
        elif menu == '3':
            list_records_by_date()
        elif menu == '4':
            print('프로그램을 종료합니다.')
            break
        else:
            print('올바른 메뉴를 선택하세요.')


if __name__ == '__main__':
    main()