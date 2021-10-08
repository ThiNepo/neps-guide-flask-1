from main import app
from factory import db

from models.user import User

from datetime import datetime

with app.app_context():
    # users = User.query.all()
    # print(users)

    user = User(
        username="maria",
        email="maria@neps.academy",
        birthday=datetime.fromisoformat("2000-05-21T00:00:00.000000"),
    )

    db.session.add(user)

    db.session.commit()
