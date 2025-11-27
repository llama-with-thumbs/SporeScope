Quick Start Instructions:

This project is designed to run on Raspberry Pi devices of different generations equipped with different camera modules. Due to hardware and configuration variations, some setup errors may occur during installation.

1. Clone the project:
    git clone https://github.com/llama-with-thumbs/SporeScope.git
    cd SporeScope

2. Create and activate a virtual environment:
    python3 -m venv .venv
    source .venv/bin/activate

3. Install dependencies:
    pip install -r requirements.txt

4. Firebase setup:
    create firebase-adminsdk.json with credentials 

5. Create config.py
    Add basic settings such as:
    INTERVAL_SECONDS, RAW_COORDINATES, ROTATION_ANGLE, CHAMBER, PLATE_ID

6. Run the app:
    python app.py

7. Run using tmux (for Raspberry Pi)
    tmux
    python app.py
    Ctrl+B then D to detach
    tmux attach to rejoin
   