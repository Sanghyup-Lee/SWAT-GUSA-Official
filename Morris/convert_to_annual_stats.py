import pandas as pd
from pathlib import Path

# === 사용자 설정 ============================================================
SELECTED_DIR = Path(r"C:\Workspace\MorrisRun\Selected")  # _selected.csv들이 들어있는 폴더
OUTPUT_DIR = SELECTED_DIR / "Annual"                    # 결과 저장 폴더
# ===========================================================================

def process_annual_stats(file: Path, output_dir: Path):
    """하나의 _selected.csv 파일을 연도별 평균/최대/최소로 변환"""
    try:
        df = pd.read_csv(file, parse_dates=["Date"])
        df["Year"] = df["Date"].dt.year

        # 연도별 통계 계산
        grouped = df.groupby("Year")[["FLOW_INcms", "FLOW_OUTcms"]]
        annual_mean = grouped.mean().reset_index()
        annual_max = grouped.max().reset_index()
        annual_min = grouped.min().reset_index()

        # 결과 합치기 (컬럼 이름 구분)
        annual_stats = annual_mean.copy()
        annual_stats.rename(columns={
            "FLOW_INcms": "FLOW_INcms_mean",
            "FLOW_OUTcms": "FLOW_OUTcms_mean"
        }, inplace=True)
        annual_stats["FLOW_INcms_max"] = annual_max["FLOW_INcms"]
        annual_stats["FLOW_OUTcms_max"] = annual_max["FLOW_OUTcms"]
        annual_stats["FLOW_INcms_min"] = annual_min["FLOW_INcms"]
        annual_stats["FLOW_OUTcms_min"] = annual_min["FLOW_OUTcms"]

        # 저장
        output_dir.mkdir(parents=True, exist_ok=True)
        out_name = file.stem.replace("_selected", "_annual_stats") + ".csv"
        out_path = output_dir / out_name
        annual_stats.to_csv(out_path, index=False)

        print(f"✅ {file.name} → {out_path.name}")
    except Exception as e:
        print(f"⚠️ Error processing {file.name}: {e}")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_files = list(SELECTED_DIR.glob("*_selected.csv"))

    if not csv_files:
        print("❌ No '_selected.csv' files found in the Selected folder.")
        return

    for file in csv_files:
        process_annual_stats(file, OUTPUT_DIR)

    print(f"\n🎯 All done! Annual statistics saved in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
