import json
import logging
from typing import Dict, List

from entities import AddEvent, CheckoutEvent, RegisterType

log = logging.getLogger(__name__)


class RegisterSet:
    def __init__(self, count=25):
        self.registers: RegisterType = {}
        self.register_count: int = count

        self.register_customers: Dict[int, List[int]] = {}  # for each register we will save the customers that are on it <register_id, [customer_id]>
        self.customer_items: Dict[int, List[int]] = {}  # for each customer we will save the items <customer_id, [item_id]>
        self.reset()

    def reset(self):
        """clear all state"""
        self.registers.clear()
        self.register_customers.clear()
        self.customer_items.clear()
        for idx in range(self.register_count):
            self.registers[idx] = []
            self.register_customers[idx] = []

    def find_register_to_add(self, e: AddEvent):
        """find a register to process add event"""
        # if there's already a register with this customer's item
        r = self.find_register_with_customer(e.customer)
        if r < 0:
            # find the one with the min # of items
            # r, _ = min(self.registers.items(), key=lambda x: len(x[1]))  # <- METHOD 1: just find a register with minimum # of items
            r, _ = min(self.registers.items(), key=lambda x: (len(x[1]), len(self.register_customers[x[0]])))  # <- METHOD 2: take into account the # of customers as well

        return r

    def find_register_with_customer(self, customer_id: int) -> int:
        """find a register that has an item of a customer if any"""
        for r, customers in self.register_customers.items():
            if customer_id in customers:
                return r  # if found, we need to put the new item on it as well

        return -1  # not found

    def add(self, e: AddEvent):
        """add new item"""
        r = self.find_register_to_add(e)
        self.registers[r].append(e.item)
        self.register_customers[r].append(e.customer)
        self.customer_items[e.customer] = [*self.customer_items.get(e.customer, []), e.item]

    def checkout(self, e: CheckoutEvent):
        r = self.find_register_with_customer(e.customer)
        if r >= 0:
            self.registers[r] = [x for x in self.registers[r] if x not in self.customer_items[e.customer]]
            self.register_customers[r].remove(e.customer)
            self.customer_items[e.customer] = []
        else:
            log.warning(f"Customer {e.customer} does not have anything to checkout.")

    def state(self):
        return json.dumps(dict(registers=self.registers))
