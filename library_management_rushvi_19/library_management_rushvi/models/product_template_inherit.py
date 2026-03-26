from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    custom_tag_ids = fields.Many2many(
        'new.model',
        string="Collections",
        help="Products can belong to multiple collections."
    )
    view_count = fields.Integer(
        string="View Count",
        compute="_compute_view_count",
        store=False
    )

    def _compute_view_count(self):
        track_model = self.env['website.track']
        for product in self:
            product.view_count = track_model.search_count([('product_id', '=', product.id)])


class NewModel(models.Model):
    _name= 'new.model'
    _description = 'new model'

    name = fields.Char(string="Name")