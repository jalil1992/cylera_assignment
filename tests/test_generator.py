import pytest

from checkoutbot.generator import (
    EventGenerator,
    AddEvent,
    CheckoutEvent,
    Item,
    Customer,
)


event_generator_params = dict(
    customer_count=200,
    item_count=1500,
    event_count=200000,
    random_seed=0,
)


def test_generator_counts():
    events = list(EventGenerator.generate(**event_generator_params, with_checkout=True))
    assert len(events) == 200000
    add_events = [e for e in events if isinstance(e, AddEvent)]
    assert len(set((e.item.id for e in add_events))) <= 1500
    assert len(set((e.customer.id for e in add_events))) <= 200


def test_generator_customers():
    events = EventGenerator.generate(**event_generator_params, with_checkout=True)
    add_events = [e for e in events if isinstance(e, AddEvent)]
    checkout_events = [e for e in events if isinstance(e, CheckoutEvent)]
    customer_ids = set((e.customer.id for e in add_events))
    assert all((e.customer.id in customer_ids for e in checkout_events))


def test_generator_ordering():
    events = EventGenerator.generate(**event_generator_params, with_checkout=True)
    customers_with_items = set()
    for e in events:
        e.display()
        if isinstance(e, AddEvent):
            customers_with_items.add(e.customer.id)
        else:
            assert e.customer.id in customers_with_items
            customers_with_items.remove(e.customer.id)


def test_generator_determinism():
    events_1 = list(
        EventGenerator.generate(**event_generator_params, with_checkout=True)
    )
    events_2 = list(
        EventGenerator.generate(**event_generator_params, with_checkout=True)
    )

    def same_event(e1, e2):
        if e1.id != e2.id:
            return False
        if type(e1) != type(e2):
            return False
        if e1.customer.id != e2.customer.id:
            return False
        if isinstance(e1, AddEvent) and e1.item.id != e2.item.id:
            return False
        return True

    assert all((same_event(e1, e2) for e1, e2 in zip(events_1, events_2)))


def test_generator_without_checkout():
    events = EventGenerator.generate(**event_generator_params, with_checkout=False)
    assert all((isinstance(e, AddEvent) for e in events))


def test_add_event_serialization():
    add_event = AddEvent(id=0, customer=Customer(id=14, weight=1), item=Item(id=238))
    assert add_event.serialize() == {"customer_id": 14, "item_id": 238}


def test_checkout_event_serialization():
    checkout_event = CheckoutEvent(id=0, customer=Customer(id=11, weight=1))
    assert checkout_event.serialize() == {"customer_id": 11}
