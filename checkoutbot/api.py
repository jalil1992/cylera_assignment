import logging
import sys
from asyncio.log import logger

from flask import Flask, request

from entities import AddEvent, CheckoutEvent, RegisterType
from register import Register

app = Flask(__name__)
log = logging.getLogger(__name__)

register: Register = Register()


@app.route("/health", methods=["GET"])
def health():
    return "OK", 200


@app.route("/state", methods=["DELETE"])
def reset():
    try:
        register.reset()
        return "OK", 202
    except Exception as e:
        log.exception(f"Exception on reset: {str(e)}")
        return str(e), 500


@app.route("/add", methods=["POST"])
def add():
    try:
        data = request.form.to_dict()
        register.add(AddEvent(id=0, customer=data["customer_id"], item=data["item_id"]))  # id is not meaningful here
        return register.state(), 201
    except Exception as e:
        log.exception(f"Exception on add: {str(e)}")
        return str(e), 500


@app.route("/checkout", methods=["POST"])
def checkout():
    try:
        data = request.form.to_dict()
        register.checkout(CheckoutEvent(id=0, customer=data["customer_id"]))  # id is not meaningful here
        return register.state(), 201
    except Exception as e:
        log.exception(f"Exception on checkout: {str(e)}")
        return str(e), 500

if __name__ == "__main__":
    app.run(debug=True)
