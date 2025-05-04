from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
import logging

logging.basicConfig(filename="autogen.log", level=logging.INFO)

config_list = [{"model": "llama3", "api_base": "http://localhost:11434", "api_type": "ollama"}]

stock_agent = AssistantAgent(
    name="StockAgent",
    llm_config={"config_list": config_list},
    system_message="Check inventory and respond with stock levels."
)

support_agent = AssistantAgent(
    name="SupportAgent",
    llm_config={"config_list": config_list},
    system_message="Handle customer queries and escalate to stock checks."
)

user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=5,
    code_execution_config={"work_dir": "coding"}
)

group_chat = GroupChat(
    agents=[stock_agent, support_agent, user_proxy],
    messages=[],
    max_round=10
)

manager = GroupChatManager(
    groupchat=group_chat,
    llm_config={"config_list": config_list}
)

def run_autogen_query(query):
    user_proxy.initiate_chat(manager, message=query)
    logging.info(f"AutoGen query: {query}")
    return group_chat.messages[-1]["content"]

