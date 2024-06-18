from dataclasses import dataclass
from textwrap import dedent
from typing import Protocol


@dataclass()
class Message:
    body: str
    from_number: str


class MessageCommand(Protocol):
    def handle_message(self, message: Message) -> str:
        pass


class EchoCommand(MessageCommand):
    def handle_message(self, message: Message):
        return f"Echo: {message.body.split(' ', 1)[1]}"


class HelpCommand(MessageCommand):
    def handle_message(self, message: Message):
        return dedent("""\
        Send a voice message to transcribe and summarize.
        Available commands:
            help - Show this help message
            echo - Echo the message back to you
        """)


command_mapping = {"help": HelpCommand(), "echo": EchoCommand()}


def command_handling(message: Message):
    command = message.body.split(" ")[0].strip().lower()
    if command in command_mapping:
        return command_mapping[command].handle_message(message)

    else:
        return HelpCommand().handle_message(message)
