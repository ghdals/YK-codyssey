# 랜덤값을 만들기 위해 사용
import random

# 더미 센서 클래스
class DummySensor:
    # env_values를 만듦
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }

    # set_env(self) : 환경값을 랜덤으로 채우는 함수
    # round(..., 2) : 소수 둘째 자리까지(안하면 소수의 자릿수가 길어지길래)
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

    # env_values 값을 반환
    def get_env(self):
        return self.env_values


# 객체 생성
ds = DummySensor()
# 랜덤값 채우기
ds.set_env()
# 현재값 확인
print(ds.get_env())