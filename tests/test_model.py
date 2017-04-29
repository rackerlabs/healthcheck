import unittest
from healthcheck.data.models import Projects, Canary


class ModelsTest(unittest.TestCase):
    def test_project_to_json(self):
        project = Projects(name="new project",
                           email="test@rackspace.com",
                           description="A test project",
                           dependencies="projectA", id=1)
        json_project = project.project_to_json()
        expected = {"name": "new project",
                    "email": "test@rackspace.com",
                    "description": "A test project",
                    "dependencies": "projectA", "id": 1}
        self.assertTrue(json_project == expected)


    def test_update_health(self):
        canary = Canary(name="test",
                        description="A test Canary",
                        meta_data={},
                        criteria={},
                        # id=1,
                        project_id=1
                        )
        update = canary.updated_at
        new_health = "RED"
        canary.update_health(new_health=new_health)
        self.assertEquals(canary.health, "RED")
        self.assertNotEqual(update, canary.updated_at)
        self.assert_("RED" in canary.history.itervalues())


# check if ir will work w/out id
# check