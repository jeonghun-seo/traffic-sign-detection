from TRFdetector import TrafficSignDetector
from DBmanager import DatabaseManager
import config

if __name__ == "__main__":
    # 데이터베이스 연결 정보를 config.py에서 가져옴
    db_manager = DatabaseManager(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)

    detector = TrafficSignDetector(config.MODEL_PATH, config.VIDEO_PATH, db_manager)
    detector.detect_traffic_signs()

    # 작업이 끝난 후 데이터베이스 연결 종료
    db_manager.close()
