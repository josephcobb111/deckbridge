from os.path import dirname, isfile, join

import yaml

ROOT = dirname(dirname(__file__))
REQ_DEPENDENCIES = join(ROOT, "requirements.txt")
META_DEPENDENCIES = join(ROOT, "conda_recipe", "meta.yaml")
ENV_DEPENDENCIES = join(ROOT, "environment.yml")


def get_requirement_dependencies():
    """Extract dependencies from requirements.txt.

    Returns
    -------
    set :
        Dependencies specified in requirements.txt
    """
    with open(REQ_DEPENDENCIES, "r") as f:
        file = f.readlines()
    return {req[:-1] for req in file}


def get_meta_dependencies():
    """Extract the run dependencies from meta.yaml.

    Returns
    -------
    set :
        Run dependencies with version specifications included
    """
    with open(META_DEPENDENCIES, "r") as f:
        meta_yaml = f.read()
    start = meta_yaml.index("build:")
    meta_yaml = yaml.safe_load(meta_yaml[start:])
    run_deps = meta_yaml["requirements"]["run"]
    return set(run_deps)


def get_env_dependencies():
    """Extract dependencies from environment.yml.

    Returns
    -------
    set :
        Dependencies specified in environment.yml
    """
    with open(ENV_DEPENDENCIES, "r") as f:
        env_yaml = yaml.safe_load(f)
    return set(env_yaml["dependencies"])


def test_dependencies_are_aligned():
    """Ensure the dependencies in requirements.txt, meta.yaml, and environment.yml are all aligned"""
    assert isfile(REQ_DEPENDENCIES), "requirements.txt does not exist"
    assert isfile(META_DEPENDENCIES), "meta.yaml does not exist"
    assert isfile(ENV_DEPENDENCIES), "environment.yml does not exist"

    req_deps = get_requirement_dependencies()
    meta_deps = get_meta_dependencies()
    env_deps = get_env_dependencies()

    for i in [
        (req_deps, meta_deps, "requirements.txt", "meta.yaml"),
        (req_deps, env_deps, "requirements.txt", "environment.yml"),
        (meta_deps, env_deps, "meta.yaml", "environment.yml"),
    ]:
        a = i[0]
        b = i[1]
        c = i[2]
        d = i[3]

        assert a.issubset(b), f"{a - b} is specified as a dependency in {c} but cannot be found in {d}"
