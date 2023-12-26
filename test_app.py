import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from main import create_app
from model import setup_for_db
import os

EXECUTIVE_PRODUCER_JWT_TOKEN = os.environ.get('EXECUTIVE_PRODUCER_JWT_TOKEN')
PRODUCER_HEADERS = {
    'Authorization': 'Bearer ' + EXECUTIVE_PRODUCER_JWT_TOKEN
}

CASTING_ASSISTANT_JWT_TOKEN = os.environ.get('CASTING_ASSISTANT_JWT_TOKEN')
ASSISTANT_HEADERS = {
    'Authorization': 'Bearer ' + CASTING_ASSISTANT_JWT_TOKEN
}

CASTING_DIRECTOR_JWT_TOKEN = ''
DIRECTOR_HEADERS = {
    'Authorization': 'Bearer ' + CASTING_DIRECTOR_JWT_TOKEN
}


class FSNDSTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "postgresql://postgres:1234567890@fsnd-db.cud9wfdw2uig.us-east-2.rds.amazonaws.com:5432/fsnd_db_test"
        setup_for_db(self.app, self.database_path)
        
        request_body = {
            "title": "The date you come",
            "release_date": "2012-08-23",
        }
        self.client().post('/movies', json=request_body, headers=PRODUCER_HEADERS)

        request_body = {
            "title": "The love and the world",
            "release_date": "2027-10-20",
        }
        self.client().post('/movies', json=request_body, headers=PRODUCER_HEADERS)

        request_body = {
            "gender": "male",
            "name": "Truong Hoang Viet",
            "age": 20,
            "movie_id": 1
        }
        self.client().post('/actors', json=request_body, headers=PRODUCER_HEADERS)

        request_body = {
            "gender": "male",
            "name": "Truong Hoang Viet",
            "age": 20,
            "movie_id": 1
        }
        self.client().post('/actors', json=request_body, headers=PRODUCER_HEADERS)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Movies end points testing
    """

    def test_create_movie(self):
        request_body = {
            "title": "The date you come",
            "release_date": "2012-08-23",
        }
        res = self.client().post('/movies', json=request_body, headers=PRODUCER_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_failed_create_movie_400(self):
        res = self.client().post('/movies', headers=PRODUCER_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    def test_get_movies(self):
        res = self.client().get('/movies', headers=PRODUCER_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_update_movie(self):
        request_body = {
            "title": "The date you come",
            "release_date": "2012-08-23",
        }
        res = self.client().patch('/movies/1', json=request_body, headers=PRODUCER_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_failed_update_movie_404(self):
        res = self.client().patch('/movies/771', headers=PRODUCER_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_movie(self):
        res = self.client().delete('/movies/2', headers=PRODUCER_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_delete_an_movie_404(self):
        res = self.client().delete('/movies/711', headers=PRODUCER_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    """
    Actors end points testing
    """

    def test_create_actor(self):
        request_body = {
            "gender": "male",
            "name": "Truong Hoang Viet",
            "age": 20,
            "movie_id": 1
        }
        res = self.client().post('/actors', json=request_body, headers=PRODUCER_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_failed_create_actor_400(self):
        res = self.client().post('/actors', headers=PRODUCER_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    def test_get_actors(self):
        res = self.client().get('/actors', headers=PRODUCER_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_update_actor(self):
        request_body = {
            "gender": "male",
            "name": "Truong Hoang Viet",
            "age": 20,
            "movie_id": 1
        }
        res = self.client().patch('/actors/1', json=request_body, headers=PRODUCER_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_failed_update_actor_404(self):
        res = self.client().patch('/actors/771', headers=PRODUCER_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_actor(self):
        res = self.client().delete('/actors/2', headers=PRODUCER_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_delete_an_acto_404(self):
        res = self.client().delete('/actors/711', headers=PRODUCER_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    """
    Actors end points testing
    """

    def test_casting_assistant_create_movie(self):
        request_body = {
            "title": "The love and the world",
            "release_date": "2027-10-20",
        }
        res = self.client().post('/movies', json=request_body, headers=ASSISTANT_HEADERS)
        self.assertEqual(res.status_code, 403)

    def test_casting_assistant_delete_actor(self):
        res = self.client().delete('/actors/1', headers=ASSISTANT_HEADERS)
        self.assertEqual(res.status_code, 403)

    def test_casting_director_create_movie(self):
        request_body = {
            "title": "The love and the world",
            "release_date": "2027-10-20",
        }
        res = self.client().post('/movies', json=request_body, headers=DIRECTOR_HEADERS)
        self.assertEqual(res.status_code, 401)

    def test_casting_director_delete_movie(self):
        res = self.client().delete('/movies/1', headers=DIRECTOR_HEADERS)
        self.assertEqual(res.status_code, 401)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()