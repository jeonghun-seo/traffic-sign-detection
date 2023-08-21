import cv2
from ultralytics import YOLO
from DBmanager import DatabaseManager 

class TrafficSignDetector:
    def __init__(self, model_path, video_path, db_manager):
        self.model = YOLO(model_path)
        self.video_path = video_path
        self.db_manager = db_manager  # 데이터베이스 매니저 객체를 저장합니다.

    def detect_traffic_signs(self):
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise Exception("영상 파일을 열 수 없습니다.")
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            results = self.model(frame)
            for result in results:
                clist = result.boxes.cls
                cls = set()
                for cno in clist:
                    cls.add(self.model.names[int(cno)])
                print(cls)
                print(clist)
                
                # 데이터베이스에 클래스와 정확도 저장
                for class_name, score in zip(cls, result.boxes.scores):
                    query = "INSERT INTO detected_objects (class_name, score) VALUES (%s, %s)"
                    values = (class_name, score)
                    self.db_manager.execute_query(query, values)
                    
            plots = results[0].plot()
            cv2.imshow("Result Video", plots)
            # q 키를 누르면 종료
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
