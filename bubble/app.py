from flask import Flask

from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView
from bubble.extensions import db, apispec, logger, celery, limiter
from bubble.models import Subject, Item, SubjectCategory, Tag
from bubble.request_handler import register_error_handler


def create_app(testing=False, cli=False):
    """Application factory, used to create application
    """
    app = Flask("bubble")
    app.config.from_object("bubble.config")

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app, cli)
    configure_apispec(app)
    register_request_handler(app)
    # register_blueprints(app)
    init_celery(app)
    init_admin(app)

    return app


def configure_extensions(app, cli):
    """configure flask extensions
    """
    if cli is True:
        app.config['MONGODB_SETTINGS'] = {
            'host': 'mongodb://localhost:27017/bubble_tmp'
        }
    else:
        # 建立mongo的数据库连接，mongo的连接只需要connect就行
        app.config['MONGODB_SETTINGS'] = {
            'host': app.config['DATABASE_URI']
        }

    db.init_app(app)
    # jwt.init_app(app)
    limiter.init_app(app)
    logger.init_loggers(app)
    # app.es = Elasticsearch(app.config['ELASTICSEARCH_URL'])


def configure_apispec(app):
    """Configure APISpec for swagger support
    """
    apispec.init_app(app, security=[{"jwt": []}])
    apispec.spec.components.security_scheme(
        "jwt", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    )
    apispec.spec.components.schema(
        "PaginatedResult",
        {
            "properties": {
                "total": {"type": "integer"},
                "pages": {"type": "integer"},
                "next": {"type": "string"},
                "prev": {"type": "string"},
            }
        },
    )


def register_blueprints(app):
    """register all blueprints for application
    """
    # app.register_blueprint(auth.views.blueprint)
    # app.register_blueprint(api.views.blueprint)
    pass


def register_request_handler(app):
    """ 注册请求处理器 """

    # 注册错误请求处理函数
    register_error_handler(app)

    @app.before_request
    def before_request_callback():
        # FIXME: 添加你想要执行的操作
        pass

    @app.after_request
    def after_request_callback(response):
        # FIXME: 添加你想要执行的操作
        return response


def init_celery(app=None):
    app = app or create_app()
    celery.conf.broker_url = app.config["CELERY_BROKER_URL"]
    celery.conf.result_backend = app.config["CELERY_RESULT_BACKEND"]
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def init_admin(app=None):
    app = app or create_app()
    admin = Admin(app, name='bubble', template_mode='bootstrap3')
    admin.add_view(ModelView(SubjectCategory))
    admin.add_view(ModelView(Tag))
    admin.add_view(ModelView(Subject))
    admin.add_view(ModelView(Item))
