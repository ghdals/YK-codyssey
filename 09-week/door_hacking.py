"""emergency_storage_key.zip 파일의 비밀번호를 무차별 대입으로 찾는 스크립트.

비밀번호는 소문자 알파벳 + 숫자, 길이 6자리로 가정한다 (36^6 = 약 21.7억 조합).
멀티프로세싱으로 CPU 코어를 모두 활용하여 탐색 시간을 단축한다.
"""

import itertools          # 비밀번호 조합 생성을 위한 데카르트 곱(product)
import multiprocessing    # 멀티프로세싱 (Process, Event, Queue, Value)
import os                 # 파일 경로 처리, CPU 코어 수 조회
import time               # 시작 시간, 진행 시간 측정
import zipfile            # zip 파일 열기 / 추출 / 비밀번호 검증
import zlib               # zip 압축 해제 중 발생하는 예외(zlib.error) 처리용


# 비밀번호에 사용 가능한 문자 집합: 소문자 a-z + 숫자 0-9 = 36자
CHARACTERS = 'abcdefghijklmnopqrstuvwxyz0123456789'

# 비밀번호 길이 (과제 조건: 6자리)
PASSWORD_LENGTH = 6

# 진행률을 화면에 출력하는 간격 (워커별 시도 횟수가 이 값의 배수일 때 출력)
PROGRESS_UNIT = 100000


def try_passwords(
    worker_id, prefixes, zip_file_name, found_event, result_queue, counter
):
    """워커 프로세스: 할당받은 첫 글자(prefix)로 시작하는 비밀번호를 모두 시도.

    매개변수:
        worker_id      : 워커 식별 번호 (출력용)
        prefixes       : 이 워커가 담당할 첫 글자 묶음 (예: 'abc')
        zip_file_name  : 해독할 zip 파일 경로
        found_event    : 한 워커가 정답을 찾으면 set()되어 모든 워커에게 종료 신호 전달
        result_queue   : 정답 비밀번호를 메인 프로세스로 전달하기 위한 큐
        counter        : 모든 워커가 공유하는 누적 시도 횟수 카운터
    """
    # 각 워커는 자기 자신의 zip_file 핸들을 별도로 연다.
    # (프로세스 간 파일 핸들은 공유하지 않는 것이 안전)
    try:
        zip_file = zipfile.ZipFile(zip_file_name)
    except (FileNotFoundError, zipfile.BadZipFile, OSError):
        # 파일이 없거나 손상되어 있으면 이 워커는 아무것도 못 함
        return

    # 비밀번호 검증용 대상 파일: zip 안의 첫 번째 항목을 사용한다.
    # extractall 대신 read를 쓰면 디스크에 쓰지 않고 메모리에서만 검증되어 빠르다.
    target_name = zip_file.namelist()[0]

    # 이 워커가 지금까지 시도한 횟수 (로컬 카운터)
    local_count = 0
    start_time = time.time()

    try:
        # 바깥 루프: 이 워커가 담당하는 첫 글자들 (예: 'a' -> 'b' -> 'c')
        for prefix in prefixes:
            # 안쪽 루프: 첫 글자 뒤에 붙을 5자리 모든 조합 (36^5 = 6,047만 가지)
            for suffix_tuple in itertools.product(
                CHARACTERS, repeat=PASSWORD_LENGTH - 1
            ):
                # 다른 워커가 이미 정답을 찾았다면 즉시 종료한다.
                # found_event는 multiprocessing.Event 객체로,
                # 한 워커가 set()하면 모든 워커가 is_set()으로 감지할 수 있다.
                if found_event.is_set():
                    return

                # 6자리 비밀번호 후보 문자열 생성
                password = prefix + ''.join(suffix_tuple)
                local_count += 1

                try:
                    # 비밀번호로 zip 내부 파일을 읽어 본다.
                    # 비밀번호가 틀리면 RuntimeError 등의 예외가 발생한다.
                    zip_file.read(target_name, pwd=password.encode('utf-8'))
                except (RuntimeError, zlib.error, zipfile.BadZipFile, OSError):
                    # 비밀번호 불일치: 다음 후보로 넘어간다.

                    # 일정 시도 횟수마다 진행 상황을 출력
                    if local_count % PROGRESS_UNIT == 0:
                        # 공유 카운터(counter)는 여러 프로세스가 동시에 수정할 수 있으므로
                        # get_lock()으로 락을 잡고 안전하게 증가시킨다.
                        # (락이 없으면 동시 쓰기로 값이 손상될 수 있음 = race condition)
                        with counter.get_lock():
                            counter.value += PROGRESS_UNIT
                            total = counter.value
                        elapsed = round(time.time() - start_time, 2)
                        print(
                            '워커', worker_id,
                            '- 반복 횟수(워커):', local_count,
                            '/ 전체 반복 횟수:', total,
                            '/ 진행 시간:', elapsed, '초'
                        )
                    continue

                # 여기까지 도달했다 = 예외 없이 read() 성공 = 비밀번호 정답!

                # 아직 카운터에 반영되지 않은 잔여분(마지막 PROGRESS_UNIT 미만)을 누적
                with counter.get_lock():
                    counter.value += local_count % PROGRESS_UNIT

                # 다른 워커들에게 "찾았다" 신호를 보낸다.
                found_event.set()

                # 메인 프로세스가 결과를 받아갈 수 있도록 큐에 넣는다.
                # (Queue는 프로세스 간 데이터 전달용. 직렬화되어 전달됨)
                result_queue.put(password)
                return

        # 이 워커가 담당 구간을 모두 다 돌았지만 못 찾은 경우
        # 마지막 잔여 카운트도 누적해 줘야 총 합계가 정확하다.
        with counter.get_lock():
            counter.value += local_count % PROGRESS_UNIT
    finally:
        # 정상/비정상 종료 모두에서 zip 파일 핸들을 반드시 닫는다.
        zip_file.close()


