from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_test'
app.config['SQLALCHEMY_ECHO'] = False


db.drop_all()

with app.app_context():
    db.create_all()


class UserModelTestCase(TestCase):
    """Tests for model for Pets."""

    def setUp(self):
        """Clean up any existing users."""

        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()




    # def test_greet(self):
    #     pet = Pet(name="TestPet", species="dog", hunger=10)
    #     self.assertEquals(pet.greet(), "I'm TestPet the dog")

    # def test_feed(self):
    #     pet = Pet(name="TestPet", species="dog", hunger=10)
    #     pet.feed(5)
    #     self.assertEquals(pet.hunger, 5)

    #     pet.feed(999)
    #     self.assertEquals(pet.hunger, 0)

    # def test_get_by_species(self):
    #     pet = Pet(name="TestPet", species="dog", hunger=10)
    #     db.session.add(pet)
    #     db.session.commit()

    #     dogs = Pet.get_by_species('dog')
    #     self.assertEquals(dogs, [pet])