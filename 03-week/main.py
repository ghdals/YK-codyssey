# [수행과제 1 + 2]
# Mars_Base_Inventory_List.csv 의 내용을 읽어 들어서 출력하고,
# 내용을 리스트(List) 객체로 변환한다.

inventory_list = []

try:
    file = open('Mars_Base_Inventory_List.csv', 'r', encoding='utf-8')

    header = file.readline().strip()

    print('[원본 데이터]')

    for line in file:
        line = line.strip()
        print(line)  # 요구사항 1 (출력)

        data = line.split(',')
        inventory_list.append(data)  # 요구사항 2 (리스트 변환)

    file.close()

except FileNotFoundError:
    print('csv 파일을 찾을 수 없어요.')


# [수행과제 3]
# 배열 내용을 적재 화물 목록을 인화성이 높은 순으로 정렬한다.

def get_flammability(x):
    # x는 한 행 (리스트)
    # x[4]는 Flammability 값
    return float(x[4])


sorted_list = sorted(
    inventory_list,
    key=get_flammability,
    reverse=True
)

"""
sorted_list = sorted(
    inventory_list,
    key=lambda x: float(x[4]),
    reverse=True
)
"""

print('\n[인화성 높은 순 정렬]')
for item in sorted_list:
    print(item)


# [수행과제 4]
# 인화성 지수가 0.7 이상되는 목록을 뽑아서 별도로 출력한다.

danger_list = []

for item in sorted_list:
    if float(item[4]) >= 0.7:
        danger_list.append(item)

print('\n[인화성 0.7 이상 위험 물질]')
for item in danger_list:
    print(item)


# [수행과제 5]
# 인화성 지수가 0.7 이상되는 목록을 CSV 포맷으로 저장한다.

try:
    file = open('Mars_Base_Inventory_danger.csv', 'w', encoding='utf-8')

    file.write(header + '\n')

    for item in danger_list:
        line = ','.join(item)
        file.write(line + '\n')

    file.close()

    print('\n저장 완료: Mars_Base_Inventory_danger.csv')

except Exception:   # 파일 권한, 경로, 디스크 문제 등
    print('파일 저장 중 오류가 발생했어요.')