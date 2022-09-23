import json
import logging
from typing import Dict, List

from entities import AddEvent, CheckoutEvent, RegisterType

log = logging.getLogger(__name__)


class Register:
    def __init__(self, count=25):
        self.registers: RegisterType = {}
        self.register_count: int = count
        self.item_customer_map: Dict[int, int] = {}
        self.register_customer: Dict[int, List[int]] = {}
        self.reset()

    def reset(self):
        self.registers.clear()
        for idx in range(self.register_count):
            self.registers[idx] = []
        self.item_customer_map.clear()

    def find_register_to_add(self, e: AddEvent):
        """find a register to process add event"""
        # if there's already a register with this customer's item
        r = self.find_register_with_customer(e.customer)
        if r < 0:
            # find the one with the fewest items
            r, _ = min(self.registers.items(), key=lambda x: len(x[1]))
        return r

    def find_register_with_customer(self, customer_id: int) -> int:
        # self.register_customer.values
        for r, items in self.registers.items():
            if customer_id in [self.item_customer_map[x] for x in items]:
                return r
        return -1  # not found

    def add(self, e: AddEvent):
        r = self.find_register_to_add(e)
        self.registers[r].append(e.item)
        self.item_customer_map[e.item] = e.customer

    def checkout(self, e: CheckoutEvent):
        r = self.find_register_with_customer(e.customer)
        if r >= 0:
            self.registers[r] = []
        else:
            log.warning(f"Customer {e.customer} does not have anything to checkout.")

    def state(self):
        return json.dumps(dict(registers=self.registers))
