from __future__ import annotations
from typing import Optional

from pydantic import BaseModel
import yaml

# Very github centric atm


class Trigger(BaseModel):
    pass


class Env(BaseModel):
    name: str
    value: str


class Step(BaseModel):
    name: str


class RunStep(Step):
    run: str


class UsesStep(Step):
    uses: str


class Job(BaseModel):
    name: str
    steps: Optional[list[Step]] = None
    image: Optional[str] = None
    dependencies: Optional[list[Job]] = None

    def json(self):
        return {
            "runs-on": self.image,
            "steps": [step.json() for step in self.steps] if self.steps else None,
        }


class Workflow(BaseModel):
    name: Optional[str] = None
    on: Optional[list[Trigger]] = None
    env: Optional[list[Env]] = None
    jobs: Optional[list[Job]] = None

    def json(self):
        return {
            "name": self.name,
            "env": {var.name: var.value for var in self.env or []},
            "jobs": {job.name: job.json() for job in self.jobs or []},
        }

    def yaml(self, file_name):
        with open(file_name, "w") as file:
            yaml.dump(self.json(), file)
