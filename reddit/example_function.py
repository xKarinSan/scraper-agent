from dotenv import load_dotenv
from RedditService import RedditService
from openai import OpenAI
import os
import json

load_dotenv()

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_comments_insights",
            "description": "Get the general insights of the subreddit.",
            "parameters": {
                "type": "object",
                "properties": {"subreddit": {"type": "string"}},
                "required": ["subreddit"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }
]

messages = [{"role": "user", "content": "What is trending in this subreddit r/SaaS?"}]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools
)

# Extract tool call data
if completion.choices[0].message.tool_calls:
    tool_call = completion.choices[0].message.tool_calls[0]
    args = json.loads(tool_call.function.arguments)
    print("Extracted Arguments:", args)
    subreddit = args["subreddit"]

    def get_subreddit_posts(subreddit):
        reddit_service = RedditService()
        return reddit_service.get_relevant_posts(subreddits=[subreddit])

    # Fetch subreddit posts
    result = get_subreddit_posts(subreddit)

    # Append assistant tool response to messages correctly
    messages.append({"role": "assistant", "content": None, "tool_calls": [tool_call]})
    messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result)})

    completion_2 = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools
    )

    print("Final Response:", completion_2.choices[0].message.content)
else:
    print("No tool calls detected.")
    exit()