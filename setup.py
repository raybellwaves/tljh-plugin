from setuptools import setup

setup(
    name="tljh-plugin",
    entry_points={"tljh": ["plugin = tljh_plugin"]},
    py_modules=["tljh_plugin"],
)
