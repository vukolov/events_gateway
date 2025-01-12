class User:
    def __init__(self):
        self.username: str | None = None
        self.email: str | None = None
        self.full_name: str | None = None
        self.active: bool = True
        self.hashed_password: str | None = None
