echo "Starting Chameleon Script..."

# Git
echo "Syncing Files..."
git reset --hard
git checkout main
git pull

# Python
echo "Installing Required Files..."
sudo python3 -m pip install -r requirements.txt

# Run
echo "RUN!"
sudo python3 main.py