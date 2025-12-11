"""Detailed debugging of Firebase token verification."""
import os
import sys
from pathlib import Path

# Set paths
workspace_root = Path(__file__).parent.resolve()
sys.path.insert(0, str(workspace_root))

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(workspace_root / "firebase-credentials.json")

import firebase_admin
from firebase_admin import credentials, auth, exceptions as fb_exceptions
import jwt

print("=" * 80)
print("FIREBASE TOKEN VERIFICATION DEBUG")
print("=" * 80)

print(f"PyJWT version: {jwt.__version__}")
print(f"firebase-admin version: {firebase_admin.__version__}")
print(f"Workspace: {workspace_root}")
print(f"Credentials: {workspace_root / 'firebase-credentials.json'}")

# Initialize Firebase
try:
    app = firebase_admin.get_app()
    print("Firebase already initialized")
except ValueError:
    cred = credentials.Certificate(str(workspace_root / "firebase-credentials.json"))
    app = firebase_admin.initialize_app(cred)
    print("Firebase initialized")

print("\n" + "=" * 80)
print("TEST 1: Check if we can fetch Google certificates")
print("=" * 80)

try:
    import requests
    # Try to fetch Google's public certificates
    certs_url = "https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com"
    resp = requests.get(certs_url, timeout=5)
    if resp.status_code == 200:
        certs = resp.json()
        print(f"✓ Successfully fetched Google certificates")
        print(f"  Certificate IDs: {list(certs.keys())}")
    else:
        print(f"✗ Failed to fetch certificates: {resp.status_code}")
except Exception as e:
    print(f"✗ Error fetching certificates: {e}")

print("\n" + "=" * 80)
print("TEST 2: Create and verify a custom token (baseline test)")
print("=" * 80)

try:
    # This should work - creating a custom token
    custom_token = auth.create_custom_token("test-user-123", {"admin": True})
    custom_token_str = custom_token.decode('utf-8') if isinstance(custom_token, bytes) else custom_token
    print(f"✓ Custom token created: {custom_token_str[:50]}...")
    
    # Try to verify as ID token (should fail - that's expected)
    try:
        auth.verify_id_token(custom_token_str)
        print("✗ ERROR: Custom token should not verify as ID token")
    except fb_exceptions.InvalidIdTokenError:
        print("✓ Expected: Custom token correctly rejected as ID token")
except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {e}")

print("\n" + "=" * 80)
print("INSTRUCTIONS FOR TESTING WITH REAL TOKEN")
print("=" * 80)
print("""
1. Open http://localhost:3000 in browser
2. Log in with your Firebase account
3. Open browser developer console (F12)
4. Go to Application > Local Storage > http://localhost:3000
5. Find 'Firebase Auth Token' or similar
6. OR run this in browser console:
   (await firebase.auth().currentUser.getIdToken()).then(t => console.log(t))
7. Copy the token and run this script with: --token "YOUR_TOKEN_HERE"
""")

# Check if token is provided as argument
if len(sys.argv) > 2 and sys.argv[1] == "--token":
    test_token = sys.argv[2]
    print("\n" + "=" * 80)
    print("TEST 3: Verifying provided Firebase ID token")
    print("=" * 80)
    
    print(f"Token length: {len(test_token)}")
    parts = test_token.split('.')
    print(f"Token parts: {len(parts)} (should be 3)")
    
    if len(parts) == 3:
        # Decode header to see algorithm
        import base64
        import json
        
        try:
            header_part = parts[0]
            # Add padding if needed
            header_part += '=' * (4 - len(header_part) % 4)
            header = json.loads(base64.urlsafe_b64decode(header_part))
            print(f"\nToken Header:")
            print(f"  Algorithm: {header.get('alg')}")
            print(f"  Key ID: {header.get('kid')}")
            
            payload_part = parts[1]
            payload_part += '=' * (4 - len(payload_part) % 4)
            payload = json.loads(base64.urlsafe_b64decode(payload_part))
            print(f"\nToken Claims:")
            for k, v in list(payload.items())[:5]:
                print(f"  {k}: {v}")
        except Exception as e:
            print(f"Error decoding: {e}")
    
    print("\nAttempting verification...")
    try:
        decoded = auth.verify_id_token(test_token)
        print("\n✓ TOKEN VERIFIED SUCCESSFULLY!")
        print(f"User UID: {decoded.get('uid')}")
        print(f"Email: {decoded.get('email')}")
        print(f"All claims: {list(decoded.keys())}")
    except fb_exceptions.InvalidIdTokenError as e:
        print(f"✗ InvalidIdTokenError: {e}")
    except fb_exceptions.ExpiredIdTokenError as e:
        print(f"✗ ExpiredIdTokenError: {e}")
    except ValueError as e:
        print(f"✗ ValueError (PyJWT error): {e}")
    except Exception as e:
        print(f"✗ {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
else:
    print("\nTo test with a real token, run:")
    print(f"  python {sys.argv[0]} --token <YOUR_TOKEN_HERE>")
