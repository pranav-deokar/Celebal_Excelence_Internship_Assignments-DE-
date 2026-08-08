import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def run(script):
    print("\n" + "="*70)
    print(f"RUNNING: {script}")
    print("="*70)
    subprocess.run([sys.executable, str(ROOT / "python" / script)], check=True)

def main():
    run("generate_data.py")
    run("clean_data.py")
    run("load_database.py")
    run("run_sql_analysis.py")
    run("test_edge_cases.py")
    print("\n" + "="*70)
    print("ASSIGNMENT 8 BUILD COMPLETED SUCCESSFULLY")
    print("="*70)
    print("Next: run cli_report.py manually and capture the required screenshots.")

if __name__ == "__main__":
    main()
