from flask_login import UserMixin


class UserLogin(UserMixin):
    def fromDB(self, user_id, db):
        try:
            x = (
                db.cursor()
                .execute("SELECT * FROM users WHERE id= ? LIMIT 1", (user_id,))
                .fetchone()
            )
            if not x:
                return None
            self.user = x
            return self
        except Exception as e:
            print(f"Error retreiving user from DB: {e}")

    def create(self, user):
        self.user = user
        return self

    def get_id(self):
        return str(self.user[0]) if self.user else None
    
    def verifyExt(self,filename):
        ext=filename.rsplit(".",1)[1]
        if ext=='png' or ext=="PNG":
            return True
        return False
