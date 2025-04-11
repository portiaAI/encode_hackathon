from dotenv import load_dotenv

from portia import (
    Config,
    Portia,
    McpToolRegistry,
    DefaultToolRegistry,
    StorageClass,
    LLMProvider
)

load_dotenv()

task = "Read the portialabs.ai website and tell me what they do"

my_config = Config.from_default(storage_class=StorageClass.CLOUD,
                                llm_provider=LLMProvider.ANTHROPIC)

registry = McpToolRegistry.from_stdio_connection(
    server_name="fetch",
    command="uvx",
    args=["mcp-server-fetch"],
) + DefaultToolRegistry(my_config)

portia = Portia(config=my_config,
                tools=registry)

print(portia.run(task).outputs.final_output)
