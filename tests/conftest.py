import pytest
from app import create_app, db
from app.models.category import CategoryModel
from app.models.topic import TopicModel
from app.models.user import UserModel
from app.utils.utils import make_hash
from config import TestingConfig


@pytest.fixture(scope='module')
def app():
    """
    This fixture creates an instance of your Flask application for testing.
    'scope=module' means that this app instance will be reused for all tests in the same module.
    """
    app = create_app(config_class=TestingConfig)
    with app.app_context():
        yield app


@pytest.fixture(scope='module')
def client(app):
    """
    This fixture creates a test client for your application.
    It uses the 'app' fixture defined above, ensuring consistency across tests.
    """
    return app.test_client()


@pytest.fixture(scope='module')
def init_database():
    """
    This fixture sets up the database for testing.
    It initializes the database before the tests run and then tears it down afterwards.
    """
    db.create_all()  # Create database tables
    yield db  # This allows tests to run with the initialized database
    db.drop_all()  # Drop all tables after the tests are done


@pytest.fixture(scope='module')
def test_user(init_database):
    user = UserModel(email="test@example.com", username="test", password=make_hash("password"))
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture(scope="module")
def test_category(init_database):
    category = CategoryModel(title="test category")
    db.session.add(category)
    db.session.commit()
    return category


@pytest.fixture(scope="module")
def test_topic(init_database, test_user):
    topic = TopicModel(
        title="test topic",
        body="body of test topic",
        user_id=test_user.id
    )
    db.session.add(topic)
    db.session.commit()
    return topic
