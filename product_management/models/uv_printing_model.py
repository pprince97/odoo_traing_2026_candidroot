from odoo import fields,models,api

class UVPrinting(models.Model):
    _name = 'product.uv.printing'
    _description = 'Product UV Printing'
    _rec_names_search = ['start_area','end_area', 'price']

    start_area = fields.Integer(string='Start Area',required=True)
    end_area = fields.Integer(string='End Area',required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.user.company_id.currency_id)
    price = fields.Monetary(string='Price',currency_field='currency_id',required=True)

    @api.model
    def name_search(self, name='', domain=None, operator='ilike', limit=100):
        domain = domain or []
        if domain:
            sols = self.search_fetch(
                domain, ['display_name'], limit=limit,
            )
            return [(sol.id, sol.display_name) for sol in sols]
        return super().name_search(name, domain, operator, limit)

    @api.depends_context('printing')
    def _compute_display_name(self):
        for product in self:
            if product:
                name = f"{product.start_area} - {product.end_area} feet"
                product.display_name = name.strip()