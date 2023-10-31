from time import time
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class Order(BaseModel):
    """This class describes Order model. Each order with the same uuid is
    treated as the same order."""

    order_id: UUID
    timestamp: float = Field(
        gt=0,
        description='Timestamp should be greater than 0',
        default=time())
    order_type: Literal['sell', 'buy']
    quantity: int = Field(
        gt=0,
        description='Quantity should be greater than 0')
    price: float = Field(
        gt=0,
        description='Price should be greater than 0')

    def __eq__(self, other):
        if not isinstance(other, Order):
            return False
        return other.order_id == self.order_id

    def __hash__(self):
        return hash(self.order_id)

    def __gt__(self, other):
        return self.order_id > other.order_id

    def __str__(self):
        return (f'{self.order_type}_{self.quantity}_'
                f'{self.price}_{self.order_id}')


class OrderBook:
    """Class to work with OrderBook"""

    def __init__(self, order_repository):
        self.orders = order_repository

    def add(self, order: Order):
        """Method adds order to repository."""
        self.orders.add(order)

    def modify(self, order: Order):
        """Method updates order in repository."""
        self.orders.update(order)

    def remove(self, order: Order):
        """Method removes order from repository."""
        self.orders.remove(order)

    def batch_remove(self, orders: list[Order]):
        """Method removes list of orders from repository."""
        self.orders.batch_remove(orders)

    def match(self):
        """Method matches buy-orders and sell-orders,
        removes matched orders from repository and
        returns list of matched orders and list of
        partially matched orders."""
        sell_orders = self.orders.get_by_field(
            field='order_type',
            value='sell',
            sort_field='price',
            reverse_sorting=False)
        buy_orders = self.orders.get_by_field(
            field='order_type',
            value='buy',
            sort_field='price',
            reverse_sorting=True)
        matched_orders = []
        partially_matched_orders = []
        partial_sell = {
            'order': None,
            'quantity_matched': 0,
        }
        partial_buy = {
            'order': None,
            'quantity_matched': 0,
        }

        sell_idx = 0
        buy_idx = 0
        matched_quantity = 0

        while (sell_idx < len(sell_orders)
               and buy_idx < len(buy_orders)):
            if sell_orders[sell_idx].price > buy_orders[buy_idx].price:
                break
            sell_to_match = (sell_orders[sell_idx].quantity
                             - partial_sell['quantity_matched'])
            buy_to_match = (buy_orders[buy_idx].quantity
                            - partial_buy['quantity_matched'])
            matched_quantity = min(sell_to_match, buy_to_match)

            if matched_quantity == sell_to_match:
                partial_sell['order'] = None
                partial_sell['quantity_matched'] = 0
                matched_orders.append(sell_orders[sell_idx])
                sell_idx += 1
            else:
                partial_sell['order'] = sell_orders[sell_idx]
                partial_sell['quantity_matched'] += matched_quantity

            if matched_quantity == buy_to_match:
                partial_buy['order'] = None
                partial_buy['quantity_matched'] = 0
                matched_orders.append(buy_orders[buy_idx])
                buy_idx += 1
            else:
                partial_buy['order'] = buy_orders[buy_idx]
                partial_buy['quantity_matched'] += matched_quantity
        self.orders.batch_remove(matched_orders)
        if partial_sell['order']:
            partially_matched_orders = self._treat_partial(
                partial_sell,
                partially_matched_orders)
        if partial_buy['order']:
            partially_matched_orders = self._treat_partial(
                partial_buy,
                partially_matched_orders)
        return matched_orders, partially_matched_orders

    def _treat_partial(self, partial_dict, result_dict):
        """Method updates partially matched order in repository
        and adds the matched part to thr list of partially matched
        orders."""
        matched_order = Order(
            order_id=partial_dict['order'].order_id,
            timestamp=partial_dict['order'].timestamp,
            order_type=partial_dict['order'].order_type,
            quantity=partial_dict['quantity_matched'],
            price=partial_dict['order'].price,
        )
        result_dict.append(matched_order)
        unmatched_part = Order(
            order_id=partial_dict['order'].order_id,
            timestamp=partial_dict['order'].timestamp,
            order_type=partial_dict['order'].order_type,
            quantity=(partial_dict['order'].quantity
                      - partial_dict['quantity_matched']),
            price=partial_dict['order'].price,
        )
        self.orders.update(unmatched_part)
        return result_dict
