===
Q&A
===

----
Tips
----

* `Blueprints Testing <https://github.com/yunstanford/pytest-sanic/issues/3>`_
* ``test_cli.ws_connect`` does not work in ``sanic.__version__ <= '0.5.4'``, because of a Sanic bug, but it has been fixed in master branch.
* `Importing app has loop already running <https://github.com/yunstanford/pytest-sanic/issues/1>`_ when you have `db_init` listeners.
* `Incorrect coverage report <https://github.com/pytest-dev/pytest-cov/issues/117>`_ with ``pytest-cov``, but we can have workarounds for this issue, it's a pytest loading plugin problem essentially.
* Websockets > 4.0 has broken websockets in ``sanic.__version__ <= '0.6.0'``, but it has been fixed in `master <https://github.com/channelcat/sanic/commit/bca1e084116335fd939c2ee226070f0428cd5de8>`_


Also, feel free to create issue if you have any question.
