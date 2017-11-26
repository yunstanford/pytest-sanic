.. pytest-sanic documentation master file, created by
   sphinx-quickstart on Wed Aug 17 13:50:33 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pytest-sanic
============

.. image:: https://travis-ci.org/yunstanford/pytest-sanic.svg?branch=master
    :alt: build status
    :target: https://travis-ci.org/yunstanford/pytest-sanic

.. image:: https://coveralls.io/repos/github/yunstanford/pytest-sanic/badge.svg?branch=master
    :alt: coverage status
    :target: https://coveralls.io/github/yunstanford/pytest-sanic?branch=master


A pytest plugin for `Sanic <http://sanic.readthedocs.io/en/latest/>`_. It helps you to test your code asynchronously.

This plugin provides:

* very easy testing with async coroutines
* common and useful fixtures
* test_client for Sanic application
* test_server for Sanic application


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



Contents:

.. toctree::
   :maxdepth: 2

   installation
   fixtures
   tips
   development
   reference


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
