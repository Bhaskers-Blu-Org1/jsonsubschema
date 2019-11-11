"""
Created on Oct. 25, 2019
@author: Andrew Habib
"""

import unittest

from jsonsubschema import isSubschema


class TestRefs(unittest.TestCase):

    def test_1(self):
        s1 = {
            "type": "array",
            "items": {"$ref": "#/definitions/positiveInteger"},
            "definitions": {
                "positiveInteger": {
                    "type": "integer",
                    "minimum": 0,
                    "exclusiveMinimum": True
                }
            }
        }
        s2 = {
            "type": "array",
            "items": {"$ref": "#/definitions/positiveInteger"},
            "definitions": {
                "positiveInteger": {
                    "type": "integer",
                    "minimum": -1,
                    "exclusiveMinimum": True
                }
            }
        }
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

        s3 = {"type": "array", "items": {"type": "integer"}}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s3))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s3))

        s4 = {"type": "array", "items": {"type": "string"}}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s4))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s4))

        s4 = {"type": "string"}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s4))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s4))

    @unittest.skip("Unsupported ecursive/circular $ref")
    def test_2(self):
        s1 = {"definitions": {"S": {"anyOf": [{"enum": [None]},
                                              {"allOf": [{"items": [{"$ref": "#/definitions/S"},
                                                                    {"$ref": "#/definitions/S"}],
                                                          "maxItems": 2,
                                                          "minItems": 2,
                                                          "type": "array"},
                                                         {"not": {"type": "array",
                                                                  "uniqueItems": True}}
                                                        ]
                                               }
                                              ]
                                    }
                              },
                "$ref": "#/definitions/S"
              }

        s2 = {"enum": [None]}

        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))