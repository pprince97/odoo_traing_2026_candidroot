from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website.controllers.main import QueryURL
from odoo.http import request, route


class CustomWebsiteSale(WebsiteSale):

    @route(['/shop'], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', **post):

        ribbons_param = request.params.get('ribbons')

        if ribbons_param:
            selected_ribbons = {
                request.env['ir.http']._unslug(r)[1]
                for r in ribbons_param.split(',')
            }
        else:
            selected_ribbons = set()

        response = super().shop(page=page, category=category, search=search, **post)

        products = response.qcontext.get('search_product')

        response.qcontext['ribbons'] = selected_ribbons
        response.qcontext['ribbon_records'] = products.mapped('website_ribbon_id')

        response.qcontext['keep'] = QueryURL(
            '/shop',
            category=category and int(category),
            search=search,
            tags=post.get('tags'),
            ribbons=ribbons_param,
        )

        return response

    def _get_search_domain(self, search, category, attrib_values):
        domain = super()._get_search_domain(search, category, attrib_values)

        ribbons = request.params.get('ribbons')

        if ribbons:
            ribbon_ids = {
                request.env['ir.http']._unslug(r)[1]
                for r in ribbons.split(',')
            }
            domain.append(('website_ribbon_id', 'in', list(ribbon_ids)))

        return domain