import datetime
import subprocess
from pathlib import Path

project_dir = Path.cwd()

task_file = project_dir / 'task.txt'
parser_file = project_dir / 'parser.py'
python_path = project_dir / 'venv' / 'Scripts' / 'python.exe'

with open(task_file, 'a') as file:
    file.write(f'{datetime.datetime.now()} - The script ran\n')

subprocess.run([str(python_path), str(parser_file)])