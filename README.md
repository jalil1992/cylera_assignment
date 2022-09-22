# Cylera Backend Assignment

**NOTE**: Do not fork this project. Instead, download it as a ZIP and create a new public repository.

## The Situation

Imagine there’s a store that handles the checkout automatically for shoppers. As shoppers browse, they can pick out what they like from the shelves. When they select something, a store employee brings that item to the checkout registers. There are many registers (to handle busy shopping times), and the employee must figure out which register to bring the item to. Luckily, the store has built a helper for this exact situation - CheckoutBot - that scans the item and tells the employee which register to take it to.

## The problem

When CheckoutBot scans the item, it knows which shopper selected the item. It then has to decide where to send the employee. CheckoutBot’s goal is to evenly distribute the items between all the registers so that we’re taking full advantage of our resources. However, while attempting to spread the workload, it must also ensure that all items from a single shopper go to the same register, so that the shopper can pick up all their items from a single location when they’re ready to checkout.

Additionally, you must handle the scenario where a shopper checks out and their items are removed from the register they used.

## Hints

- We have provided a script that generates events, posts the events to your local API, and prints a representation of the register states. You may run this script when testing your model.
- You are expected to reverse-engineer the API specifications from the event generator script.
- Do not edit the event generator script; we will use our own copy when we evaluate your model.
- Your solution should be horizontally scalable, in that it should be able to handle many simultaneous requests from different employees trying to sort their shoppers’ items.
- You can assume there are 25 registers.
- The Makefile is provided for your convenience and is optional. However, if your API cannot start using the Makefile's provided "make api" target then you must provide instructions for starting it.

## Example output

![image](https://user-images.githubusercontent.com/11721593/180261327-4bfa2a77-0eca-4a28-aa6a-2fd9dc2cdfc6.png)

## Scoring Criteria

- Code quality
- Successful implementation
- Performance
- Distribution of items
