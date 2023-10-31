import random
import time
from uuid import uuid4

from domain.models import Order, OrderBook
from repository.repository import SimpleOrderRepository


def print_result_message(
    market_round: int,
    added_orders: int,
    matched_list: list[Order],
    partial_list: list[Order],
    unmatched_orders: int,
) -> None:
    """Function prints message with the results of trade in
    the specified round."""
    end_string = '\n' + '-' * 20 + '\n'
    separator = '-' * 20
    print(f'Round {market_round}', end=end_string)
    print('Matched orders:')
    for item in matched_list:
        print(item)
    print(separator)
    print('Partially  matched orders:')
    for item in partial_list:
        print(item)
    print(separator)
    print('Summary:')
    print(f'Orders added: {added_orders}')
    print(f'Orders matched in full: {len(matched_list)}')
    print(f'Orders matched in part: {len(partial_list)}')
    print(f'Orders unmatched: {unmatched_orders}', end=end_string)
    print('To interrupt simulation press Ctrl+C', end=end_string)


def get_random_orders(order_number: int):
    """Function generates the list of random orders."""
    orders = []
    for _ in range(order_number):
        order = Order(
            order_id=uuid4(),
            order_type=random.choice(('sell', 'buy')),
            quantity=random.randint(1, 500),
            price=round(random.uniform(0.1, 100), 2)
        )
        orders.append(order)
    return orders


def market_simulator(order_book: OrderBook):
    """Function simulates market trade. After each round
    functions generates report on completed deals."""
    print('Welcome to market simulator')
    market_round = 0
    while True:
        market_round += 1
        order_list = get_random_orders(random.randint(15, 30))
        for order in order_list:
            order_book.add(order)
        match, partial = order_book.match()
        print_result_message(
            market_round=market_round,
            added_orders=len(order_list),
            matched_list=match,
            partial_list=partial,
            unmatched_orders=len(order_book.orders.orders),
        )
        time.sleep(1)


def main():
    """This is the entrypoint of the app. Function initiates
    repository, Order Book and starts market simulation."""
    test_repository = SimpleOrderRepository()
    order_book = OrderBook(test_repository)
    market_simulator(order_book)


if __name__ == '__main__':
    main()
