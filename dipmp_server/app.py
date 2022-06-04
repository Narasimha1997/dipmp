from flask import Flask, stream_with_context, Response
from dipmp import resolve_package, yield_chunks_from_ipfs
from env import init_env

config = init_env()

app = Flask("__main__")


@app.get("/simple/<address>/<sub>/")
# resolve package names
def get(address: str, sub: str):
    print(address, sub)
    if sub.startswith("/"):
        sub = sub[1:]
    if sub.endswith("/"):
        sub = sub[:-1]
    return resolve_package(config, sub, address)


@app.get("/serve/<hash>/<package>")
# serve packages with their names
def serve(hash: str, package: str):
    

    headers = {
        'Content-Disposition': 'attachment; filename={}'.format(package),
        'Content-Type': "application/octet-stream",
        "X-filename": package
    }

    return Response(stream_with_context(yield_chunks_from_ipfs(config, hash)),
                    headers=headers,
                    mimetype="application/x-wheel+zip"
                )
