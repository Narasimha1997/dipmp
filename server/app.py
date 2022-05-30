from flask import Flask


example = """
<!DOCTYPE html>
<html>
  <body>
    <h1>Links for python_world</h1>
    <a href="http://www.google.com#egg=pycpu-0.0.1" data-requires-python="&gt;=3.6.0">pycpu-0.0.1</a><br/>
    <a href="http://www.google.com#egg=pycpu-0.0.2" data-requires-python="&gt;=3.6.0">pycpu-0.0.2</a><br/>
    <a href="http://www.google.com#egg=pycpu-0.0.3" data-requires-python="&gt;=3.6.0">pycpu-0.0.3</a><br/>
  </body>
</html>
"""

app = Flask("__main__")

@app.get("/<sub>/")
# all the package fetch operations will be fetched from
# the registry
def get(sub: str):
    print(sub)
    return example

app.run('0.0.0.0', port=5000)