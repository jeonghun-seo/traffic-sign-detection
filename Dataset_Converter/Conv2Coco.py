import os
import json

#원본 어노테이션 경로
anno_dir = 'data\\annotation'
#원본 이미지 경로
image_dir = "data\\images"

#anno_dir 내 어노테이션 리스트업
anno_list = os.listdir(anno_dir)
print(len(anno_list))

#coco_dict에 필요한 이미지, 어노테이션 정보 리스트업
image_temp_dict = []
anno_temp_dict = []

idNum = 1
anno_id_num = 5000
category_id = 0 #카테고리 id 초기화
for anno in anno_list:
    with open(anno_dir +"\\"+ anno, encoding="utf-8-sig",errors="ignore") as json_file:
        json_data = json.load(json_file)
    img_path = anno.replace(".json",".jpg")
    try :
        images = {
            "file_name": json_data["image"]["filename"],
            "height": 1280,
            "width": 720,
            "date_captured": "2023-05-22 11:44:46",
            "id": idNum
        }
    except:
        images = {
            "file_name": img_path,
            "height": 1280,
            "width": 720,
            "date_captured": "2023-05-22 11:44:46",
            "id": idNum
            }
    image_temp_dict.append(images)
    print(anno)

    for annotation in json_data["annotation"]:
        if "type" in annotation and annotation["type"] == "restriction":
            speed = annotation.get("text")
            if speed == "30":
                category_id = 1
            elif speed == "40":
                category_id = 2
            elif speed == "50":
                category_id = 3
            elif speed == "60":
                category_id = 4
            elif speed == "70":
                category_id = 5
            elif speed == "80":
                category_id = 6
            elif speed == "90":
                category_id = 7
            elif speed == "100":
                category_id = 8
            elif speed == "110":
                category_id = 9
            else:
                category_id = 10
        else:
            category_id = 10
        print(category_id)

        try:  # bbox 정보가 존재할 경우
            bbox = [
                annotation["box"][0],
                annotation["box"][1],
                annotation["box"][2] - annotation["box"][0],
                annotation["box"][3] - annotation["box"][1]
            ]

            annotations = {
                "segmentation": [],
                "area": "",
                "iscrowd": "",
                "image_id": idNum,
                "bbox": bbox,
                "id": anno_id_num,
                "category_id": category_id,
            }
        except:
            annotations = {
                "segmentation": [],
                "area": "",
                "iscrowd": "",
                "image_id": idNum,
                "category_id": 10,
                "bbox": [],
                "id": anno_id_num,
            }
        anno_temp_dict.append(annotations)
        anno_id_num += 1
    idNum += 1


coco_dict = {}

coco_dict["info"] = {
    "description" : "속도제한표지 인식 데이터셋 ",
    "version" : "1.0",
    "url" : "https://github.com/jeonghun-seo",
    "year" : "2023",
    "contributor" : "Jeong Hun Seo",
    "date_created": "2023/05/22",
}
coco_dict["licenses"] = [
    {"url": "https://github.com/jeonghun-seo","id":"1","name":"한이음 프로젝트" }
]

coco_dict["images"] = image_temp_dict
coco_dict["annotations"] = anno_temp_dict

coco_dict["categories"] = [
    {"supercategory": "traffic_sign", "id": 1, "name": "최고제한속도 30"},
    {"supercategory": "traffic_sign", "id": 2, "name": "최고제한속도 40"},
    {"supercategory": "traffic_sign", "id": 3, "name": "최고제한속도 50"},
    {"supercategory": "traffic_sign", "id": 4, "name": "최고제한속도 60"},
    {"supercategory": "traffic_sign", "id": 5, "name": "최고제한속도 70"},
    {"supercategory": "traffic_sign", "id": 6, "name": "최고제한속도 80"},
    {"supercategory": "traffic_sign", "id": 7, "name": "최고제한속도 90"},
    {"supercategory": "traffic_sign", "id": 8, "name": "최고제한속도 100"},
    {"supercategory": "traffic_sign", "id": 9, "name": "최고제한속도 110"},
    {"supercategory": "traffic_sign", "id": 10, "name": "normal traffic sign"},
]

with open("runs\coco.json", 'w', encoding="utf-8") as f :
    json.dump(coco_dict, f, ensure_ascii=False)
    print("완료했습니다.")
