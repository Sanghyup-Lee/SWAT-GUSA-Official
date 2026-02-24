import os
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

# === 사용자 설정 ============================================================
ROOT_DIR = Path(r"C:\Workspace\MorrisRun\Output")

# 입력 폴더 목록
FOLDERS = [
    "Output 1-200",
    "Output 201-400",
    "Output 401-600",
    "Output 601-800",
    "Output 801-1000",
    "Output 1001-1200",
]

# 결과 저장 폴더
SAVE_DIR = Path(r"C:\Workspace\MorrisRun\Selected")

# 🎯 추출 시작행 (1-based)
START_ROW = 113
# 🎯 추출 간격
STEP = 175

# 🎯 시작 날짜 (연속 증가)
START_DATE = datetime(2011, 1, 1)
# ===========================================================================


def extract_and_save_each(file: Path, start_row: int, step: int, save_dir: Path, start_date: datetime):
    """파일별로 175간격으로 행 추출하고, 날짜는 2011-01-01부터 하루씩 증가"""
    try:
        df = pd.read_csv(file)

        # 175 간격으로 행 선택
        indices = list(range(start_row - 1, len(df), step))
        subset = df.iloc[indices].copy()

        # 날짜 생성 (추출된 행 수만큼)
        dates = [start_date + timedelta(days=i) for i in range(len(subset))]
        subset.insert(0, "Date", [d.strftime("%Y-%m-%d") for d in dates])
        subset.insert(1, "RowIndex", [i + 1 for i in indices])

        # 저장
        out_name = file.stem + "_selected.csv"
        out_path = save_dir / out_name
        subset.to_csv(out_path, index=False)
        print(f"✅ {file.name} → {out_path.name} ({len(subset)} rows)")
    except Exception as e:
        print(f"⚠️ Error processing {file.name}: {e}")


def main():
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    total_files = 0

    for folder_name in FOLDERS:
        folder_path = ROOT_DIR / folder_name
        if not folder_path.exists():
            print(f"⚠️ Folder not found: {folder_path}")
            continue

        print(f"\n📂 Processing folder: {folder_path}")
        for file in folder_path.glob("FLOW_IOcms_iter_*.csv"):
            extract_and_save_each(file, START_ROW, STEP, SAVE_DIR, START_DATE)
            total_files += 1

    print(f"\n🎯 Done! {total_files} files processed.")
    print(f"📁 All selected CSVs saved in: {SAVE_DIR}")


if __name__ == "__main__":
    main()
