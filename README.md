# Cylera Backend Assignment

## Requirements

### The Situation

Imagine there’s a store that handles the checkout automatically for shoppers. As shoppers browse, they can pick out what they like from the shelves. When they select something, a store employee brings that item to the checkout registers. There are many registers (to handle busy shopping times), and the employee must figure out which register to bring the item to. Luckily, the store has built a helper for this exact situation - CheckoutBot - that scans the item and tells the employee which register to take it to.

### The problem

When CheckoutBot scans the item, it knows which shopper selected the item. It then has to decide where to send the employee. CheckoutBot’s goal is to evenly distribute the items between all the registers so that we’re taking full advantage of our resources. However, while attempting to spread the workload, it must also ensure that all items from a single shopper go to the same register, so that the shopper can pick up all their items from a single location when they’re ready to checkout.

Additionally, you must handle the scenario where a shopper checks out and their items are removed from the register they used.

### Hints

- We have provided a script that generates events, posts the events to your local API, and prints a representation of the register states. You may run this script when testing your model.
- You are expected to reverse-engineer the API specifications from the event generator script.
- Do not edit the event generator script; we will use our own copy when we evaluate your model.
- Your solution should be horizontally scalable, in that it should be able to handle many simultaneous requests from different employees trying to sort their shoppers’ items.
- You can assume there are 25 registers.
- The Makefile is provided for your convenience and is optional. However, if your API cannot start using the Makefile's provided "make api" target then you must provide instructions for starting it.

### Example output

![image](https://user-images.githubusercontent.com/11721593/180261327-4bfa2a77-0eca-4a28-aa6a-2fd9dc2cdfc6.png)

### Scoring Criteria

- Code quality
- Successful implementation
- Performance
- Distribution of items

## Implementation

### RegisterSet

Simulates a set of registers. By default, consists of 25 registers.

### State

Used two additional dictionaries `register_customers` and `customer_items` to manage the state of RegisterSet at any moment.

### Algorithm

When a new item is arrived, if the customer's item was already assigned to a register we must assign the new item to that register again.
If the customer is new, we have to pick a register and we aim to maximize the efficiency.

**Method 1**
Whenever a new item is received, we can pick a register with the minimum number of items and use that.

**Method 2**
Whenever a new item is received, we can pick a register with the minimum number of items and use that.
If there are more than two registers with the minimum number of items, we choose one with the minimum customers assigned.

Both methods are kind of greedy algorithm and it is impossible to say which one is better for all cases because there is no assumption about the customer's purchase behavior.

I did some tests changing the number of customers with all the other parameters fixed. (25 registers, 1000 items, and 2500 events)

|        | Method 1 | Method 2 |
| ------ | -------- | -------- |
| C=50   | 15.7275  | 15.5281  |
| C=500  | 4.29361  | 3.9274   |
| C=5000 | 0.64521  | 0.6636   |

Method 1 performed better when there are more customers than the number of items.
This is reasonable because it is unlikely that a customer purchases more than one item.

In other cases, method 2 performed better and it is also desirable to keep less number of customers on each register.

I chose the method #2 after all.
