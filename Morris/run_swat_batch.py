import os
import shutil
import subprocess
from pathlib import Path
import pandas as pd

# === 사용자 설정 ============================================================
MODEL_DIR = r"C:\Workspace\1010_Scenario1_LC10_CP1"
SWAP_DIRS = [
    (r"C:\Workspace\swap1\swap.0001", "iter_0001"),
    (r"C:\Workspace\swap1\swap.0002", "iter_0002"),
]
OUTPUT_DIR = r"C:\Workspace\Output"
RCH_FILENAME = "output.rch"
# ===========================================================================


def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def copy_tree_overwrite(src: Path, dst: Path):
    """src의 모든 파일/폴더를 dst에 덮어쓰기 복사"""
    for root, dirs, files in os.walk(src):
        rel = Path(root).relative_to(src)
        target_root = dst / rel
        target_root.mkdir(parents=True, exist_ok=True)
        for d in dirs:
            (target_root / d).mkdir(parents=True, exist_ok=True)
        for f in files:
            s = Path(root) / f
            t = target_root / f
            shutil.copy2(s, t)


def run_swat(model_dir: Path):
    """model_dir에서 swat.exe 실행 후 완료까지 대기"""
    exe = model_dir / "swat.exe"
    if not exe.exists():
        raise FileNotFoundError(f"swat.exe not found in: {exe}")
    subprocess.run([str(exe)], cwd=str(model_dir), check=True)


def parse_flow_from_rch(rch_path: Path) -> pd.DataFrame:
    """
    output.rch에서 FLOW_INcms, FLOW_OUTcms 두 컬럼 추출.
    - 데이터 라인 첫 토큰 'REACH' 보정(+1 offset)
    - 공백/푸터 자동 무시
    """
    if not rch_path.exists():
        raise FileNotFoundError(f"output.rch not found: {rch_path}")

    with rch_path.open("r", encoding="latin-1", errors="ignore") as f:
        lines = [ln.rstrip("\n") for ln in f]

    # 헤더 찾기
    header_idx, header_line = None, None
    for i, line in enumerate(lines):
        if "FLOW_OUTcms" in line and "FLOW_INcms" in line:
            header_idx, header_line = i, line
            break
    if header_idx is None:
        raise ValueError("Could not locate FLOW_INcms/FLOW_OUTcms header in output.rch")

    # 헤더 파싱
    cols = header_line.split()
    try:
        in_idx = cols.index("FLOW_INcms")
        out_idx = cols.index("FLOW_OUTcms")
    except ValueError:
        raise ValueError("Header line found but missing FLOW_INcms or FLOW_OUTcms.")

    data_start = header_idx + 1
    flow_in, flow_out = [], []

    for raw in lines[data_start:]:
        line = raw.strip()
        if not line or line.upper().startswith("REACH OUTPUT"):
            continue
        parts = line.split()
        if not parts:
            continue

        # 데이터 오프셋 (맨 앞에 REACH 추가 여부 보정)
        offset = 1 if parts[0].upper() == "REACH" else 0
        in_pos = in_idx + offset
        out_pos = out_idx + offset

        if len(parts) <= max(in_pos, out_pos):
            continue

        try:
            in_val = float(parts[in_pos])
            out_val = float(parts[out_pos])
        except ValueError:
            continue

        flow_in.append(in_val)
        flow_out.append(out_val)

    return pd.DataFrame({
        "FLOW_INcms": flow_in,
        "FLOW_OUTcms": flow_out
    })


def main():
    model_dir = Path(MODEL_DIR)
    output_dir = Path(OUTPUT_DIR)
    ensure_dir(output_dir)

    for swap_path_str, tag in SWAP_DIRS:
        swap_dir = Path(swap_path_str)
        if not swap_dir.exists():
            raise FileNotFoundError(f"Swap dir not found: {swap_dir}")

        print(f"\n=== [{tag}] Copy from {swap_dir} → {model_dir} ===")
        copy_tree_overwrite(swap_dir, model_dir)

        print(f"=== [{tag}] Run swat.exe ===")
        run_swat(model_dir)

        print(f"=== [{tag}] Parse {RCH_FILENAME} (FLOW_INcms, FLOW_OUTcms) ===")
        rch_path = model_dir / RCH_FILENAME
        df = parse_flow_from_rch(rch_path)

        out_csv = output_dir / f"FLOW_IOcms_{tag}.csv"
        df.to_csv(out_csv, index=False)
        print(f"Saved: {out_csv}")

    print("\nAll iterations completed.")


if __name__ == "__main__":
    main()
