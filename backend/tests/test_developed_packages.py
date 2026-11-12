from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = BACKEND_DIR.parent


def test_development_packages_match_production():
    production = (BACKEND_DIR / "work_packages.txt").read_text().splitlines()
    development = (BACKEND_DIR / "work_packages_dev.txt").read_text().splitlines()

    assert development == [f"-e {package}" for package in production]


def test_production_packages_are_repository_relative_projects():
    production = (BACKEND_DIR / "work_packages.txt").read_text().splitlines()

    assert production
    for package in production:
        assert package.startswith("./python/")
        assert (REPOSITORY_ROOT / package / "pyproject.toml").is_file()
