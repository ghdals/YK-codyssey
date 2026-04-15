import json
import platform
import os
import psutil


class MissionComputer:

    # 설정 파일 읽기 (true / false)
    def load_settings(self):
        settings = {}

        try:
            with open("setting.txt", "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()

                    if not line or "=" not in line:
                        continue

                    key, value = line.split("=", 1)
                    settings[key.strip()] = value.strip().lower() == "true"

        except FileNotFoundError:
            print("setting.txt 파일을 찾을 수 없습니다.")

        return settings

    # 시스템 정보 출력 (JSON)
    def get_mission_computer_info(self):
        settings = self.load_settings()
        info = {}

        if settings.get("operating_system"):
            info["operating_system"] = platform.system()

        if settings.get("operating_system_version"):
            info["operating_system_version"] = platform.version()

        if settings.get("cpu_type"):
            info["cpu_type"] = platform.processor()

        if settings.get("cpu_core_count"):
            info["cpu_core_count"] = os.cpu_count()

        if settings.get("memory_size_gb"):
            memory_gb = round(psutil.virtual_memory().total / (1024 ** 3), 2)
            info["memory_size_gb"] = memory_gb

        print(json.dumps(info, indent=4, ensure_ascii=False))

    # 시스템 부하 출력 (JSON)
    def get_mission_computer_load(self):
        settings = self.load_settings()
        load = {}

        if settings.get("cpu_usage_percent"):
            load["cpu_usage_percent"] = psutil.cpu_percent(interval=1)

        if settings.get("memory_usage_percent"):
            load["memory_usage_percent"] = psutil.virtual_memory().percent

        print(json.dumps(load, indent=4, ensure_ascii=False))


# 인스턴스 생성
runComputer = MissionComputer()

# 메소드 실행
runComputer.get_mission_computer_info()
runComputer.get_mission_computer_load()