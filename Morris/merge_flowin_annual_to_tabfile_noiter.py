import pandas as pd
from pathlib import Path

# === 사용자 설정 ============================================================
ANNUAL_DIR = Path(r"C:\Workspace\MorrisRun\Selected\Annual")  # Annual 폴더
OUTPUT_FILE = Path(r"C:\Workspace\MorrisRun\Final_FLOWIN_Annual.txt")  # 최종 출력 파일

YEARS = list(range(2011, 2021))  # 2011~2020
# ===========================================================================


def extract_flowin_values(df: pd.DataFrame) -> list:
    """FLOW_INcms의 연도별 mean, max, min을 순서대로 평탄화"""
    vals = []
    for year in YEARS:
        row = df[df["Year"] == year]
        if row.empty:
            vals.extend([0.0, 0.0, 0.0])  # 해당 연도 없을 경우 0으로 채움
        else:
            r = row.iloc[0]
            vals.extend([r["FLOW_INcms_mean"], r["FLOW_INcms_max"], r["FLOW_INcms_min"]])
    return vals


def main():
    annual_files = sorted(ANNUAL_DIR.glob("*_annual_stats.csv"))
    if not annual_files:
        print("❌ No annual stats files found.")
        return

    all_records = []
    for f in annual_files:
        df = pd.read_csv(f)
        vals = extract_flowin_values(df)
        all_records.append(vals)

    # 헤더 생성
    headers = []
    for y in YEARS:
        headers += [f"{y}_mean", f"{y}_max", f"{y}_min"]

    result_df = pd.DataFrame(all_records, columns=headers)

    # 탭 구분 파일로 저장 (Iter 열 없이)
    result_df.to_csv(OUTPUT_FILE, index=False, sep="\t", header=True)

    print(f"✅ Tab-separated file created: {OUTPUT_FILE}")
    print(f"📈 Total iterations: {len(result_df)}")
    print(f"📊 Total columns: {len(result_df.columns)} ({headers[-1]} is last column)")


if __name__ == "__main__":
    main()
