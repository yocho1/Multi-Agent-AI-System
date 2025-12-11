"""Test Firebase token verification in isolation."""
import os
import sys
from pathlib import Path

# Set up environment
workspace_root = Path(__file__).parent
sys.path.insert(0, str(workspace_root))

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(workspace_root / "firebase-credentials.json")

# Check if credentials file exists and is valid JSON
cred_path = workspace_root / "firebase-credentials.json"
print(f"Credentials file: {cred_path}")
print(f"Exists: {cred_path.exists()}")

if cred_path.exists():
    import json
    with open(cred_path) as f:
        cred_data = json.load(f)
    print(f"Service account email: {cred_data.get('client_email')}")
    print(f"Project ID: {cred_data.get('project_id')}")

# Initialize Firebase
import firebase_admin
from firebase_admin import credentials, auth

print("\nInitializing Firebase...")
try:
    firebase_admin.get_app()
    print("Firebase already initialized")
except ValueError:
    cred = credentials.Certificate(str(cred_path))
    firebase_admin.initialize_app(cred)
    print("Firebase initialized")

# Test with a manually created token
print("\nCreating a test token...")
try:
    custom_token = auth.create_custom_token("test-user-123", {"admin": True})
    print(f"Custom token created: {custom_token[:50]}...")
    
    # Now try to verify it
    print("\nVerifying custom token...")
    decoded = auth.verify_id_token(custom_token)
    print(f"ERROR: Should not be able to verify custom token as ID token")
except auth.InvalidIdTokenError as e:
    print(f"Expected error - custom token is not an ID token: {e}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")

print("\n" + "=" * 80)
print("To test with a real Firebase ID token:")
print("1. Open frontend at http://localhost:3000")
print("2. Log in with your Firebase account")
print("3. Open browser console and run:")
print("   await getAuth().currentUser.getIdToken()")
print("4. Copy the token and paste it in the debug script")
print("=" * 80)
