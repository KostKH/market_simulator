from repository.repository import SimpleOrderRepository


def test_rep_order_simple_rep_adds_order_correctly(valid_orders):
    repository = SimpleOrderRepository()
    for order in valid_orders:
        repository.add(order)
    assert len(repository.orders) == len(valid_orders)
    for order in valid_orders:
        assert order in repository.orders


def test_rep_order_simple_rep_udates_order_correctly(valid_orders):
    repository = SimpleOrderRepository()
    for order in valid_orders:
        repository.add(order)
    order_to_change = valid_orders[0]
    new_quantity = order_to_change.quantity * 20
    order_to_change.quantity = new_quantity
    repository.update(order_to_change)
    changed_order = repository.get_by_field(
        'order_id',
        order_to_change.order_id,
    )[0]
    assert changed_order.quantity == order_to_change.quantity


def test_rep_order_simple_rep_removes_order_correctly(valid_orders):
    repository = SimpleOrderRepository()
    for order in valid_orders:
        repository.add(order)
    order_to_remove = valid_orders[-1]
    repository.remove(order_to_remove)
    assert order_to_remove not in repository.orders


def test_rep_order_simple_rep_batch_removes_order_correctly(valid_orders):
    repository = SimpleOrderRepository()
    for order in valid_orders:
        repository.add(order)
    orders_to_remove = valid_orders[:1]
    repository.batch_remove(orders_to_remove)
    for order_to_remove in orders_to_remove:
        assert order_to_remove not in repository.orders


def test_rep_order_simple_rep_gets_orders_correctly(valid_orders):
    repository = SimpleOrderRepository()
    for order in valid_orders:
        repository.add(order)
    buy_orders_desc = sorted(
        [item for item in valid_orders if item.order_type == 'buy'],
        key=lambda item: -item.price
    )
    sell_orders_asc = sorted(
        [item for item in valid_orders if item.order_type == 'sell'],
        key=lambda item: item.price
    )
    retrieved_buy_orders = repository.get_by_field(
        field='order_type',
        value='buy',
        sort_field='price',
        reverse_sorting=True,
    )
    retrieved_sell_orders = repository.get_by_field(
        field='order_type',
        value='sell',
        sort_field='price',
        reverse_sorting=False,
    )
    assert retrieved_buy_orders == buy_orders_desc
    for idx in range(len(buy_orders_desc)):
        assert (retrieved_buy_orders[idx].quantity
                == buy_orders_desc[idx].quantity)
        assert (retrieved_buy_orders[idx].price
                == buy_orders_desc[idx].price)
    assert retrieved_sell_orders == sell_orders_asc
    for idx in range(len(sell_orders_asc)):
        assert (retrieved_sell_orders[idx].quantity
                == sell_orders_asc[idx].quantity)
        assert (retrieved_sell_orders[idx].price
                == sell_orders_asc[idx].price)
