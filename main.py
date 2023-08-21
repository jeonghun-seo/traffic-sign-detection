import cv2
from ultralytics import YOLO

class TrafficSignDetector:
    def __init__(self, model_path, video_path):
        self.model = YOLO(model_path)
        self.video_path = video_path

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
            plots = results[0].plot()
            cv2.imshow("Result Video", plots)
            # q 키를 누르면 종료
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

if __name__ == "__main__":
    model_path = './runs/detect/train4/weights/best.pt'
    video_path = './traffic-sign-to-test.mp4'

    detector = TrafficSignDetector(model_path, video_path)
    detector.detect_traffic_signs()
