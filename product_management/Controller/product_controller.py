from odoo import http, _
from odoo.http import request, route
from odoo.addons.website_sale.controllers.main import WebsiteSale,TableCompute
from odoo.fields import Domain
from odoo.osv import expression

class ProductController(WebsiteSale):
    #
    @route()
    def shop(self, **post):
        selected_apps = request.httprequest.args.getlist('applications')
        response = super(ProductController, self).shop(**post)
        if selected_apps:
            app_ids = [int(i) for i in selected_apps if i.isdigit()]
            if app_ids:
                products = response.qcontext.get('products')
                if products:
                    # filtered_products = products.filtered(lambda products: any(id in app_ids for id in products.application_area.ids))
                    filtered_products = []
                    for p in products:  # <--- This 'p' is exactly the same as the lambda 'p'
                        for pid in p.application_area.ids:
                            if pid in app_ids and p not in filtered_products:
                                filtered_products.append(p)
                    print('filtered_products:', filtered_products)
                    print(products.search([('application_area', 'in', app_ids)]))
                    ppg = response.qcontext.get('ppg')
                    ppr = response.qcontext.get('ppr')
                    response.qcontext.update({
                                    'products': filtered_products,
                                    'search_count': len(filtered_products),
                                    'bins': TableCompute().process(filtered_products, ppg, ppr),
                    })

        application = request.env['product.application.area'].search([])
        response.qcontext['application'] = application
        return response
