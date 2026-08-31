#!/usr/bin/env python3
import argparse
import json
import random
import signal
import sys
import time

from confluent_kafka import Producer

from catalog import build_customer_pool, build_product_catalog
from config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC_CLICKSTREAM, KAFKA_TOPIC_ORDERS
from generators import generate_session

running = True


def _handle_shutdown(signum, frame):
    global running
    running = False


def _delivery_report(err, msg):
    if err is not None:
        print(f"[ERROR] delivery failed for {msg.topic()}: {err}", file=sys.stderr)


def produce(rate_per_sec: float, duration_seconds: int | None) -> int:
    producer = Producer({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})
    customers = build_customer_pool()
    catalog = build_product_catalog()

    signal.signal(signal.SIGINT, _handle_shutdown)
    signal.signal(signal.SIGTERM, _handle_shutdown)

    interval = 1.0 / rate_per_sec if rate_per_sec > 0 else 0
    start = time.monotonic()
    sessions_produced = 0

    print(f"Producing sessions to {KAFKA_BOOTSTRAP_SERVERS} "
          f"(topics: {KAFKA_TOPIC_ORDERS}, {KAFKA_TOPIC_CLICKSTREAM}) ...")

    while running:
        if duration_seconds is not None and (time.monotonic() - start) >= duration_seconds:
            break

        customer = random.choice(customers)
        events, order = generate_session(customer, catalog)

        for event in events:
            producer.produce(
                KAFKA_TOPIC_CLICKSTREAM,
                key=event["customer_id"],
                value=json.dumps(event),
                callback=_delivery_report,
            )

        if order:
            producer.produce(
                KAFKA_TOPIC_ORDERS,
                key=order["customer_id"],
                value=json.dumps(order),
                callback=_delivery_report,
            )

        producer.poll(0)
        sessions_produced += 1
        if sessions_produced % 20 == 0:
            print(f"  ...{sessions_produced} sessions produced")

        if interval:
            time.sleep(interval)

    print(f"Flushing... {sessions_produced} sessions produced total.")
    producer.flush(10)
    return sessions_produced


def main():
    parser = argparse.ArgumentParser(description="Simulate e-commerce sessions onto Kafka.")
    parser.add_argument("--rate", type=float, default=2.0, help="Sessions per second (default: 2.0)")
    parser.add_argument("--duration", type=int, default=None, help="Stop after N seconds (default: run until Ctrl+C)")
    args = parser.parse_args()
    produce(args.rate, args.duration)


if __name__ == "__main__":
    main()
