import os


def _init_config() -> dict[str, str]:
    # service_dir = os.path.dirname(os.path.dirname(
    #     os.path.dirname(os.path.realpath(__file__))
    # ))
    # path_to_local_venv = os.path.realpath(f"{service_dir}/.env")
    # path_to_local_secrets_venv = os.path.realpath(
    #     f"{service_dir}/.env.secret.postgres"
    # )

    res = {
        # **dotenv_values(path_to_local_venv),
        # **dotenv_values(path_to_local_secrets_venv),
        **os.environ,
    }

    return res


class _EnvVars:
    _config = _init_config()

    def __class_getitem__(cls, env_var: str) -> str:
        return cls._config[env_var]

    @classmethod
    def get_val(cls, env_var: str, default: str | None) -> str | None:
        if env_var in cls._config:
            return cls._config[env_var]
        return default

    @classmethod
    def set_val(cls, env_var: str, val: str) -> None:
        os.environ[env_var] = val
        cls._config[env_var] = val

    @classmethod
    def is_on_host(cls) -> bool:
        return cls._config.get("IS_ON_HOST", False)

    @classmethod
    def print_all(cls) -> None:
        print("Environment variables")
        for key, value in cls._config.items():
            print(f"{key}: {value}")


def get(env_var: str, default: str | None = None) -> str | None:
    return _EnvVars.get_val(env_var, default)


def setdefault(env_var: str, val: str):
    return _EnvVars.set_val(env_var, val)


def is_on_host() -> bool:
    return _EnvVars.is_on_host()
