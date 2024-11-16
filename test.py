from xagent import XAgent
from xagent.config import XAgentConfig

from langchain.smith import RunEvalConfig, run_on_dataset
from langchain_community.chat_models import ChatOpenAI
from langsmith import Client

# Initialize XAgent with specific config if needed
def agent_factory():
    # Configuring XAgent with required settings
    config = XAgentConfig(
        llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"),
        tools=get_tools(["SerpGoogleSearch"]),
        verbose=True
    )
    return XAgent(config)

# Create the agent
agent = agent_factory()

# Client and evaluation configuration
client = Client()

eval_config = RunEvalConfig(
    evaluators=[
        "qa",
        RunEvalConfig.Criteria("helpfulness"),
        RunEvalConfig.Criteria("conciseness"),
    ],
    input_key="input",
    eval_llm=ChatOpenAI(temperature=0.5, model_name="gpt-3.5-turbo"),
)

# Run evaluation on dataset
chain_results = run_on_dataset(
    client,
    dataset_name="test-dataset",
    llm_or_chain_factory=agent_factory,
    evaluation=eval_config,
    concurrency_level=1,
    verbose=True,
)
