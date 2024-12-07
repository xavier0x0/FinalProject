from . import orders, order_details, menu_items, reviews,promo_codes


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(menu_items.router)
    app.include_router(reviews.router)
    app.include_router(promo_codes.router)