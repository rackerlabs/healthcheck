import unittest
from app.models import Projects


class ModelsTest(unittest.TestCase):

    def test_to_json(self):
        project = Projects(name="new project", email="test@rackspace.com", description="A test project",
                           dependencies="projectA", id=1)
        json_project = project.to_json()
        expected = {"name": "new project", "email": "test@rackspace.com", "description": "A test project",
                    "dependencies": "projectA", "id": 1}
        self.assertTrue(json_project == expected)

