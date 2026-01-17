import os
import shutil

base_dir = r"C:\Workspace\MorrisRun\Model"

# P1 ~ P20 폴더 순회
for i in range(1, 21):
    folder_name = f"1010_Scenario1_LC10_P{i}"
    folder_path = os.path.join(base_dir, folder_name)

    if not os.path.exists(folder_path):
        print(f"폴더 없음: {folder_path}")
        continue

    # 안의 모든 파일/폴더 확인
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        # "1010_Scenario1_LC10_CP1"만 제외
        if item == "1010_Scenario1_LC10_CP1":
            continue

        # 폴더일 경우 전체 삭제
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
            print(f"삭제된 폴더: {item_path}")
        else:
            os.remove(item_path)
            print(f"삭제된 파일: {item_path}")

print("✅ 삭제 작업 완료!")
