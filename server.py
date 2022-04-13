from flask import Flask
from flask import g
from flask import send_file
from flask import request
from flask import session
from flask import abort
from typing import Dict, Tuple, Union
from os import urandom
from flask_caching import Cache
import os.path
import lmdb
import struct
import hashlib

SECRET_KEY = urandom(12)
SESSION_TYPE = "redis"
app = Flask(__name__)
app.config.from_object(__name__)
cache = Cache(config={"CACHE_TYPE": "SimpleCache"})
cache.init_app(app)

def get_credentials() -> Union[None, Tuple[str, str]]:
    if os.path.exists("auth"):
        with open("auth") as fp:
            return tuple(fp.read().split()[:2])
    else:
        return None


def get_env():
    if getattr(g, "lmdb_env", None) is None:
        g.lmdb_env = lmdb.open("db", max_dbs=2)
    return g.lmdb_env


def get_db(db_name):
    if getattr(g, f"db_{db_name}", None) is None:
        setattr(g, f"db_{db_name}", get_env().open_db(db_name.encode()))

    return getattr(g, f"db_{db_name}")


def get_login_method():
    if os.path.exists("auth"):
        return "auth"
    else:
        return "open"

@app.route("/dot.png")
def dot():
    url: bytes = request.headers.get("referer", "dummy").encode()
    useragent: bytes = request.headers.get("user-agent", "dummy").encode()
    hit_db = get_db("hit")
    useragent_db = get_db("ua")
    with get_env().begin(write=True, db=hit_db) as txn:
        current_hit_packed: bytes = bytes(txn.get(url, default=b"\x00"*8))
        current_hit_unpacked: int = struct.unpack("Q", current_hit_packed)[0]
        current_hit_unpacked += 1
        current_hit_packed = struct.pack("Q", current_hit_unpacked)
        if current_hit_packed == 1:
            txn.put(url, current_hit_packed)
        else:
            txn.replace(url, current_hit_packed)
        
    with get_env().begin(write=True, db=useragent_db) as txn:
        current_hit_packed: bytes = bytes(txn.get(useragent, default=b"\x00"*8))
        current_hit_unpacked: int = struct.unpack("Q", current_hit_packed)[0]
        current_hit_unpacked += 1
        current_hit_packed = struct.pack("Q", current_hit_unpacked)
        if current_hit_unpacked == 1:
            txn.put(useragent, current_hit_packed)
        else:
            txn.replace(useragent, current_hit_packed)

    return send_file("dot.png", mimetype="image/png")


@app.route("/stats")
def stats():
    print(session.get("who"))
    if session.get("who", "noone") == "noone":
        abort(403)
    result: Dict[str, int] = dict()
    with get_env().begin(db=get_db("hit")) as txn:
        for url, hit_packed in txn.cursor():
            result[url] = struct.unpack("Q", hit_packed)[0]
    result["total"] = sum(result.values())
    return result


@app.route("/login")
def login_method():
    return { "method": get_login_method() }


@app.route("/login", methods=("POST", ))
def login():
    if not request.is_json:
        abort(404)
    credentials = get_credentials()
    if credentials is None:
        session["who"] = "admin"
        print(session)
        return { "logged_in": "success"}
    else:
        username = request.json.get("username")
        password = request.json.get("password")
    
        if not username or not password:
            abort(404)
        
        if username != credentials[0]:
            return { "logged_in": "fail" }
        elif credentials[1] != hashlib.sha256(password.encode()).hexdigest():
            return { "logged_in": "fail" }
        else:
            session["who"] = "admin"
            return { "logged_in": "success" }


@app.route("/logout")
def logout():
    session["who"] = "noone"
    return {}

@app.route("/useragent")
@app.route("/useragent/", defaults=dict(text=""))
@app.route("/useragent/<text>")
def useragent(text: str = ""):
    if session.get("who", "noone") == "noone":
        abort(403)
    result = dict(result=0, total=0)
    with get_env().begin(db=get_db("ua")) as txn:
        for useragent, hit_packed in txn.cursor():
            hit_unpacked: int = struct.unpack("Q", hit_packed)[0]
            if text in useragent.decode():
                result["result"] += hit_unpacked
            result["total"] += hit_unpacked

    return result


@app.route("/whoami")
def whoami():
    return { "youre": session.get("who", "noone") }

if __name__ == "__main__":
    app.run(debug=True)
