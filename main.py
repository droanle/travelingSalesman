import os
from flask import Flask
from Src.Router import Router

template_dir = os.path.abspath('./Templates')

app = Flask(__name__,
            template_folder=template_dir,
            static_url_path="/Public",
            static_folder='Public')
app.register_blueprint(Router)

if __name__ == '__main__':
  app.app_context().push()
  app.run(debug=True, host='0.0.0.0', port=5000)

# from Environment import Environment
# from HillClimb import HillClimb

# environment = Environment(6, 10, 351, 150)

# environment.create_environment()

# hillClimb = HillClimb(environment)

# hillClimb.hill_climb()

# hillClimb.print()