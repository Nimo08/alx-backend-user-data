#!/usr/bin/env python3
"""SessionDBAuth"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Inherits from SessionExpAuth"""
    def create_session(self, user_id=None):
        """
        Creates and stores new instance of UserSession and
        returns the Session ID
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        data = {
            "user_id": user_id,
            "session_id": session_id
        }
        user = UserSession(**data)
        user.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns the User ID by requesting UserSession in the database
        based on session_id
        """
        user_session = UserSession.search({"session_id": session_id})
        if user_session:
            return user_session
        return None

    def destroy_session(self, request=None):
        """
        Destroys the UserSession based on the Session ID
        from the request cookie
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_sessions = UserSession.search({"session_id": session_id})
        if not user_sessions:
            return False
        for session in user_sessions:
            session.delete()
        return True
