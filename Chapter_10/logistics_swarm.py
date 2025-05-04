from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
import redis
import logging

logging.basicConfig(filename="logistics.log", level=logging.INFO)
redis_client = redis.Redis(host="localhost", port=6379, db=0)
config_list = [{"model": "llama3", "api_base": "http://localhost:11434", "api_type": "ollama"}]

routing_agent = AssistantAgent(
    name="RoutingAgent",
    llm_config={"config_list": config_list},
    system_message="Optimize delivery routes based on distance and time."
)

tracking_agent = AssistantAgent(
    name="TrackingAgent",
    llm_config={"config_list": config_list},
    system_message="Track shipments and update statuses."
)

user_proxy = UserProxyAgent(
    name="Logistics",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=5,
    code_execution_config={"work_dir": "coding"}
)

group_chat = GroupChat(
    agents=[routing_agent, tracking_agent, user_proxy],
    messages=[],
    max_round=10
)

manager = GroupChatManager(
    groupchat=group_chat,
    llm_config={"config_list": config_list}
)

def optimize_delivery(order_id, destination):
    redis_client.setex(f"delivery:{order_id}", 3600, json.dumps({"destination": destination, "status": "pending"}))
    user_proxy.initiate_chat(manager, message=f"Optimize route for order {order_id} to {destination}")
    response = group_chat.messages[-1]["content"]
    route = response.split("Route: ")[1].split(",")[0]
    redis_client.setex(f"delivery:{order_id}", 3600, json.dumps({"destination": destination, "route": route, "status": "scheduled"}))
    send_to_kafka({"order_id": order_id, "action": "notify_delivery", "recipient": "logistics@example.com"})
    return response

