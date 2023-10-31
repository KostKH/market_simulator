import pytest

from domain import models


def test_models_order_is_created_with_valid_data(valid_order_data):
    for input_data in valid_order_data:
        output = models.Order(**input_data)
        output_data = output.model_dump()
        field_names = list(input_data.keys())
        for name in field_names:
            assert output_data[name] == input_data[name], f'{input_data}'


def test_models_order_is_not_created_with_invalid_data(invalid_order_data):
    for input_data in invalid_order_data:
        with pytest.raises(Exception):
            models.Order(**input_data)


def test_models_order_book_adds_order_correctly(valid_orders,
                                                test_repository):
    order_book = models.OrderBook(test_repository)
    for order in valid_orders:
        order_book.add(order)
    assert len(test_repository.orders) == len(valid_orders)
    for order in valid_orders:
        assert order in test_repository.orders


def test_rep_order_order_book_removes_order_correctly(valid_orders,
                                                      test_repository):
    order_book = models.OrderBook(test_repository)
    for order in valid_orders:
        order_book.add(order)
    order_to_remove = valid_orders[-1]
    order_book.remove(order_to_remove)
    assert order_to_remove not in test_repository.orders


def test_rep_order_simple_rep_batch_removes_order_correctly(valid_orders,
                                                            test_repository):
    order_book = models.OrderBook(test_repository)
    for order in valid_orders:
        order_book.add(order)
    orders_to_remove = valid_orders[:1]
    order_book.batch_remove(orders_to_remove)
    for order_to_remove in orders_to_remove:
        assert order_to_remove not in test_repository.orders


def test_rep_order_simple_rep_matches_orders_correctly(orders_to_match,
                                                       test_repository):
    order_book = models.OrderBook(test_repository)
    for order in orders_to_match['orders']:
        order_book.add(order)

    match, partial = order_book.match()

    assert sorted(match) == sorted(orders_to_match['exp_match'])
    match_sum_quantity = sum(order.quantity for order in match)
    exp_sum_quantity = sum(order.quantity for order
                           in orders_to_match['exp_match'])
    assert match_sum_quantity == exp_sum_quantity

    assert sorted(partial) == sorted(orders_to_match['exp_partial'])
    part_sum_quantity = sum(order.quantity for order in partial)
    exp_part_quantity = sum(order.quantity for order
                            in orders_to_match['exp_partial'])
    assert part_sum_quantity == exp_part_quantity

    assert (sorted(test_repository.orders)
            == sorted(orders_to_match['exp_unmatched']))
