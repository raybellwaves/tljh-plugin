# See https://github.com/jupyterhub/the-littlest-jupyterhub/blob/main/tljh/hooks.py
import sh
from tljh.hooks import hookimpl
from tljh.user import ensure_group


@hookimpl
def tljh_extra_apt_packages():
    # Install linux applications
    return ["nano", "vim"]


# Doesn't work for unknown reasons
# Use tljh_extra_user_conda_packages instead
# def tljh_extra_hub_pip_packages():
#     """Install jupyter lab extensions"""


@hookimpl
def tljh_extra_user_conda_packages():
    # See also https://github.com/raybellwaves/tljh-requirements/blob/main/requirements.txt

    # Jupyter lab extensions
    # See also https://github.com/raybellwaves/jupyter_lab_extensions/blob/main/requirements.txt
    lab = [
        "black",
        "dask-labextension", # installs dask
        "isort",
        "jupyterlab_code_formatter",
        "jupyterlab_execute_time",
        "jupyter_bokeh",
        "jupyter-dash",
        "jupyterlab-git",
        "jupyterlab-link-share",
        "jupyter-videochat",
    ]

    # Python kernel extensions
    kernel = [
        "nb_conda_kernels", # not on pip
        "ipykernel",
        "ipympl",
        "ipyleaflet",
        "ipytree",
        "ipywidgets",
        "ipyvolume",
    ]

    # Data science core
    core = [
        "geopandas", # installs folium
        "fastparquet",
        "featuretools",
        "joblib",
        "jupytext",
        "lightgbm",
        "movingpandas",
        "mlflow",
        "rubicon-ml",
        "netCDF4",
        "optuna",
        "pooch",
        "py-xgboost",
        "pyarrow",
        "python-snappy",
        "rioxarray",
        "scikit-learn",
        "s3fs",
        "shap",
        "tpot",
        "tqdm",
        "tsfresh",
        "xarray",
    ]
    
    # Data science viz
    viz = [
        "altair",
        "contextily",
        "dtale",
        "geoviews",
        "graphviz",
        "hvplot", # installs holoviews and panel
        "ipyleaflet",
        "lux-api",
        "lux-widget",
        "pandas-profiling",
        "python-graphviz",
        "seaborn",
        "sweetviz",
        "vega",
    ]
    
    # Data science apps
    app = ["cdsdashboards-singleuser", "streamlit", "voila"]

    return lab + kernel + core + viz + app


@hookimpl
def tljh_custom_jupyterhub_config(c):
    # See https://github.com/jupyterhub/the-littlest-jupyterhub/blob/main/tljh/jupyterhub_config.py
    # Setup cdsdashboards
    # See https://cdsdashboards.readthedocs.io/en/stable/chapters/setup/tljh.html#
    c.JupyterHub.allow_named_servers = True
    c.JupyterHub.spawner_class = 'cdsdashboards.hubextension.spawners.variableusercreating.VariableUserCreatingSpawner'

    c.SystemdSpawner.unit_name_template = 'jupyter-{USERNAME}{DASHSERVERNAME}'

    c.CDSDashboardsConfig.builder_class = 'cdsdashboards.builder.processbuilder.ProcessBuilder'

    from cdsdashboards.app import CDS_TEMPLATE_PATHS
    c.JupyterHub.template_paths = CDS_TEMPLATE_PATHS

    from cdsdashboards.hubextension import cds_extra_handlers
    c.JupyterHub.extra_handlers = cds_extra_handlers    

    
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
    
    # See https://github.com/kafonek/tljh-shared-directory/blob/master/tljh_shared_directory.py   
    # Create a shared directory
    sh.mkdir('/srv/scratch', '-p') # mkdir -p /srv/scratch
    ensure_group('jupyterhub-users') # make sure user is created before changing permissions
    sh.chown('root:jupyterhub-users', '/srv/scratch') # sudo chown root:jupyterhub-users /srv/scratch
    sh.chmod('777', '/srv/scratch') # sudo chmod 777 /srv/scratch
    sh.chmod('g+s', '/srv/scratch') # sudo chmod g+s /srv/scratch
    # Link skeleton directory (directory copied to a new user's home on log in)
    sh.ln('-s', '/srv/scratch', '/etc/skel/scratch')
    
    # init conda
    # doesn't work
    # subprocess.call("conda init bash", shell=True)
