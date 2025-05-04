from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
import redis
import logging

logging.basicConfig(filename="support.log", level=logging.INFO)
redis_client = redis.Redis(host="localhost", port=6379, db=0)
config_list = [{"model": "llama3", "api_base": "http://localhost:11434", "api_type": "ollama"}]

ticket_agent = AssistantAgent(
    name="TicketAgent",
    llm_config={"config_list": config_list},
    system_message="Create and track support tickets."
)

escalation_agent = AssistantAgent(
    name="EscalationAgent",
    llm_config={"config_list": config_list},
    system_message="Escalate complex tickets and coordinate with teams."
)

user_proxy = UserProxyAgent(
    name="Customer",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=5,
    code_execution_config={"work_dir": "coding"}
)

group_chat = GroupChat(
    agents=[ticket_agent, escalation_agent, user_proxy],
    messages=[],
    max_round=10
)

manager = GroupChatManager(
    groupchat=group_chat,
    llm_config={"config_list": config_list}
)

def handle_ticket(issue, ticket_id):
    redis_client.setex(f"ticket:{ticket_id}", 3600, json.dumps({"issue": issue, "status": "open"}))
    user_proxy.initiate_chat(manager, message=f"New ticket {ticket_id}: {issue}")
    response = group_chat.messages[-1]["content"]
    status = "resolved" if "resolved" in response.lower() else "escalated"
    redis_client.setex(f"ticket:{ticket_id}", 3600, json.dumps({"issue": issue, "status": status}))
    send_to_kafka({"ticket_id": ticket_id, "action": "notify", "recipient": "support@example.com"})
    return response
