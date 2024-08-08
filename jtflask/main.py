import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from jtflask import init_app  # noqa E402

app = init_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=int(os.environ.get("PORT", 8080)))
