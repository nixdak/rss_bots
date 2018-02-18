import json
import yaml
import unittest

import requests
import jsonschema

class TestFlexgetConfig(unittest.TestCase):
    def setUp(self):
        with open("podcasts.yml", "r") as podcasts:
            self.yaml = yaml.load(podcasts)

        self.task_schema = {
            "type": "object",
            "properties": {
                "rss": {
                    "type": "string",
                    "format": "uri",
                    "pattern": "^(https?)://"
                },
                "set": {
                    "type": "object",
                    "properties": {
                        "podcast_name": { "type": "string" }
                    },
                    "required": [ "podcast_name" ],
                    "additional_properties": False
                },
                "template": { "enum": [ "podcast" ] }
            },
            "required": [ "rss", "set", "template" ],
            "additionalProperties": False
        }

        # Because people block python requests and that makes me sad
        self.headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0" }

    def test_validate_task_schemas(self):
        for task_yaml in self.yaml['tasks'].values():
            jsonschema.validate(task_yaml, self.task_schema)

    def test_validate_task_url(self):
        for task_yaml in self.yaml['tasks'].values():
            url = task_yaml['rss']
            response = requests.get(url, headers=self.headers)
            self.assertEqual(200, response.status_code)

if __name__ == "__main__":
    unittest.main()
