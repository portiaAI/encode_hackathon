from dotenv import load_dotenv

from portia import (
    Config,
    Portia,
    PortiaToolRegistry,
    StorageClass,
    example_tool_registry,
    execution_context
)
from portia.cli import CLIExecutionHooks

load_dotenv()

task0 = "Star the github repo for portiaAI/portia-sdk-python"

task1 = """
Check my availability in Google Calendar for tomorrow between 10am and 12pm.
If I have any free times between 10am and 12pm, please schedule a 30-minute meeting with
bob (bob@portialabs.ai) with title 'Encode Hackathon', and description 'hack it'.
If I don't have any free times, please output the next time after 12pm when I am free.
"""

# Instantiate a Portia runner. Load it with the default config and with Portia cloud tools above.
# Use the CLIExecutionHooks to allow the user to handle any clarifications at the CLI.
my_config = Config.from_default(storage_class=StorageClass.CLOUD)
portia = Portia(
    config=my_config,
    tools=PortiaToolRegistry(my_config),
    execution_hooks=CLIExecutionHooks(),
)

with execution_context(end_user_id="emzi"):
    plan_run = portia.run(task0)
    print(plan_run.outputs)
