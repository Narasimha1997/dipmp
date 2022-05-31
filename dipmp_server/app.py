from flask import Flask
from .dipmp import resolve_package
from .env import init_env


config = init_env()


app = Flask("__main__")

@app.get("/<sub>/")
# resolve package names
def get(sub: str):
    if sub.startswith("/"):
      sub = sub[1:]
    if sub.endswith("/"):
      sub = sub[:-1]
    return resolve_package(config, sub)

@app.get("/serve/<sub>")
# serve packages with their names
def serve(sub: str):
  pass