Quick Start Instructions:

1. Clone the project:
git clone <your-repo-url>
cd SporeScope

2. Create and activate a virtual environment:
python -m venv .venv
source .venv/bin/activate
Windows users: .venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt
Or manually install: firebase-admin, google-cloud-storage, opencv-python, numpy, pillow, python-dotenv

4. Firebase setup:
    • Open Firebase Console
    • Go to Project Settings → Service Accounts
    • Click “Generate new private key” and download the JSON file
    • Rename the file to firebase-adminsdk.json
    • Place the file in the same folder as app.py

5. Optional test:
python test_firebase.py

6. Run the app:
python app.py