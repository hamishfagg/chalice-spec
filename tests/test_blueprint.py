from apispec import APISpec

from chalice_spec import PydanticPlugin
from chalice_spec.chalice import ChaliceWithSpec


def setup_test():
    spec = APISpec(
        title="Test Schema",
        openapi_version="3.0.1",
        version="0.0.0",
        plugins=[PydanticPlugin()],
    )
    app = ChaliceWithSpec(app_name="test", spec=spec)
    return app, spec


def test_blueprint_one():
    from .chalicelib.blueprint_one import blueprint_one

    app, spec = setup_test()
    app.register_blueprint(blueprint_one, url_prefix="/prefix")

    assert spec.to_dict() == {
        "paths": {
            "/prefix/hello-world/deep": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Success",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/TestSchema"
                                    }
                                }
                            },
                        }
                    }
                }
            }
        },
        "info": {"title": "Test Schema", "version": "0.0.0"},
        "openapi": "3.0.1",
        "components": {
            "schemas": {
                "TestSchema": {
                    "title": "TestSchema",
                    "type": "object",
                    "properties": {
                        "hello": {"title": "Hello", "type": "string"},
                        "world": {"title": "World", "type": "integer"},
                    },
                    "required": ["hello", "world"],
                }
            }
        },
    }


def test_blueprint_two():
    from .chalicelib.blueprint_two import blueprint_two

    app, spec = setup_test()
    app.register_blueprint(blueprint_two)

    assert spec.to_dict() == {
        "paths": {
            "/another-world/post": {
                "post": {
                    "responses": {
                        "200": {
                            "description": "Success",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/TestSchema"
                                    }
                                }
                            },
                        }
                    }
                }
            }
        },
        "info": {"title": "Test Schema", "version": "0.0.0"},
        "openapi": "3.0.1",
        "components": {
            "schemas": {
                "TestSchema": {
                    "title": "TestSchema",
                    "type": "object",
                    "properties": {
                        "hello": {"title": "Hello", "type": "string"},
                        "world": {"title": "World", "type": "integer"},
                    },
                    "required": ["hello", "world"],
                }
            }
        },
    }


def test_two_blueprints():
    app, spec = setup_test()

    from .chalicelib.blueprint_one import blueprint_one
    from .chalicelib.blueprint_two import blueprint_two

    app.register_blueprint(blueprint_one, url_prefix="/prefixed")
    app.register_blueprint(blueprint_two)

    assert spec.to_dict() == {
        "paths": {
            "/prefixed/hello-world/deep": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Success",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/TestSchema"
                                    }
                                }
                            },
                        }
                    }
                }
            },
            "/another-world/post": {
                "post": {
                    "responses": {
                        "200": {
                            "description": "Success",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/TestSchema"
                                    }
                                }
                            },
                        }
                    }
                }
            },
        },
        "info": {"title": "Test Schema", "version": "0.0.0"},
        "openapi": "3.0.1",
        "components": {
            "schemas": {
                "TestSchema": {
                    "title": "TestSchema",
                    "type": "object",
                    "properties": {
                        "hello": {"title": "Hello", "type": "string"},
                        "world": {"title": "World", "type": "integer"},
                    },
                    "required": ["hello", "world"],
                }
            }
        },
    }
