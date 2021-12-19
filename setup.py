from setuptools import setup

setup(
    name="tljh-plugin",
    version="0.1",    
    entry_points={"tljh": ["plugin = tljh_plugin"]},
    py_modules=["tljh_plugin"],
)
