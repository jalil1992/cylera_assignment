import argparse
from collections import defaultdict
import json
import math
import random
import statistics
import time
from typing import Generator, List
import requests

from entities import EventType, AddEvent, CheckoutEvent, Customer, Item, RegisterType
from progressbar import ProgressBar


class EventGenerator:
    @staticmethod
    def generate(
        customer_count: int,
        item_count: int,
        event_count: int,
        random_seed: int,
        with_checkout: bool,
    ) -> Generator[EventType, None, None]:
        rnd = random.Random()
        rnd.seed(random_seed)

        customers = [Customer(id=i, weight=rnd.random()) for i in range(customer_count)]
        customer_weights = [c.weight for c in customers]
        items = [Item(id=i) for i in range(item_count)]

        customer_items: defaultdict[int, int] = defaultdict(lambda: 0)
        for i in range(event_count):
            customer = rnd.choices(customers, weights=customer_weights, k=1)[0]
            event_cls = (
                rnd.choices([AddEvent, CheckoutEvent], weights=[15, 1], k=1)[0]
                if with_checkout and customer_items[customer.id] > 0
                else AddEvent
            )
            if event_cls == AddEvent:
                customer_items[customer.id] += 1
                item = rnd.choice(items)
                event = AddEvent(id=i, customer=customer, item=item)
            elif event_cls == CheckoutEvent:
                customer_items[customer.id] = 0
                event = CheckoutEvent(id=i, customer=customer)
            else:
                raise TypeError(f"Unknown event type: {str(event_cls)} (broken generator!)")
            yield event


def evaluate_model(history: List[RegisterType]):
    print("Evaluating model...")
    print(f"{'ITER':>8}", end="")
    for i in range(25):
        col_header = f"R{i}"
        print(f"{col_header:>8}", end="")
    print(f"{'STDEV':>8}", end="")
    print(f"{'VAR':>8}", end="")
    print("")

    variances = []
    for i, registers in enumerate(history):
        print(f"{(i + 1):>8}", end="")
        counts = [len(x) for x in registers.values()]
        total = sum(counts)
        for x in counts:
            relative = x / total
            percentage = round(relative * 100)
            formatted_percentage = f"{percentage}%"
            print(f"{formatted_percentage:>8}", end="")
        stdev = round(statistics.stdev(counts), 4)
        variance = round(statistics.variance(counts), 4)
        variances.append(variance)
        print(f"{stdev:>8}", end="")
        print(f"{variance:>8}", end="")

        print("", end="\r")
        time.sleep(0.1)
    print("\n")

    avg_stdev = math.sqrt(statistics.mean(variances))
    print(f"Avg stdev: {avg_stdev}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--api-url",
        required=False,
        default="http://localhost:5000",
        help="URL of the REST API serving CheckoutBot endpoints.",
    )
    parser.add_argument(
        "--json-path",
        required=False,
        default="out.json",
        help="Path to an output JSON file.",
    )
    parser.add_argument(
        "--customer-count",
        required=False,
        default=150,
        help="Total number of unique customers to generate.",
    )
    parser.add_argument(
        "--item-count",
        required=False,
        default=900,
        help="Total number of unique items to generate.",
    )
    parser.add_argument(
        "--event-count",
        required=False,
        default=100000,
        help="Total number of events to generate and then process.",
    )
    parser.add_argument(
        "--random_seed",
        required=False,
        default=0,
        help="Random seed to use for generating events, customers, and items.",
    )
    parser.add_argument(
        "--with-checkout",
        required=False,
        action="store_true",
        default=False,
        help="Generate checkout events.",
    )
    parser.add_argument(
        "--dry-run",
        required=False,
        action="store_true",
        default=False,
        help="Print events without POSTing them to the API.",
    )
    parser.add_argument(
        "--to-json",
        required=False,
        action="store_true",
        default=False,
        help="Write a JSON file containing all of the events.",
    )
    args = parser.parse_args()

    api_url = str(args.api_url)
    dry_run = bool(args.dry_run)
    to_json = bool(args.to_json)
    json_path = str(args.json_path)
    random_seed = hash(args.random_seed)

    if dry_run:
        print("Starting dry run...")
    else:
        print(f"Testing connection to {api_url}")
        r = requests.get(f"{api_url}/health", timeout=5)
        if r.status_code == 200:
            print("API health check successful!")
        else:
            raise RuntimeError(f"API health check failed! Is the API running at '{api_url}'?")

    print("Generating events...")
    events = list(
        EventGenerator.generate(
            customer_count=int(args.customer_count),
            item_count=int(args.item_count),
            event_count=int(args.event_count),
            random_seed=hash(random_seed),
            with_checkout=bool(args.with_checkout),
        )
    )
    print(f"Generated {len(events)} events!")

    print("Handling generated events...")
    progress_bar = ProgressBar(n=len(events))
    history: List[RegisterType] = []
    if not dry_run:
        print("Clearing the model's internal state...")
        requests.delete(f"{api_url}/state")
    for i, event in enumerate(events):
        progress_bar.display(i)
        if not dry_run:
            r = requests.post(url=f"{api_url}/{event.action}", data=event.serialize())
            if r.status_code != 201:
                print(r, r.request.method, r.request.url, event.serialize())
                break
            register_state: RegisterType = r.json()["registers"]
            history.append(register_state)

    if not dry_run:
        evaluate_model(history=history)

    if to_json:
        print(f"Writing events to {json_path}")
        with open(json_path, "w") as fout:
            fout.write(json.dumps([dict(action=e.action, **e.serialize()) for e in events]))


if __name__ == "__main__":
    main()
