from flask_login import UserMixin
class UserLogin(UserMixin):
    def fromDB(self, user_id, db):
        x = db.cursor().execute("SELECT * FROM users WHERE id= ? LIMIT 1",(user_id,)).fetchone()
        if not x:
            return None
        self.user=x
        return self

    def create(self, user):
        self.user = user
        return self

    def get_id(self):
        return str(self.user[0])
