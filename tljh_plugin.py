from tljh.hooks import hookimpl


@hookimpl
def tljh_extra_user_conda_packages():
    """Install jupyter lab extensions"""
    return [
        "black",
        "isort",
        "jupyterlab_code_formatter",
    ]


@hookimpl
def tljh_config_post_install(config):
    # See https://github.com/jupyterhub/the-littlest-jupyterhub/blob/main/tljh/configurer.py
    # Set jupyter lab to be default
    config["user_environment"] = {"default_app": "jupyterlab"}
    # Disable culling idle servers
    config["services"] = {
        "cull": {
            "enabled": False,
        },
    }
