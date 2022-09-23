import json
import logging
from typing import Dict, List

from entities import AddEvent, CheckoutEvent, RegisterType

log = logging.getLogger(__name__)


class Register:
    def __init__(self, count=25):
        self.registers: RegisterType = {}
        self.register_count: int = count
        self.register_customer: Dict[int, List[int]] = {} # for each register we will save the customers that are on it <register_id, [customer_id]>
        self.customer_items: Dict[int, List[int]] = {} # for each customer we will save the items <customer_id, [item_id]>
        self.reset()

    def reset(self):
        self.registers.clear()
        self.register_customer.clear()
        self.customer_items.clear()
        for idx in range(self.register_count):
            self.registers[idx] = []
            self.register_customer[idx] = []
        

    def find_register_to_add(self, e: AddEvent):
        """find a register to process add event"""
        # if there's already a register with this customer's item
        r = self.find_register_with_customer(e.customer)
        if r < 0:
            # find the one with the fewest items
            r, _ = min(self.registers.items(), key=lambda x: len(x[1]))
        return r

    def find_register_with_customer(self, customer_id: int) -> int:
        for r, customers in self.register_customer.items():
            if customer_id in customers:
                return r
        
        return -1  # not found

    def add(self, e: AddEvent):
        r = self.find_register_to_add(e)
        self.registers[r].append(e.item)
        self.register_customer[r].append(e.customer)

        self.customer_items.update()
        if e.customer in self.customer_items.keys():
            self.customer_items[e.customer].append(e.item)
        else:
            self.customer_items[e.customer] = e.item

    def checkout(self, e: CheckoutEvent):
        r = self.find_register_with_customer(e.customer)
        if r >= 0:
            self.registers[r].remove(self.customer_items[e.customer])
            self.register_customer[r].remove(e.customer)
        else:
            log.warning(f"Customer {e.customer} does not have anything to checkout.")

    def state(self):
        return json.dumps(dict(registers=self.registers))
