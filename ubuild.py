import os
import subprocess
from uranium import task_requires


def main(build):
    build.packages.install(".", develop=True)


@task_requires("main")
def test(build):
    build.packages.install("pytest")
    build.packages.install("pytest-cov")
    build.packages.install("aiohttp")
    build.packages.install("sanic")
    build.packages.install("pytest-asyncio")
    build.packages.install("radon")
    build.executables.run([
        "pytest", "./tests",
        "--cov", "pytest_sanic",
        "--cov-report", "term-missing",
    ] + build.options.args)


def distribute(build):
    """ distribute the uranium package """
    build.packages.install("wheel")
    build.executables.run([
        "python", "setup.py",
        "sdist", "bdist_wheel", "--universal", "upload"
    ])
