from dotenv import load_dotenv

from portia._unstable.browser_tool import BrowserTool, BrowserToolForUrl
from portia import (
    Config,
    Portia,
    StorageClass,
    LLMProvider,
    PlanRunState,
    InputClarification,
    MultipleChoiceClarification,
    ActionClarification
)
from portia.cli import CLIExecutionHooks

load_dotenv()

task = "Find my connections called 'Bob' on LinkedIn (https://www.linkedin.com)"

my_config = Config.from_default(storage_class=StorageClass.CLOUD,
                                llm_provider=LLMProvider.ANTHROPIC)

# Also see BrowserToolForUrl("https://www.linkedin.com")
# and BrowserTool(infrastructure_option=InfrastructureOption.LOCAL)

# Needs BrowserBase API Key
portia = Portia(config=my_config,
                tools=[BrowserTool()])

plan_run = portia.run(task)

while plan_run.state == PlanRunState.NEED_CLARIFICATION:
    # If clarifications are needed, resolve them before resuming the workflow
    print("\nPlease resolve the following clarifications to continue")
    for clarification in plan_run.get_outstanding_clarifications():
        # Usual handling of Input and Multiple Choice clarifications
        if isinstance(clarification, (InputClarification, MultipleChoiceClarification)):
            print(f"{clarification.user_guidance}")
            user_input = input(
                "Please enter a value:\n"
                + (
                    str(clarification.options)
                    if isinstance(clarification, MultipleChoiceClarification)
                    else ""
                ),
            )
            plan_run = portia.resolve_clarification(clarification, user_input, plan_run)

        # Handling of Action clarifications
        if isinstance(clarification, ActionClarification):
            print(f"{clarification.user_guidance} -- Please click on the link below to proceed.")
            print(clarification.action_url)
            input("Press Enter to continue...")

    # Once clarifications are resolved, resume the workflow
    plan_run = portia.resume(plan_run)