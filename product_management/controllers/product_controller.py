from odoo.http import request
from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale

class ProductController(WebsiteSale):

    @http.route()
    def shop(self, **post):
        response = super(ProductController, self).shop(**post)
        functionalities = self.env['product.functionality'].search([])
        response.qcontext['functionalities'] = functionalities
        return response
