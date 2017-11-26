=======
Example
=======

A simple example.

-----------
Quick Start
-----------

You don't have to load ``pytest-sanic`` explicitly. ``pytest`` will do it for you. Just write tests like,

.. code-block:: python

    async def test_sanic_db_find_by_id(app):
        """
        Let's assume that, in db we have,
            {
                "id": "123",
                "name": "Kobe Bryant",
                "team": "Lakers",
            }
        """
        doc = await app.db["players"].find_by_id("123")
        assert doc.name == "Kobe Bryant"
        assert doc.team == "Lakers"
