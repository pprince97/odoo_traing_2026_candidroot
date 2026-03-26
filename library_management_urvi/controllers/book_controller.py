# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.http import request
import base64

class BookController(http.Controller):

    @http.route(['/book','/book/page/<int:page>'], type='http', auth='public', website=True)
    def public_controller(self,page=0):
        if request.env.user._is_public():
            return request.render("library_management_urvi.book_template_public")
        else:
            books = request.env['library.book'].search([])
            pager = request.website.pager(
                url='/book',
                total=len(books),
                page=page,
                step=3,
            )
            offset = pager['offset']
            books = books[offset: offset + 3]
            return request.render('library_management_urvi.template_view_all_books', {'books': books,'pager': pager})



    @http.route(['/book/submit'], type='http', auth="user", website=True, sitemap=False)
    def book_form_submit(self, **post):
        if post.get('image'):
            post['image'] = base64.b64encode(post['image'].read())
        request.env['library.book'].create({
            'name': post.get('name'),
            'barcode': post.get('barcode'),
            'description': post.get('description'),
            'state': post.get('state'),
            'category': post.get('category'),
            'copies': int(post.get('copies') or 0),
            'borrow_price': float(post.get('borrow_price') or 0.0),
            'maximum_day_limit': int(post.get('maximum_day_limit') or 0),
            'image': post['image'] if post.get('image') else False,
        })
        books = request.env['library.book'].search([])
        return request.render("library_management_urvi.template_view_all_books",{'books': books})

    @http.route(['/create/book'], type='http', auth='user', website=True)
    def book_create(self):
        return request.render("library_management_urvi.template_create_book")

    @http.route(['/my/profile'], type='http', auth="user", website=True)
    def edit_partner_profile(self, **post):
        # Get the partner record of the current logged-in user
        partner = request.env.user.partner_id
        values = {
            'partner': partner,
        }
        return request.render("library_management_urvi.partner_edit_template", values)

    @http.route(['/my/profile/update'], type='http', auth="user", website=True)
    def update_partner_profile(self, **post):
        partner = request.env.user.partner_id
        partner.update({'name': post.get('name') or '','email': post.get('email') or '','phone': post.get('phone') or '','gender': post.get('gender') or ''})
        values = {
            'partner': partner,
        }
        return request.redirect("/my/profile")


