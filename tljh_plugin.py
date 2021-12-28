import subprocess
from tljh.hooks import hookimpl


@hookimpl
def tljh_extra_apt_packages():
    """Install linux applications"""
    return ["nano", "vim"]


# Doesn't work for unknown reasons
# Use tljh_extra_user_conda_packages instead
# def tljh_extra_hub_pip_packages():
#     """Install jupyter lab extensions"""


@hookimpl
def tljh_extra_user_conda_packages():
    # Lab extensions
    lab_extensions = [
        "black",
        "dask-labextension",
        "isort",
        "jupyterlab_code_formatter",
        "jupyterlab_execute_time",
        "jupyter_bokeh",
        "jupyter-dash",
        "jupyterlab-git",
        "jupyterlab-link-share",
        "jupyter-videochat",
        
    ]
    
    # Other packages required on root
    other = [
        #"cdsdashboards",        
        "nb_conda_kernels",
        "ipykernel",
        "ipympl",
        "ipyleaflet",
        "ipytree",
        "ipywidgets",
        #"jhsingle-native-proxy",
        #"jupyterhub-traefik-proxy",
        "jupytext",
        #"streamlit",
    ]
    
    # Data science
    ds = ["xarray"]
    
    return lab_extensions + other + ds


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
    
    # init conda
    # doesn't work
    # subprocess.call("conda init bash", shell=True)
