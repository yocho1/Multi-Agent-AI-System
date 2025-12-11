"""Debug script to understand the token verification issue."""
import os
import sys
import json
import base64
from pathlib import Path

# Set up paths
workspace_root = Path(__file__).parent
sys.path.insert(0, str(workspace_root))

os.environ["FIREBASE_CREDENTIALS_PATH"] = str(workspace_root / "firebase-credentials.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(workspace_root / "firebase-credentials.json")

# Import libraries
import jwt
import firebase_admin
from firebase_admin import credentials, auth

print("=" * 80)
print("TOKEN VERIFICATION DEBUG SCRIPT")
print("=" * 80)

print(f"\njwt version: {jwt.__version__}")
print(f"firebase-admin version: {firebase_admin.__version__}")

# Initialize Firebase
try:
    firebase_admin.get_app()
    print("\nFirebase already initialized")
except ValueError:
    print("\nInitializing Firebase...")
    cred_path = workspace_root / "firebase-credentials.json"
    cred = credentials.Certificate(str(cred_path))
    firebase_admin.initialize_app(cred)
    print(f"Firebase initialized with credentials from: {cred_path}")

# Test token from frontend
test_token = input("\nEnter a Firebase ID token from the frontend:\n> ").strip()

if test_token:
    print(f"\nToken length: {len(test_token)}")
    
    # Decode without verification to see structure
    parts = test_token.split('.')
    print(f"Token parts: {len(parts)}")
    
    if len(parts) == 3:
        try:
            # Decode header
            header_data = parts[0] + '=' * (4 - len(parts[0]) % 4)
            header = json.loads(base64.urlsafe_b64decode(header_data))
            print(f"\nToken Header: {json.dumps(header, indent=2)}")
            
            # Decode payload
            payload_data = parts[1] + '=' * (4 - len(parts[1]) % 4)
            payload = json.loads(base64.urlsafe_b64decode(payload_data))
            print(f"\nToken Payload: {json.dumps(payload, indent=2)}")
        except Exception as e:
            print(f"Error decoding token: {e}")
    
    # Try to verify with firebase-admin
    print("\n" + "=" * 80)
    print("Attempting Firebase token verification...")
    print("=" * 80)
    
    try:
        decoded = auth.verify_id_token(test_token)
        print("\n✓ Token verified successfully!")
        print(f"User UID: {decoded.get('uid')}")
        print(f"Email: {decoded.get('email')}")
    except Exception as e:
        print(f"\n✗ Token verification failed!")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {e}")
        
        # Try manual verification with PyJWT
        print("\n" + "-" * 80)
        print("Attempting manual PyJWT verification...")
        print("-" * 80)
        
        try:
            # Get unverified header to see algorithm
            unverified_header = jwt.get_unverified_header(test_token)
            print(f"Token algorithm: {unverified_header.get('alg')}")
            print(f"Token key ID: {unverified_header.get('kid')}")
            
            # Try decoding without verification
            decoded_unverified = jwt.decode(test_token, options={"verify_signature": False})
            print("\nUnverified decode successful!")
            print(f"Claims: {json.dumps(decoded_unverified, indent=2)}")
            
            # Try with different algorithms
            print("\nAttempting to decode with various algorithms...")
            for alg in ['RS256', 'HS256', 'ES256']:
                try:
                    result = jwt.decode(test_token, "", algorithms=[alg], options={"verify_signature": False})
                    print(f"✓ Algorithm {alg}: OK (no signature verification)")
                except Exception as alg_e:
                    print(f"✗ Algorithm {alg}: {alg_e}")
                    
        except Exception as jwt_e:
            print(f"\nPyJWT error: {jwt_e}")
            
else:
    print("No token provided")
