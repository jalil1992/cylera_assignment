# Cylera Backend Assignment

## Requirements
[Check here](https://github.com/Cylera/hiring-backend-engineer)

## Implementation
### Files
```
checkoutbot/api.py
checkoutbot/register.py
checkoutbot/tests/test_api.py
```
### RegisterSet

`checkoutbot/register.py`
Simulates a set of registers. By default, consists of 25 registers.


### State management

Used two additional dictionaries `register_customers` and `customer_items` to manage the state of `RegisterSet` at any moment.

### Algorithm

When a new item is arrived, if the customer's item was already assigned to a register we must assign the new item to that register again.
If the customer is new, we have to pick a register and we aim to maximize the efficiency.

**[Method 1](https://github.com/jalil1992/cylera_assignment/blob/c2cc49b0bc00f0a163dd90c2781aaac3b594cb50/checkoutbot/register.py#L34)**
Whenever a new item is received, we can pick a register with the minimum number of items and use that.

**[Method 2](https://github.com/jalil1992/cylera_assignment/blob/c2cc49b0bc00f0a163dd90c2781aaac3b594cb50/checkoutbot/register.py#L35)**
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
