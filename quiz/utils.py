from typing import Any, Callable, TypeVar

F = TypeVar('F', bound=Callable)


def admin_attr(short_description: str, admin_order_field: str = None, **extra: Any) -> Callable:
    """
    Helper method to add attributes to admin methods for actions, list_views, and other readonly fields, etc.
    It allows for adding them in a more concise way than manually assigning them.

    Usage:
    ```python
    @admin_attr(_('Export toppings'))
    def export_toppings(modeladmin, request, queryset) -> None:
        export_queryset(queryset)

    class PizzaAdmin(admin.ModelAdmin):
        actions = (export_toppings,)
        list_view = ('name', 'get_all_toppings')

        @admin_attr(_('All toppings'), 'toppings__name', allow_tags=True)
        def get_all_toppings(self, obj: Pizza) -> str:
            return humanize_list(topping.name for topping in obj.toppings.only('name'))
    ```
    """

    def decorator(func: F) -> F:
        attributes = [
            ('short_description', short_description),
            ('admin_order_field', admin_order_field),
            *extra.items(),
        ]
        for attr, value in attributes:
            if value and attr:
                setattr(func, attr, value)
        return func

    return decorator
