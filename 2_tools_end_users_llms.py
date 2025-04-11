from dotenv import load_dotenv

from portia import (
    Config,
    Portia,
    PortiaToolRegistry,
    StorageClass,
    LLMProvider,
    open_source_tool_registry,
    execution_context
)
from portia.cli import CLIExecutionHooks

load_dotenv()

# Need Tavily API key
task2 = "Research the price of gold in the last 30 days, and send bob@portialabs.ai a report about it."

# Need OpenWeatherMap API key
task3 = "Fetch the weather in London and email bob@portialabs.ai with the results."


# Instantiate a Portia runner. Load it with the default config and with Portia cloud tools above.
# Use the CLIExecutionHooks to allow the user to handle any clarifications at the CLI.
my_config = Config.from_default(storage_class=StorageClass.CLOUD,
                                llm_provider=LLMProvider.ANTHROPIC)

portia = Portia(
    config=my_config,
    tools=PortiaToolRegistry(my_config) + open_source_tool_registry,
    execution_hooks=CLIExecutionHooks(),
)

with execution_context(end_user_id="its me, mario"):
    plan = portia.plan(task2)
    [print(step) for step in plan.steps]

    plan_run = portia.run_plan(plan)
