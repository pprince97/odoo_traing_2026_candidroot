from odoo import http, _
from odoo.http import request,route
from odoo.addons.website_sale.controllers.main import WebsiteSale



class ProductController(WebsiteSale):
#
    @route()
    def shop(self,**post):
        response = super(ProductController,self).shop(area='',**post)
        # print('>>>>>>>>>>>>>>>>>>>controller inherit',response.qcontext['min_price'],response.qcontext['max_price'],response.qcontext['available_min_price'])
        # website = request.env['website'].get_current_website()
        # filter_by_area_enabled = website.is_view_active('area_attribute')
        # print(filter_by_area_enabled)
        # application = request.env['product.template'].search([('application_area','!=',False)])
        application = request.env['product.application.area'].search([])
        response.qcontext['application'] = application
        print(response.qcontext,'inhr')
        print('>>>>>>>>>>>>>>>',request.session.get('applications'))
        return response