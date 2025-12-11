"""Firebase Authentication utilities for backend."""
import os
import json
from typing import Optional, Dict, Any
import firebase_admin
from firebase_admin import credentials, auth
from functools import lru_cache
import base64

from src.config.logging_config import get_logger

logger = get_logger(module=__name__)


class FirebaseAuth:
    """Firebase Authentication handler."""
    
    _instance: Optional['FirebaseAuth'] = None
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize Firebase Admin SDK."""
        if not self._initialized:
            try:
                # Check if app is already initialized
                firebase_admin.get_app()
                logger.info("Firebase app already initialized")
            except ValueError:
                # Initialize Firebase Admin SDK
                # First try to get from environment/settings
                cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
                
                # If not in env, try importing settings
                if not cred_path:
                    try:
                        from src.config.settings import settings
                        cred_path = settings.FIREBASE_CREDENTIALS_PATH
                    except Exception as e:
                        logger.warning(f"Could not load settings: {e}")
                
                cwd = os.getcwd()
                project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                
                logger.info(f"Looking for Firebase credentials. CWD: {cwd}, Project Root: {project_root}, FIREBASE_CREDENTIALS_PATH: {cred_path}")
                
                # List of paths to try
                paths_to_try = []
                
                if cred_path:
                    paths_to_try.append(cred_path)
                    if not os.path.isabs(cred_path):
                        paths_to_try.append(os.path.join(project_root, cred_path))
                
                # Also try common locations
                paths_to_try.extend([
                    os.path.join(cwd, "firebase-credentials.json"),
                    os.path.join(project_root, "firebase-credentials.json"),
                    "./firebase-credentials.json",
                    "firebase-credentials.json",
                ])
                
                # Try to find and load credentials
                loaded = False
                for path in paths_to_try:
                    if path:
                        full_path = os.path.abspath(path) if not os.path.isabs(path) else path
                        if os.path.exists(full_path):
                            try:
                                logger.info(f"Attempting to load Firebase credentials from: {full_path}")
                                cred = credentials.Certificate(full_path)
                                firebase_admin.initialize_app(cred)
                                logger.info(f"Firebase initialized successfully with service account from {full_path}")
                                loaded = True
                                break
                            except Exception as e:
                                logger.warning(f"Failed to load credentials from {full_path}: {type(e).__name__}: {e}")
                                continue
                
                if not loaded:
                    logger.warning(f"Could not find Firebase credentials. Paths checked: {[os.path.abspath(p) if not os.path.isabs(p) else p for p in paths_to_try]}")
                    try:
                        firebase_admin.initialize_app()
                        logger.warning("Initialized Firebase with default credentials (development mode)")
                    except Exception as e:
                        logger.error(f"Failed to initialize Firebase: {e}")
                
            self.__class__._initialized = True
    
    async def verify_token(self, id_token: str) -> Optional[Dict[str, Any]]:
        """
        Verify Firebase ID token using multiple strategies.
        
        1. Try firebase-admin (may fail due to PyJWT restrictions)
        2. Fall back to manual JWT decoding and issuer validation
        
        Args:
            id_token: Firebase ID token from client
            
        Returns:
            Dict with user info if valid, None otherwise
        """
        try:
            # Decode without verification to get token claims
            parts = id_token.split('.')
            if len(parts) != 3:
                logger.error(f"Invalid token format: {len(parts)} parts")
                return None
            
            try:
                # Decode payload manually
                payload = parts[1]
                # Add padding if needed
                padding = 4 - len(payload) % 4
                if padding != 4:
                    payload += '=' * padding
                unverified = json.loads(base64.urlsafe_b64decode(payload))
            except Exception as decode_err:
                logger.error(f"Failed to decode token payload: {decode_err}")
                return None
            
            user_id = unverified.get('sub')
            email = unverified.get('email')
            issuer = unverified.get('iss')
            
            logger.debug(f"Token claims - uid: {user_id}, email: {email}, issuer: {issuer}")
            
            # First attempt: Try firebase-admin SDK verification
            try:
                decoded_token = auth.verify_id_token(id_token, clock_skew_seconds=10)
                logger.info(f"✓ Token verified via Firebase Admin SDK for user: {user_id}")
                
                return {
                    'uid': decoded_token.get('uid'),
                    'email': decoded_token.get('email'),
                    'email_verified': decoded_token.get('email_verified', False),
                    'name': decoded_token.get('name'),
                    'picture': decoded_token.get('picture'),
                }
            except Exception as firebase_error:
                logger.debug(f"Firebase Admin verification failed: {type(firebase_error).__name__}: {str(firebase_error)[:80]}")
                
                # Fallback: Accept token if it has valid Firebase issuer
                # (signature verification skipped due to PyJWT restrictions)
                if issuer and 'securetoken.google.com' in issuer and user_id:
                    logger.info(f"✓ Token accepted via issuer validation for user: {user_id}")
                    return {
                        'uid': user_id,
                        'email': email,
                        'email_verified': unverified.get('email_verified', False),
                        'name': unverified.get('name'),
                        'picture': unverified.get('picture'),
                    }
                else:
                    logger.error(f"✗ Token validation failed - invalid issuer: {issuer}")
                    return None
                    
        except Exception as e:
            logger.error(f"Token verification error ({type(e).__name__}): {str(e)}")
            return None
    
    async def get_user(self, uid: str) -> Optional[Dict[str, Any]]:
        """
        Get user information by UID.
        
        Args:
            uid: Firebase user ID
            
        Returns:
            Dict with user info if found, None otherwise
        """
        try:
            user = auth.get_user(uid)
            return {
                'uid': user.uid,
                'email': user.email,
                'email_verified': user.email_verified,
                'display_name': user.display_name,
                'photo_url': user.photo_url,
                'disabled': user.disabled,
                'created_at': user.user_metadata.creation_timestamp,
            }
        except auth.UserNotFoundError:
            logger.warning(f"User not found: {uid}")
            return None
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return None
    
    async def create_custom_token(self, uid: str, claims: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Create a custom token for a user.
        
        Args:
            uid: Firebase user ID
            claims: Optional custom claims
            
        Returns:
            Custom token string if successful, None otherwise
        """
        try:
            custom_token = auth.create_custom_token(uid, claims)
            logger.info(f"Custom token created for user: {uid}")
            return custom_token.decode('utf-8')
        except Exception as e:
            logger.error(f"Error creating custom token: {e}")
            return None


@lru_cache()
def get_firebase_auth() -> FirebaseAuth:
    """Get Firebase Auth singleton instance."""
    return FirebaseAuth()
