echo "Starting Chameleon Script..."

# VENV
source ./bin/activate

# Git
echo "Syncing Files..."
git reset --hard
git checkout main
git pull

# Python
echo "Installing Required Files..."
python3 -m pip install -r requirements.txt

# Run
echo "RUN!"
python3 main.py