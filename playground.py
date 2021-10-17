from acicd.provider import Workflow, Env, Job, RunStep

job_101_steps = [RunStep(name="Run step", run="echo 'Hello world'")]
job_101 = Job(name="Job 101", steps=job_101_steps)

jobs = [job_101, Job(name="Job 102", dependencies=[job_101, job_101])]
w = Workflow(name="Test workflow", env=[Env(name="abc", value="def")], jobs=jobs)

print(w.json())
print(w.yaml("test_output.yml"))
