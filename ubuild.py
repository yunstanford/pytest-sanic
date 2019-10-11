import os
import subprocess
from uranium import task_requires


def main(build):
    build.packages.install(".", develop=True)


@task_requires("main")
def test(build):
    build.packages.install("pytest")
    build.packages.install("aiohttp")
    build.packages.install("sanic")
    build.packages.install("radon")
    build.packages.install("coverage")
    build.packages.install("asynctest")
    build.packages.install("websockets", version=">=6.0,<7.0")
    build.executables.run([
        "coverage", "run", "--append",
        "--source=pytest_sanic",
        "./bin/pytest", "./tests",
    ] + build.options.args)
    build.executables.run([
        "coverage", "report", "-m"
    ])


def publish(build):
    """ distribute the uranium package """
    build.packages.install("wheel")
    build.packages.install("twine")
    build.executables.run([
        "python", "setup.py",
        "sdist", "bdist_wheel",
    ])
    build.executables.run([
        "twine", "upload", "dist/*", "--verbose",
    ])
