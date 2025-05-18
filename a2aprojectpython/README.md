Projects
Creating and working on Python projects, i.e., with a pyproject.toml.

uv init: Create a new Python project.
uv add: Add a dependency to the project.
uv remove: Remove a dependency from the project.
uv sync: Sync the project's dependencies with the environment.
uv lock: Create a lockfile for the project's dependencies.
uv run: Run a command in the project environment.
uv tree: View the dependency tree for the project.
uv build: Build the project into distribution archives.
uv publish: Publish the project to a package index.


# server has 3 end points
/agent-card - GET endpoint returning agent capabilities
/execute - POST endpoint for running agent tasks
/cancel - POST endpoint for canceling running tasks