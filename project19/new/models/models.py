from odoo import models,fields,api

class Entries(models.Model):
    _name="custom.new"
    _description="user data"

    name=fields.Char()
    role=fields.Char()
    topic=fields.Char()

# class News(models.Model):
#     _name="custom.anothernew"
#     _description="new data"
#
#     topic=fields.Char()
#     description=fields.Text()
#     writer=fields.Char()
#     date=fields.Date()
