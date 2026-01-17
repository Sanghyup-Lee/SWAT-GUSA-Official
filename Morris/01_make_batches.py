import textwrap
from pathlib import Path

#Folder path (User modify)
base_model_dir = r"C:\Workspace\Sobol\4_set_desktop_run\Test_sim5\Models"
swap_root = r"C:\Workspace\Sobol\4_set_desktop_run\Test_sim5\Warehouse\Output-1-1"
output_dir = r"C:\Workspace\Sobol\4_set_desktop_run\Test_sim5\Outputs"

# Simulation start number (User modify)
base_start = 1

template = textwrap.dedent('''\
import os
import shutil
import subprocess
from pathlib import Path
import pandas as pd

MODEL_DIR = r"{model_dir}"
SWAP_DIRS = [
{swap_dirs}
]
OUTPUT_DIR = r"{output_dir}"
RCH_FILENAME = "output.rch"

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def copy_tree_overwrite(src: Path, dst: Path):
    for root, dirs, files in os.walk(src):
        rel = Path(root).relative_to(src)
        target_root = dst / rel
        target_root.mkdir(parents=True, exist_ok=True)
        for f in files:
            shutil.copy2(Path(root)/f, target_root/f)

def run_swat(model_dir: Path):
    exe = model_dir / "swat.exe"
    subprocess.run([str(exe)], cwd=str(model_dir), check=True)

def parse_flow_from_rch(rch_path: Path) -> pd.DataFrame:
    with rch_path.open("r", encoding="latin-1", errors="ignore") as f:
        lines = [ln.rstrip("\\n") for ln in f]
    header_idx = next(i for i,l in enumerate(lines) if "FLOW_OUTcms" in l and "FLOW_INcms" in l)
    cols = lines[header_idx].split()
    in_idx, out_idx = cols.index("FLOW_INcms"), cols.index("FLOW_OUTcms")
    data_start = header_idx + 1
    flow_in, flow_out = [], []
    for raw in lines[data_start:]:
        parts = raw.split()
        if not parts: continue
        offset = 1 if parts[0].upper()=="REACH" else 0
        try:
            flow_in.append(float(parts[in_idx+offset]))
            flow_out.append(float(parts[out_idx+offset]))
        except: continue
    return pd.DataFrame({{"FLOW_INcms":flow_in, "FLOW_OUTcms":flow_out}})

def main():
    model_dir = Path(MODEL_DIR)
    output_dir = Path(OUTPUT_DIR)
    ensure_dir(output_dir)
    for swap_path_str, tag in SWAP_DIRS:
        swap_dir = Path(swap_path_str)
        print(f"\\n=== [{{tag}}] Copy from {{swap_dir}} → {{model_dir}} ===")
        copy_tree_overwrite(swap_dir, model_dir)
        print(f"=== [{{tag}}] Run swat.exe ===")
        run_swat(model_dir)
        df = parse_flow_from_rch(model_dir / RCH_FILENAME)
        out_csv = output_dir / f"FLOW_IOcms_{{tag}}.csv"
        df.to_csv(out_csv, index=False)
        print(f"Saved: {{out_csv}}")
    print("\\nAll iterations completed.")

if __name__ == "__main__":
    main()
''')

# if 10 sim parallel : i*10 , start + 9
# if 5 sim parallel : i*20, start +19
for i in range(5):
    start = base_start + i*20
    end = start + 19
    model_dir = fr"{base_model_dir}\1010_Scenario1_LC10_P{i+1}"
    swap_lines = []
    for j in range(start, end+1):
        swap_lines.append(f'    (r"{swap_root}\\swap.{j:04d}", "iter_{j:04d}"),')
    swap_text = "\n".join(swap_lines)
    code = template.format(model_dir=model_dir, swap_dirs=swap_text, output_dir=output_dir)
    Path(f"run_P{i+1}.py").write_text(code, encoding="utf-8")

print("✅ %s-%s Script is generated."%(base_start,end))
