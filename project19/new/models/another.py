from odoo import models,fields,api

class News(models.Model):
    _name="custom.anothernew"
    _description="new data"

    topic=fields.Char()
    description=fields.Text()
    writer=fields.Char()
    date=fields.Date()