from crewai import Agent, Task, Crew
import redis
import logging

logging.basicConfig(filename="hr.log", level=logging.INFO)
redis_client = redis.Redis(host="localhost", port=6379, db=0)

onboarding_agent = Agent(
    role="Onboarding Agent",
    goal="Process employee onboarding documents",
    backstory="Expert in HR workflows",
    tools=[],
    verbose=True
)

training_agent = Agent(
    role="Training Agent",
    goal="Assign training modules to new employees",
    backstory="Specialist in employee development",
    tools=[],
    verbose=True
)

onboarding_task = Task(
    description="Process onboarding for employee {employee_id}",
    agent=onboarding_agent,
    expected_output="JSON with employee_id, onboarding_status"
)

training_task = Task(
    description="Assign training for employee {employee_id}",
    agent=training_agent,
    expected_output="JSON with employee_id, training_status"
)

hr_crew = Crew(
    agents=[onboarding_agent, training_agent],
    tasks=[onboarding_task, training_task],
    verbose=2
)

def run_hr_crew(employee_id):
    details = query_rag_gpu(f"Onboarding for {employee_id}", model, index, hr_documents)
    role = details.split("Role: ")[1].split(",")[0]
    redis_client.setex(f"employee:{employee_id}", 3600, json.dumps({"role": role, "status": "pending"}))
    result = hr_crew.kickoff(inputs={"employee_id": employee_id})
    redis_client.setex(f"employee:{employee_id}", 3600, json.dumps({"role": role, "status": "onboarded"}))
    send_to_queue({"employee_id": employee_id, "action": "log_onboarding"}, "tasks")
    return result

