from __future__ import annotations
from typing import Optional

import attr
import yaml

# Very github centric atm


def is_not_null(instance, attribute, value):
    return not value is None


@attr.s
class Trigger:
    pass


@attr.s
class Env:
    name: str = attr.ib()
    value: str = attr.ib()


@attr.s
class Step:
    name: str = attr.ib()

    def json(self):
        return {"name": self.name}


@attr.s
class RunStep(Step):
    run: str = attr.ib()

    def json(self):
        step_json = super().json()
        return step_json | {"run": self.run}


@attr.s
class UsesStep(Step):
    uses: str = attr.ib()

    def json(self):
        step_json = super().json()
        return step_json | {"uses": self.uses}


@attr.s
class Job:
    name: str = attr.ib(validator=[is_not_null])
    steps: Optional[list[Step]] = attr.ib(default=None)
    image: Optional[str] = attr.ib(default=None)
    dependencies: Optional[list[Job]] = attr.ib(default=None)

    def json(self):
        output = {}
        if self.image:
            output["runs-on"] = self.image

        if self.steps:
            output["steps"] = [step.json() for step in self.steps]

        if self.dependencies:
            output["needs"] = [dep.name for dep in self.dependencies]

        return output


@attr.s
class Workflow:
    name: Optional[str] = attr.ib()
    on: Optional[list[Trigger]] = attr.ib(default=None)
    env: Optional[list[Env]] = attr.ib(default=None)
    jobs: Optional[list[Job]] = attr.ib(default=None)

    def json(self):
        return {
            "name": self.name,
            "env": {var.name: var.value for var in self.env or []},
            "jobs": {job.name: job.json() for job in self.jobs or [] if job.json()},
        }

    def yaml(self, file_name):
        with open(file_name, "w") as file:
            yaml.dump(self.json(), file)
