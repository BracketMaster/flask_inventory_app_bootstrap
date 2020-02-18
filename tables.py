from flask_table import Table, Col, ButtonCol

#HTML Tables
class GameTable(Table):
    classes = ['table']
    #properties
    title = Col('Title')
    genre = Col('Genre')
    rating = Col('Rating')
    platform = Col('Platform')
    dev = Col('Developer')
    year = Col('Year of Release')
    price = Col('Price')
    delete = ButtonCol('Delete', 'delete', url_kwargs=dict(title='title'), button_attrs={'class' : "btn btn-danger"})
    add_to_cart = ButtonCol('Add to Cart', 'add_to_cart', url_kwargs=dict(title='title'), button_attrs={'class' : "btn btn-success"})

class CartTable(Table):
    classes = ['table']
    #properties
    title = Col('Title')
    genre = Col('Genre')
    rating = Col('Rating')
    platform = Col('Platform')
    dev = Col('Developer')
    year = Col('Year of Release')
    price = Col('Price')
    delete = ButtonCol('Remove From Cart', 'delete_from_cart', url_kwargs=dict(title='title'), button_attrs={'class' : "btn btn-danger"})
