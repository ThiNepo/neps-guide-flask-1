import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "Vp62aTffoX7CC@"

    APP_TITLE = "Full Stack Developer: Backend"

    # SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_DATABASE_URI = "postgresql://xhstffmhacuqpt:9ea18bb31f372acbefaffef4739fd68eb3d72fae2e8d8833086ac2946679af8b@ec2-34-254-120-2.eu-west-1.compute.amazonaws.com:5432/dc6ueqgdu5565n"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "anotverysafekey"
    JWT_TOKEN_LOCATION = ["headers"]

    @staticmethod
    def init_app(app):
        pass
