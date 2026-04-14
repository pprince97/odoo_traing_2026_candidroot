from odoo import models,fields,api,_
from odoo.exceptions import ValidationError
from pygments.lexer import default


class ServiceRequestLines(models.Model):
    _name = 'service.request.lines'
    _description = 'Service Request Lines'

    service_id = fields.Many2one('product.product',string='Service')
    quantity = fields.Float(string='Quantity',default=1)
    amount = fields.Float(string='Amount')
    total_amount = fields.Float(string='Total Amount',compute='_compute_total_amount',store=True)
    request_id = fields.Many2one('service.request',string='Requests')

    @api.onchange('service_id')
    def _onchange_service_id(self):
        for rec  in self:
            rec.amount = rec.service_id.list_price

    @api.depends('quantity','service_id')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = rec.amount * rec.quantity