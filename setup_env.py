import subprocess
import sys
import jupytext

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install required packages
with open('requirements.txt', 'r') as f:
    packages = f.read().splitlines()

print("Installing required packages...")
for package in packages:
    install(package)

# Convert welcome.py to welcome.ipynb
print("Creating Jupyter notebook...")
notebook = jupytext.read('welcome.py')
jupytext.write(notebook, 'welcome.ipynb')

print("Running linting and formatting...")
subprocess.run(["ruff", "check", "."])
subprocess.run(["black", "."])

print("Running tests...")
subprocess.run(["pytest"])

print("Setup complete!")