import subprocess

# Ensure these are the correct paths to your scripts
nonthread_path = "nonthread.py"
neutral_path = "neutral.py"
idk="idk.py"
while True:
    try:
        # Start the target Python file as a subprocess and wait for it to complete  
        result = subprocess.run(["python", nonthread_path], check=True)
    except subprocess.CalledProcessError as e:
        # This catches errors where the subprocess exits with a non-zero status (which `check=True` turns into exceptions)
        print("Error:", e)
        subprocess.run(["python", neutral_path])
