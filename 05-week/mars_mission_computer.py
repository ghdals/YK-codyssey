import json
import random
import time


# 역할 : 값 생성(값을 랜덤으로 만들어주는)
class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = round(
            random.uniform(18, 30), 2
        )
        self.env_values['mars_base_external_temperature'] = round(
            random.uniform(0, 21), 2
        )
        self.env_values['mars_base_internal_humidity'] = round(
            random.uniform(50, 60), 2
        )
        self.env_values['mars_base_external_illuminance'] = round(
            random.uniform(500, 715), 2
        )
        self.env_values['mars_base_internal_co2'] = round(
            random.uniform(0.02, 0.1), 4
        )
        self.env_values['mars_base_internal_oxygen'] = round(
            random.uniform(4, 7), 2
        )

    def get_env(self):
        return self.env_values


# 1. 미션 컴퓨터에 해당하는 클래스를 생성한다. 클래스의 이름은 MissionComputer로 정의한다.
# 역할 : 값 관리 및 출력(센서값을 받아오고 저장하고 출력하는)
class MissionComputer:
    def __init__(self):
        # 2. 미션 컴퓨터에는 화성 기지의 환경에 대한 값을 저장할 수 있는 사전(Dict) 객체가 env_values라는 속성으로 포함되어야 한다.
        # 3. env_values라는 속성 안에는 다음과 같은 내용들이 구현 되어야 한다.
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }
        # 4. 문제 3에서 제작한 DummySensor 클래스를 ds라는 이름으로 인스턴스화 시킨다.
        self.ds = DummySensor()

        # 보너스 2. 
        # 5분 평균 계산을 위해 값을 저장할 딕셔너리
        self.avg_values = {
            'mars_base_internal_temperature': [],
            'mars_base_external_temperature': [],
            'mars_base_internal_humidity': [],
            'mars_base_external_illuminance': [],
            'mars_base_internal_co2': [],
            'mars_base_internal_oxygen': []
        }

    # 5. MissionComputer에 get_sensor_data() 메소드를 추가한다.
    # 6. get_sensor_data() 메소드에 다음과 같은 세 가지 기능을 추가한다.
    def get_sensor_data(self):
        # while True : 5초마다 반복하기 위함
        while True:
            count = 0
            # 6-1. 센서의 값을 가져와서 env_values에 담는다.
            self.ds.set_env()
            sensor_data = self.ds.get_env()

            self.env_values['mars_base_internal_temperature'] = (
                sensor_data['mars_base_internal_temperature']
            )
            self.env_values['mars_base_external_temperature'] = (
                sensor_data['mars_base_external_temperature']
            )
            self.env_values['mars_base_internal_humidity'] = (
                sensor_data['mars_base_internal_humidity']
            )
            self.env_values['mars_base_external_illuminance'] = (
                sensor_data['mars_base_external_illuminance']
            )
            self.env_values['mars_base_internal_co2'] = (
                sensor_data['mars_base_internal_co2']
            )
            self.env_values['mars_base_internal_oxygen'] = (
                sensor_data['mars_base_internal_oxygen']
            )

            # 6-2. env_values의 값을 출력한다. 이때 환경 정보의 값은 json 형태로 화면에 출력한다.
            # indent=4 : 보기 좋게 들여쓰기 해주는 옵션
            print('현재 환경 값 >> ')
            print(json.dumps(self.env_values, indent=4))

            # 평균 계산용 값 저장
            self.avg_values['mars_base_internal_temperature'].append(
                self.env_values['mars_base_internal_temperature']
            )
            self.avg_values['mars_base_external_temperature'].append(
                self.env_values['mars_base_external_temperature']
            )
            self.avg_values['mars_base_internal_humidity'].append(
                self.env_values['mars_base_internal_humidity']
            )
            self.avg_values['mars_base_external_illuminance'].append(
                self.env_values['mars_base_external_illuminance']
            )
            self.avg_values['mars_base_internal_co2'].append(
                self.env_values['mars_base_internal_co2']
            )
            self.avg_values['mars_base_internal_oxygen'].append(
                self.env_values['mars_base_internal_oxygen']
            )

            count += 1

            # 5초마다 측정하므로 60번이면 5분
            if count == 60:
                average_result = {
                    'mars_base_internal_temperature': round(
                        sum(self.avg_values['mars_base_internal_temperature']) / 60, 2
                    ),
                    'mars_base_external_temperature': round(
                        sum(self.avg_values['mars_base_external_temperature']) / 60, 2
                    ),
                    'mars_base_internal_humidity': round(
                        sum(self.avg_values['mars_base_internal_humidity']) / 60, 2
                    ),
                    'mars_base_external_illuminance': round(
                        sum(self.avg_values['mars_base_external_illuminance']) / 60, 2
                    ),
                    'mars_base_internal_co2': round(
                        sum(self.avg_values['mars_base_internal_co2']) / 60, 4
                    ),
                    'mars_base_internal_oxygen': round(
                        sum(self.avg_values['mars_base_internal_oxygen']) / 60, 2
                    )
                }

                print('5분 평균 환경 값 >> ')
                print(json.dumps(average_result, indent=4))

                # 다음 5분 평균 계산을 위해 초기화
                count = 0
                self.avg_values = {
                    'mars_base_internal_temperature': [],
                    'mars_base_external_temperature': [],
                    'mars_base_internal_humidity': [],
                    'mars_base_external_illuminance': [],
                    'mars_base_internal_co2': [],
                    'mars_base_internal_oxygen': []
                }

            # 6-3. 위의 두 가지 동작을 5초에 한번씩 반복한다.
            time.sleep(5)

            # 보너스 1. 특정 키를 입력할 경우 반복적으로 출력되던 화성 기지의 환경에 대한 출력을 멈추고 ‘Sytem stoped….’ 를 출력 할 수 있어야 한다.
            user_input = input("종료하려면 c 입력: ")

            if user_input == "c":
                print("System stoped....")
                break


# 7. MissionComputer 클래스를 RunComputer 라는 이름으로 인스턴스화 한다.
RunComputer = MissionComputer()
# 8. RunComputer 인스턴스의 get_sensor_data() 메소드를 호출해서 지속적으로 환경에 대한 값을 출력 할 수 있도록 한다.
RunComputer.get_sensor_data()