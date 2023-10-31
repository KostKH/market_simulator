from time import time
from uuid import UUID

import pytest

from domain.models import Order
from repository.repository import SimpleOrderRepository


@pytest.fixture(scope='function')
def test_repository():
    return SimpleOrderRepository()


@pytest.fixture(scope='function')
def valid_order_data():
    return [
        {
            'order_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
            'timestamp': time(),
            'order_type': 'sell',
            'quantity': 5,
            'price': 30,
        },
        {
            'order_id': UUID('a038f779-2c66-4565-90e8-8507da656fa2'),
            'timestamp': time(),
            'order_type': 'sell',
            'quantity': 3,
            'price': 15,
        },
        {
            'order_id': UUID('a038f779-2c66-4565-90e8-8507da656fa3'),
            'order_type': 'buy',
            'quantity': 1,
            'price': 17,
        },
        {
            'order_id': UUID('a038f779-2c66-4565-90e8-8507da656fa4'),
            'timestamp': 12345,
            'order_type': 'buy',
            'quantity': 6,
            'price': 233.40,
        },
    ]


@pytest.fixture(scope='function')
def invalid_order_data():
    return [
        {
            'order_id': 'ggg',
            'timestamp': time(),
            'order_type': 'sell',
            'quantity': 1,
            'price': 20,
        },
        {
            'order_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
            'timestamp': -5,
            'order_type': 'sell',
            'quantity': 1,
            'price': 20,
        },
        {
            'order_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
            'timestamp': time(),
            'order_type': 'hhh',
            'quantity': 1,
            'price': 20,
        },
        {
            'order_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
            'timestamp': time(),
            'order_type': 'sell',
            'quantity': 0,
            'price': 20,
        },
        {
            'order_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
            'timestamp': time(),
            'order_type': 'sell',
            'quantity': 1,
            'price': 0,
        },
        {
            'timestamp': time(),
            'order_type': 'sell',
            'quantity': 1,
            'price': 20,
        },
        {
            'order_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
            'timestamp': time(),
            'quantity': 1,
            'price': 20,
        },
        {
            'order_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
            'timestamp': time(),
            'order_type': 'sell',
            'price': 20,
        },
        {
            'order_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
            'timestamp': time(),
            'order_type': 'sell',
            'quantity': 1,
        },
    ]


@pytest.fixture(scope='function')
def valid_orders(valid_order_data):
    return [Order(**item) for item in valid_order_data]


@pytest.fixture(scope='function')
def orders_to_match():
    orders = [
        Order(
            order_id=UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
            timestamp=time(),
            order_type='sell',
            quantity=5,
            price=30,
        ),
        Order(
            order_id=UUID('a038f779-2c66-4565-90e8-8507da656fa2'),
            timestamp=time(),
            order_type='sell',
            quantity=3,
            price=15,
        ),
        Order(
            order_id=UUID('a038f779-2c66-4565-90e8-8507da656fa3'),
            order_type='buy',
            quantity=1,
            price=17,
        ),
        Order(
            order_id=UUID('a038f779-2c66-4565-90e8-8507da656fa4'),
            timestamp=12345,
            order_type='buy',
            quantity=6,
            price=233.40,
        ),
    ]
    expected_match = [
        Order(
            order_id=UUID('a038f779-2c66-4565-90e8-8507da656fa4'),
            timestamp=12345,
            order_type='buy',
            quantity=6,
            price=233.40,
        ),
        Order(
            order_id=UUID('a038f779-2c66-4565-90e8-8507da656fa2'),
            timestamp=time(),
            order_type='sell',
            quantity=3,
            price=15,
        ),
    ]
    expected_partial = [
        Order(
            order_id=UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
            timestamp=time(),
            order_type='sell',
            quantity=3,
            price=30,
        ),
    ]
    expected_unmatched = [
        Order(
            order_id=UUID('a038f779-2c66-4565-90e8-8507da656fa3'),
            order_type='buy',
            quantity=1,
            price=17,
        ),
        Order(
            order_id=UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
            timestamp=time(),
            order_type='sell',
            quantity=2,
            price=30,
        ),
    ]
    return {
        'orders': orders,
        'exp_match': expected_match,
        'exp_partial': expected_partial,
        'exp_unmatched': expected_unmatched,
    }
