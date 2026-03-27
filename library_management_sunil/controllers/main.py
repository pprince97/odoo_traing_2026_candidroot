from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website
from requests import session


# inherit Controller
class WebsiteTopSelling(Website):
    @http.route('/', type='http', auth='public', website=True)
    def index(self, **kw):
        print("========>", request.session.uid)

        res = super(WebsiteTopSelling, self).index(**kw)

        top_products = request.env['product.template'].search([
            ('website_published', '=', True),
        ], limit=4)

        res.qcontext['top_selling_products'] = top_products

        print("========>", top_products)

        return res


class WebsitePages(http.Controller):

    @http.route('/my-page', type='http', auth='public', website=True)
    def my_page(self, **kwargs):
        return request.render('library_management_sunil.my_page_template')

    @http.route('/target-page', type='http', auth='public', website=True)
    def target_page(self, **kwargs):
        return request.render('library_management_sunil.target_page_template')

    # @http.route('/home', auth='public', website=True)
    # def home(self, **kwargs):
    #     user = request.env.user
    #     if user.id == request.website.user_id.id:
    #         return request.render('library_management_sunil.public_homepage')
    #     else:
    #         return request.render('library_management_sunil.loggedin_homepage')

    @http.route('/books', type='http', auth='public', website=True)
    def fetch_books(self, **kwargs):
        books = request.env['book.book'].sudo().search([])
        return request.render('library_management_sunil.website_book_menu_view',
                              {'books': books})

    @http.route('/book/form', type='http', auth='public', methods=['GET'], website=True)
    def book_form(self, **kwargs):
        return request.render('library_management_sunil.book_form_view')

    @http.route(['/book/create'], type='http', auth="public", methods=['POST'], website=True, csrf=True)
    def create_book(self, **post):
        request.env['book.book'].sudo().create({
            'name': post.get('name'),
            'available_copies': post.get('available_copies'),
            'stock': post.get('stock'),
            'borrow_price_per_day': post.get('borrow_price_per_day'),
            'maximum_day_limit': post.get('maximum_day_limit'),
        })

        return request.redirect('/books')

    @http.route('/library/save', type='http', auth='user', website=True)
    def save_library(self, **post):
        request.env['book.book'].sudo().create({
            'name': post.get('name'),
            'user_id': request.env.user.id

        })

        return request.redirect('/my/orders')

    @http.route('/my/orders', type='http', auth='user', website=True)
    def my_orders(self, **kwargs):
        orders = request.env['book.book'].search([('user_id', '=', request.env.user.id)])

        return request.render('library_management_sunil.portal_my_orders_template',
                              {
                                  'orders': orders
                              })

    # @http.route('/', auth='public', website=True)
    # def homepage(self):
    #     website = request.website
    #
    #     if website.name == "Crickets Website":
    #         return request.render('library_management_sunil.crickets_homepage')
    #
    #     elif website.name == "Kabaddis Website":
    #         return request.render('library_management_sunil.kabaddis_homepage')
    #
    #     return request.render('website.default_page')