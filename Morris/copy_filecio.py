import os
import shutil

base_dir = r"C:\Workspace\MorrisRun\Model"
src_file = r"C:\Workspace\MorrisRun\file.cio"

# 원본 파일이 존재하는지 확인
if not os.path.exists(src_file):
    raise FileNotFoundError(f"원본 파일 없음: {src_file}")

# P1~P20 폴더 순회
for i in range(1, 21):
    cp1_path = os.path.join(base_dir, f"1010_Scenario1_LC10_P{i}", "1010_Scenario1_LC10_CP1")

    if os.path.exists(cp1_path):
        dst_file = os.path.join(cp1_path, "file.cio")
        shutil.copy2(src_file, dst_file)  # 같은 이름 있으면 덮어쓰기
        print(f"✅ 복사 완료: {dst_file}")
    else:
        print(f"⚠️ CP1 폴더 없음: {cp1_path}")

print("작업 끝!")
