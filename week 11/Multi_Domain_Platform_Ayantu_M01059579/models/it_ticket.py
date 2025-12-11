class ITTicket:
    def __init__(self, ticket_id: int, title: str, priority: str, status: str, assigned_to):
        self.__id = ticket_id
        self.__title = title
        self.__priority = priority
        self.__status = status
        self.__assigned_to = assigned_to

    def assign_to(self, staff: str) -> None:
        self.__assigned_to = staff

    def close_ticket(self) -> None:
        self.__status = "Closed"

    def get_status(self) -> str:
        return self.__status

    def get_priority(self) -> str:
        return self.__priority

    def get_title(self) -> str:
        return self.__title

    def get_assigned_user(self):
        return self.__assigned_to

    def __str__(self):
        return f"Ticket {self.__id}: {self.__title} [{self.__priority}] {self.__status}"
