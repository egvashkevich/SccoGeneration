import os


def _init_config() -> dict[str, str]:
    # service_dir = os.path.dirname(os.path.dirname(
    #     os.path.dirname(os.path.realpath(__file__))
    # ))
    # path_to_local_venv = os.path.realpath(f"{service_dir}/.env")
    # path_to_local_secrets_venv = os.path.realpath(
    #     f"{service_dir}/.env.secret.postgres"
    # )

    return {
        # **dotenv_values(path_to_local_venv),
        # **dotenv_values(path_to_local_secrets_venv),
        **os.environ,
    }


class EnvVars:
    _config = _init_config()

    def __class_getitem__(cls, env_var: str):
        return cls._config[env_var]

    @classmethod
    def set_val(cls, env_var: str, val: str):
        os.environ[env_var] = val
        cls._config[env_var] = val

    @classmethod
    def is_on_host(cls) -> bool:
        return cls._config.get("IS_ON_HOST", False)

    @classmethod
    def print_all(cls):
        print("Environment variables")
        for key, value in cls._config.items():
            print(f"{key}: {value}")
