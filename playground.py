from acicd.provider import Workflow, Env, Job

jobs = [Job(name="Job 101"), Job(name="Job 102")]
w = Workflow(name="Test workflow", env=[Env(name="abc", value="def")], jobs=jobs)
print(w.json())
print(w.yaml("test_output.yml"))
