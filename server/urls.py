from server.views import main_view

ROUTES = [
    (r"/", main_view.MainHandler),
]
