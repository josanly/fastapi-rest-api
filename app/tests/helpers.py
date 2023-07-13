import contextlib

from app.settings import get_sqldb_settings, get_secret_dir


@contextlib.contextmanager
def override_sqldb_settings(**overrides):
    settings = get_sqldb_settings()
    original = {}
    try:
        for key, value in overrides.items():
            original[key] = getattr(settings, key)
            setattr(settings, key, value)
        yield
    finally:
        for key, value in original.items():
            setattr(settings, key, value)


@contextlib.contextmanager
def override_get_secret_dir(**overrides):
    settings = get_secret_dir()
    original = {}
    try:
        for key, value in overrides.items():
            original[key] = getattr(settings, key)
            setattr(settings, key, value)
        yield
    finally:
        for key, value in original.items():
            setattr(settings, key, value)
