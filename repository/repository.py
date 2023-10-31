import abc

from domain.models import Order


class RepAlreadyExistsError(Exception):
    pass


class RepNotFoundError(Exception):
    pass


class AbstractOrderRepository(abc.ABC):
    """Abstract repository class for Orders."""

    def add(self, order: Order) -> None:
        """Method to add order into repository."""
        self._add(order)

    def update(self, order: Order) -> None:
        """Method to update order in repository."""
        self._update(order)

    def get_by_field(
        self,
        field: str,
        value,
        sort_field: str | None = None,
        reverse_sorting: bool = False,
    ) -> list[Order]:
        """Method to get list of orders from repository, basing on
        specified field value."""
        return self._get_by_field(field, value, sort_field, reverse_sorting)

    def remove(self, order: Order) -> None:
        """Method to remove order from repository."""
        self._remove(order)

    def batch_remove(self, orders: list[Order]) -> None:
        """Method to remove order from repository."""
        self._batch_remove(orders)

    def _add(self, order: Order) -> None:
        """Method to add order into repository."""
        raise NotImplementedError

    def _update(self, order: Order) -> None:
        """Method to update order in repository."""
        raise NotImplementedError

    def _get_by_field(
        self,
        field: str,
        value: str,
        sort_field: str,
        reverse_sorting: bool = False,
    ) -> list[Order]:
        """Method to get list of orders from repository, basing on
        specified field value."""
        raise NotImplementedError

    def _remove(self, order: Order) -> None:
        """Method to remove order from repository."""
        raise NotImplementedError

    def _batch_remove(self, orders: list[Order]) -> None:
        """Method to remove order from repository."""
        raise NotImplementedError


class SimpleOrderRepository(AbstractOrderRepository):

    def __init__(self):
        self.orders = set()

    def _add(self, order: Order) -> None:
        """Method to add order into repository."""
        if order in self.orders:
            raise RepAlreadyExistsError('Order is already in repository')
        self.orders.add(order)

    def _update(self, order: Order) -> None:
        """Method to update order in repository."""
        try:
            self.orders.remove(order)
        except Exception:
            raise RepNotFoundError('Order for update is not found')
        self.orders.add(order)

    def _get_by_field(
        self,
        field: str,
        value,
        sort_field: str | None = None,
        reverse_sorting: bool = False,
    ) -> list[Order]:
        """Method to get list of orders from repository, basing on
        specified field value."""
        results = [item for item in self.orders
                   if getattr(item, field) == value]
        if not sort_field:
            return results
        if reverse_sorting:
            results.sort(key=lambda item: -getattr(item, sort_field))
        else:
            results.sort(key=lambda item: getattr(item, sort_field))
        return results

    def _remove(self, order: Order) -> None:
        """Method to remove order from repository."""
        try:
            self.orders.remove(order)
        except KeyError:
            raise RepNotFoundError('Order for removal is not found')

    def _batch_remove(self, orders: list[Order]) -> None:
        """Method to remove list of orders from repository."""
        for order in orders:
            try:
                self.remove(order)
            except RepNotFoundError:
                pass
