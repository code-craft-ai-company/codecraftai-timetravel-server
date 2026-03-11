import secrets
import hashlib
import datetime
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from automojo.timetravelserver.persistence.models import Credential

class CredentialStore:
    def __init__(self, session: Session):
        self._session = session

    def _hash_token(self, token: str) -> str:
        return hashlib.sha256(token.encode('utf-8')).hexdigest()

    def create(self, label: str, expires_in_days: Optional[int] = None) -> Tuple[Credential, str]:
        """Creates a new credential and returns it along with the plain text token."""
        plain_token = secrets.token_urlsafe(32)
        token_hash = self._hash_token(plain_token)

        expires_at = None
        if expires_in_days is not None:
            expires_at = datetime.datetime.utcnow() + datetime.timedelta(days=expires_in_days)

        cred = Credential(token_hash=token_hash, label=label, expires_at=expires_at)
        self._session.add(cred)
        self._session.commit()
        return cred, plain_token

    def validate(self, plain_token: str) -> Optional[Credential]:
        """Validates a plain text token and updates its last_used_at timestamp if valid."""
        token_hash = self._hash_token(plain_token)
        try:
            cred = self._session.query(Credential).filter_by(token_hash=token_hash).one()
        except NoResultFound:
            return None

        if cred.revoked_at is not None:
            return None

        if cred.expires_at is not None and cred.expires_at < datetime.datetime.utcnow():
            return None

        cred.last_used_at = datetime.datetime.utcnow()
        self._session.commit()
        return cred

    def revoke(self, credential_id: str) -> bool:
        """Revokes a credential by ID."""
        import uuid
        try:
            cred_uuid = uuid.UUID(credential_id)
            cred = self._session.query(Credential).filter_by(id=cred_uuid).one()
        except (ValueError, NoResultFound):
            return False

        if cred.revoked_at is None:
            cred.revoked_at = datetime.datetime.utcnow()
            self._session.commit()
            return True
        return False

    def rotate(self, credential_id: str, expires_in_days: Optional[int] = None) -> Optional[Tuple[Credential, str]]:
        """Rotates a credential by revoking the old one and creating a new one with the same label."""
        import uuid
        try:
            cred_uuid = uuid.UUID(credential_id)
            old_cred = self._session.query(Credential).filter_by(id=cred_uuid).one()
        except (ValueError, NoResultFound):
            return None

        label = old_cred.label
        self.revoke(credential_id)
        return self.create(label, expires_in_days)

    def list_credentials(self) -> List[dict]:
        """Lists metadata of all credentials, hiding token hashes."""
        creds = self._session.query(Credential).all()
        return [
            {
                "id": str(cred.id),
                "label": cred.label,
                "created_at": cred.created_at,
                "last_used_at": cred.last_used_at,
                "revoked_at": cred.revoked_at,
                "expires_at": cred.expires_at,
            } for cred in creds
        ]

    def get(self, credential_id: str) -> Optional[Credential]:
        """Gets a credential by ID."""
        import uuid
        try:
            cred_uuid = uuid.UUID(credential_id)
            return self._session.query(Credential).filter_by(id=cred_uuid).one()
        except (ValueError, NoResultFound):
            return None

    def delete(self, credential_id: str) -> bool:
        """Permanently deletes a credential."""
        import uuid
        try:
            cred_uuid = uuid.UUID(credential_id)
            cred = self._session.query(Credential).filter_by(id=cred_uuid).one()
            self._session.delete(cred)
            self._session.commit()
            return True
        except (ValueError, NoResultFound):
            return False
