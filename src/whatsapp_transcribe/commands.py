from dataclasses import dataclass
from textwrap import dedent
from typing import Protocol


@dataclass()
class Message:
    """
    Represents a message sent to the service
    """

    body: str
    from_number: str


class MessageCommand(Protocol):
    """
    Base Class defining the methods to define on all Commands.

    We are using a command pattern and therefore implement one command in one
    Command Protocol instance.

    To create a new command correctly implement the MessageCommand Protocl
    """

    def handle_message(self, message: Message) -> str:
        pass


class EchoCommand(MessageCommand):
    """
    EchoCommand returns the message sent to the service prefixed with "Echo: "

    Assumes that the message is prefixed with "echo" and the message to echo
    is the rest of the message.
    """

    def handle_message(self, message: Message):
        return f"Echo: {message.body.split(' ', 1)[1]}"


class HelpCommand(MessageCommand):
    """
    HelpCommand returns a help message for the user.

    The help message contains information about the available commands.
    """

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
