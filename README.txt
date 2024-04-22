How to run application

# Create virtual environment
python -m venv .venv

# Activate virtual environment
./.venv/Scripts/activate

# Install requirements from requirements.txt
pip install -r requirements.txt

# Run generator.py to generate pair of RSA keys
./generator.py

# Run app.py to run application
./app.py