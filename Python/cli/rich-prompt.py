from rich.prompt import Prompt, Confirm

is_correct = False
while not is_correct:
    name = Prompt.ask("Enter your name", default="Martin")
    is_correct = Confirm.ask(f"Is your name '{name}'?")

age = Prompt.ask(
    "What is your age group",
    choices=["<18", "18-25", "25-35", ">35"],
    default="25-35"
)

print(f"You are {name} and your age is {age}.")
