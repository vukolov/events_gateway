class User:
    def __init__(self,
                 id: int | None = None,
                 username: str | None = None,
                 email: str | None = None,
                 full_name: str | None = None,
                 active: bool = True,
                 hashed_password: str | None = None,
                 plan_id: int | None = None):
        self.id: int | None = id
        self.username: str | None = None
        self.email: str | None = None
        self.full_name: str | None = None
        self.active: bool = True
        self.hashed_password: str | None = None
        self.plan_id: int | None = None
