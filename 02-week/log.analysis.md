# Mission Computer Log Analysis.

## 로그 분석.
mission_computer_main.log 파일을 확인한 결과 로켓은 발사 준비, 이륙, 궤도 진입, 위성 배치, 재진입 및 착륙까지 정상적으로 진행된 것으로 보임.

2023-08-27 11:30:00,INFO,Mission completed successfully. Recovery team dispatched.
라는 로그가 기록되어 임무가 성공적으로 완수된 것으로 확인됨.

하지만 이후 다음과 같은 로그가 기록됨.
2023-08-27 11:35:00,INFO,Oxygen tank unstable.
2023-08-27 11:40:00,INFO,Oxygen tank explosion.
2023-08-27 12:00:00,INFO,Center and mission control systems powered down.

## 사고의 원인.
로그를 보면 산소 탱크가 불안정 상태가 된 이후 산소 탱크 폭발이 발생함.
따라서 사고의 직접적인 원인은 산소 탱크의 상태 이상으로 판단됨.
