from odoo import http
from odoo.http import request

class OwlDataController(http.Controller):
    @http.route('/owl/save_data', type='json', auth='user', methods=['POST'])
    def save_owl_data(self, **post):
        return request.env['owl.data.storage'].create({
            'name': post.get('name'),
            'price': post.get('price'),
            'image': request.get('image'),
        })

    
