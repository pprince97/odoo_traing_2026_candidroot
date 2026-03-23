from odoo import models,fields

class Rent(models.Model):
    _inherit = 'account.move'


    # user_id
    # employee
    borrow_date = fields.Datetime(string="Borrow Date")
    return_date = fields.Datetime(string="Return Date")
    total_rental_days = fields.Integer(string="Total Rental Days")
    price = fields.Float(string="Price")
    # book
    # author
    # library
