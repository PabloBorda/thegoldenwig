import subprocess
from tqdm import tqdm
import time

def execute_script(script_name):
    """Execute a script using Python's subprocess module."""
    subprocess.run(["python", script_name], check=True)

def main():
    scripts = [
        "websites.py",
        "news_iterator.py",
        "associations_to_gpt.py",
        "news_to_wordpress.py"
    ]

    total_scripts = len(scripts)
    progress_bar = tqdm(total=total_scripts, desc="Executing Scripts", unit="script")

    for script in scripts:
        execute_script(script)
        progress_bar.update(1)
        # Optional: Add a sleep time to visually see the progress bar update for quick scripts
        # time.sleep(1)

    progress_bar.close()

if __name__ == "__main__":
    main()
