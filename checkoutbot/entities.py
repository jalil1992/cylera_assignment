from typing import Union, Dict, List
import dataclasses


@dataclasses.dataclass(frozen=True)
class Customer:
    id: int
    weight: float

    @property
    def alias(self):
        return f"customer-{self.id}"


@dataclasses.dataclass(frozen=True)
class Item:
    id: int

    @property
    def alias(self):
        return f"item-{self.id}"


@dataclasses.dataclass(frozen=True)
class AddEvent:
    id: int
    customer: Customer
    item: Item

    action = "add"

    def serialize(self):
        return dict(customer_id=self.customer.id, item_id=self.item.id)

    def display(self):
        print(f"{self.id}: {self.customer.alias} added {self.item.alias}")


@dataclasses.dataclass(frozen=True)
class CheckoutEvent:
    id: int
    customer: Customer

    action = "checkout"

    def serialize(self):
        return dict(customer_id=self.customer.id)

    def display(self):
        print(f"{self.id}: {self.customer.alias} checked out")


EventType = Union[AddEvent, CheckoutEvent]


# Maps each register to a list of items, where each item is represented by its customer ID
RegisterType = Dict[int, List[int]]
