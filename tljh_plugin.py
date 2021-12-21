from tljh.hooks import hookimpl


@hookimpl
def tljh_extra_user_conda_packages():
    """Install jupyter lab extensions"""
    return [
        'black',
        'isort',
        'jupyterlab_code_formatter',
    ]


@hookimpl
def tljh_config_post_install(config):
    # Set jupyter lab to be default
    user_environment = config.get('user_environment', {})
    user_environment['default_app'] = user_environment.get('default_app', 'jupyterlab')
    config['user_environment'] = user_environment
    # Disable culling idle servers
    services_cull = config.get('services.cull', {})
    services_cull['enabled'] = user_environment.get('enabled', 'False')
    config['services.cull'] = services_cull
