from app.auth.auth_manager import AuthManager

class OneDriveManager:
    def __init__(self):
        self.auth = AuthManager()
        self.token = self.auth.get_token(force_auth=True)
        # Aquí inicializas Graph API client si es necesario
        self.datacampus_root_id = None
