import os
import pytest

from core import Settings

from unittest import mock
from ruamel.yaml import YAML


@pytest.mark.parametrize(
    "email,password,zip_code,languages,save,file_name",
    [("test4@mail.com", "dskalksdl678", "12345", None, "Y", "test_settings1.yaml"),
     ("test6@mail.com", "$6237556^^$", "12345", "English,French", "Y", "test_settings2.yaml"),
     ("cultest8lzie@mail.com", "43223*&6", "12345", None, "N", "no_save_test_settings.yaml")],
    ids=(
        "create settings all languages and save",
        "create settings select languages and save",
        "create settings all languages and don't save"
    )
)
def test_settings(email, password, zip_code, languages, save, file_name):
    with mock.patch("builtins.input", side_effect=[email, zip_code, languages, save]):
        with mock.patch("getpass.getpass", return_value=password):
            settings_path = f"test_tmp/{file_name}"
            settings = Settings(settings_path)
            assert settings.email == email
            assert settings.password == password
            assert settings.zip_code == zip_code
            assert settings.languages == [] if languages is None else languages

            if save.upper() == "Y":
                yaml = YAML()
                with open(settings_path) as f:
                    settings = yaml.load(f)
                    assert settings["udemy"]["email"] == email
                    assert settings["udemy"]["password"] == password
                    assert settings["udemy"]["zipcode"] == zip_code
                    assert settings["udemy"]["languages"] == [] if languages is None else ",".join(languages)
                # Load settings just created
                Settings(settings_path)
            else:
                assert os.path.isdir(settings_path) is False


@pytest.mark.parametrize(
    "email,password,zip_code,languages,save,file_name",
    [("test9@mail.com", "uherwh834", "12345", None, "Y", "test_load_existing_settings1.yaml"),
     ("test10@mail.com", "234sdfs", "None", "English", "Y", "test_load_existing_settings2.yaml"),
     ("test11@mail.com", "frtuhrfty234", "788192", "French,German", "Y", "test_load_existing_settings3.yaml")],
    ids=(
        "load existing settings no languages",
        "load existing settings no zipcode",
        "load existing settings full",
    )
)
def test_load_existing_settings(email, password, zip_code, languages, save, file_name):
    with mock.patch("builtins.input", side_effect=[email, zip_code, languages, save]):
        with mock.patch("getpass.getpass", return_value=password):
            settings_path = f"test_tmp/{file_name}"
            Settings(settings_path)

    # Load existing settings
    settings = Settings(settings_path)
    assert settings.email == email
    assert settings.password == password
    assert settings.zip_code == zip_code
    assert settings.languages == [] if languages is None else languages
