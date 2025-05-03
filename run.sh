echo "Starting Chameleon Script..."

# Git
echo "Syncing Files..."
git reset --hard
git checkout main
git pull

# Python
echo "Installing Required Files..."

# Run
echo "RUN!"
sudo python3 main.py