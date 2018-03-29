#   annotator_audio 
#   --------------------------------------
#
#   Written and maintained by Rhys Pang <rhyspang@qq.com>
#
#   Copyright 2017 rhys. All Rights Reserved.
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


from __future__ import print_function

from flask_login import LoginManager
import flask
import flask_migrate
import flask_sqlalchemy

app = flask.Flask(__name__)
app.config.from_object('poll.config')
db = flask_sqlalchemy.SQLAlchemy(app)

migrate = flask_migrate.Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

from poll import views, models


