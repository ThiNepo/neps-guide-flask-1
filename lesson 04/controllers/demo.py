from flask import Blueprint

demo_controller = Blueprint("demo_controller", __name__, url_prefix="/demo")


@demo_controller.route("/")
def home():
    return "Hello from the demo controller"


@demo_controller.route("/<demo_id>")
def get_by_id(demo_id):
    return f"Demo {demo_id}"