def unlock_zip():
    """zip 파일 비밀번호를 찾아 password.txt에 저장하는 메인 함수."""

    # 스크립트가 위치한 폴더 기준으로 경로를 만든다.
    # → 어느 디렉토리에서 실행해도 같은 경로를 사용할 수 있음.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    zip_file_name = os.path.join(base_dir, 'emergency_storage_key.zip')
    output_folder = os.path.join(base_dir, 'emergency_storage_key')
    password_file_name = os.path.join(base_dir, 'password.txt')

    start_time = time.time()
    print('암호 해독을 시작합니다.')
    print('시작 시간:', time.ctime(start_time))

    # zip 파일이 정상적으로 열리는지 사전 검사.
    # 본격적인 워커 생성 전에 빠르게 실패하기 위함.
    try:
        with zipfile.ZipFile(zip_file_name):
            pass
    except FileNotFoundError:
        print('zip 파일을 찾을 수 없습니다.')
        return
    except zipfile.BadZipFile:
        print('올바른 zip 파일이 아닙니다.')
        return

    # CPU 논리 프로세서 수만큼 워커를 만든다.
    # os.cpu_count()가 None을 반환할 수 있어 안전 장치(or 1)를 추가.
    worker_count = max(1, os.cpu_count() or 1)
    print('워커 프로세스 수:', worker_count)

    # 36개 첫 글자를 워커 수만큼 균등하게 나누어 각 워커에게 분배한다.
    # 예) 글자 36개, 워커 14개 → 한 워커당 3글자씩, 총 12개의 청크 생성
    #     (36이 14로 정확히 나누어떨어지지 않으면 일부 워커는 만들어지지 않음)
    # (N + M - 1) // M 은 ceil(N / M) 과 동일한 정수 올림 나눗셈 트릭.
    chunk_size = (len(CHARACTERS) + worker_count - 1) // worker_count
    chunks = [
        CHARACTERS[i:i + chunk_size]
        for i in range(0, len(CHARACTERS), chunk_size)
    ]

    # 프로세스 간 통신(IPC)에 사용할 객체들
    # - Event:  찾았는지 여부를 한 번에 모든 워커에게 알리는 신호 (set/is_set)
    # - Queue:  결과(비밀번호 문자열)를 메인 프로세스로 전달
    # - Value:  모든 워커가 공유하는 누적 시도 횟수 카운터
    #           ('Q' = unsigned long long, 8바이트 정수 타입 코드)
    found_event = multiprocessing.Event()
    result_queue = multiprocessing.Queue()
    counter = multiprocessing.Value('Q', 0)

    # 각 청크를 담당할 워커 프로세스를 만들어 시작시킨다.
    workers = []
    for worker_id, chunk in enumerate(chunks):
        process = multiprocessing.Process(
            target=try_passwords,
            args=(
                worker_id,
                chunk,
                zip_file_name,
                found_event,
                result_queue,
                counter,
            ),
        )
        process.start()
        workers.append(process)

    # 모든 워커가 종료될 때까지 메인 프로세스는 여기서 대기한다.
    # (정답을 찾은 워커가 found_event.set()을 호출하면, 나머지 워커들도
    #  다음 루프 시작 시 is_set()을 보고 자발적으로 종료된다.)
    for process in workers:
        process.join()

    end_time = time.time()
    progress_time = round(end_time - start_time, 2)
    total_count = counter.value  # 모든 워커의 시도 횟수 합산

    # 결과 큐가 비어 있다 = 어떤 워커도 비밀번호를 큐에 넣지 못했다 = 실패
    if result_queue.empty():
        print('암호를 찾지 못했습니다.')
        print('총 반복 횟수:', total_count)
        print('총 진행 시간:', progress_time, '초')
        return

    # 성공: 큐에서 비밀번호를 꺼낸다.
    password = result_queue.get()
    print('암호 해독 성공!')
    print('암호:', password)
    print('총 반복 횟수:', total_count)
    print('총 진행 시간:', progress_time, '초')

    # 찾은 비밀번호로 zip 내부 파일들을 모두 추출한다.
    try:
        with zipfile.ZipFile(zip_file_name) as zip_file:
            zip_file.extractall(
                path=output_folder,
                pwd=password.encode('utf-8'),
            )
    except (RuntimeError, zlib.error, zipfile.BadZipFile, OSError) as error:
        print('파일 추출 중 오류가 발생했습니다:', error)

    # 과제 조건: 찾은 비밀번호를 password.txt 파일에 저장한다.
    try:
        with open(password_file_name, 'w', encoding='utf-8') as file:
            file.write(password)
    except OSError:
        print('password.txt 파일 저장 중 오류가 발생했습니다.')


# Windows에서 multiprocessing을 사용할 때 필수: 워커 프로세스가 모듈을 재import할 때
# unlock_zip()이 무한 재귀로 호출되는 것을 막아 준다.
if __name__ == '__main__':
    unlock_zip()
