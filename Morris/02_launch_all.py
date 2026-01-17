import subprocess
from pathlib import Path
import time

base_dir = Path(r"C:\Workspace\MorrisRun").resolve()
python_exe = "python"

scripts = [f"run_P{i}.py" for i in range(1, 6)]

# wt.exe 명령 구성
commands = []
for i, script in enumerate(scripts):
    script_path = base_dir / script
    if i == 0:
        commands.append(f'new-tab -d "{base_dir}" {python_exe} "{script_path}"')
    else:
        commands.append(f'; new-tab -d "{base_dir}" {python_exe} "{script_path}"')

# 전체 명령 조합
cmd = "wt " + " ".join(commands)
print("Launching all 10 scripts in Windows Terminal tabs...")
subprocess.run(cmd, shell=True)
print("✅ All scripts launched in WT tabs successfully!")
