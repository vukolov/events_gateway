from application.downstream.metrics.abstract_destination import AbstractDestination


class File(AbstractDestination):
    def get_topic_name(self) -> str:
        return ''
