import os
from flask import Flask
from Src.Router import Router

template_dir = os.path.abspath('./Templates')

app = Flask(__name__,
            template_folder=template_dir,
            static_url_path="/Public",
            static_folder='Public')
app.register_blueprint(Router)

print(template_dir)
if __name__ == '__main__':
  app.app_context().push()
  app.run(debug=True, host='0.0.0.0', port=5001)