from entities.downstream.metrics.abstract_destination import AbstractDestination


class MessageProcessor:
    def send_message(self, message: dict, destination: AbstractDestination, topic: str):
        message = self._preprocess_message(message)
        destination.send(message, topic)

    def _preprocess_message(self, message: dict) -> dict:
        return message
