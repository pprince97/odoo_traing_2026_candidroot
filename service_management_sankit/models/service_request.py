from odoo import api, fields, models

class ServiceRequest(models.Model):
    _name = 'service.request'
    _description = 'Service Request'

    request_number = fields.Char(string="Request Number")
    customer_id = fields.Many2one('res.partner', string='Customer')
    country_id = fields.Many2one('res.country', string='Country')
    state_id = fields.Many2one('res.country.state', string='State', domain="[('country_id', '=', country_id)]")
    city_id = fields.Many2one('res.city', string='City', domain="[('state_id', '=', state_id)]")
    city = fields.Char(string="City")
    # country_id = fields.Many2one(related='customer_id.country_id', string='Country')
    # state_id = fields.Many2one(related='customer_id.state_id', string='State')
    # city_id = fields.Char(related='customer_id.city', string='City')

    company_id = fields.Many2one('company.object', string='Company')
    owner_id = fields.Many2one(related='company_id.owner_id', string='Owner')
    service_category_id = fields.Many2one('service.category', string='Service Category')
    service_id = fields.Many2one('product.template', string='Service')
    service_date = fields.Date(string="Service Date")
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
            ('invoice', 'In Voice'),
        ],
        default='draft',
        string="State",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if not val.get('request_number'):
                val['request_number'] = self.env['ir.sequence'].next_by_code('service.seq')

        res = super().create(vals_list)
        return res

    def in_progress_state(self):
        self.update({'state': 'in_progress'})

    def done_state(self):
        self.update({'state': 'done'})
        self.ensure_one()
        l = []
        l.append((0, 0, {'name': self.service_id.name,'price_unit': self.service_id.list_price}))
        print(l)
        res = self.env['sale.order'].create(
         {'partner_id': self.customer_id.id,
                'order_line': l
                })

    def invoice_state(self):
        self.update({'state': 'invoice'})
        return self.env.ref('sale.action_report_saleorder').report_action([], data={
            'partner_id': self.customer_id.id,
        }, config=False)

    def draft_state(self):
        self.update({'state': 'draft'})



    @api.onchange('state_id')
    def _onchange_state(self):
        self.city_id = []

    @api.onchange('country_id')
    def _onchange_country_id(self):
        self.city_id = []
        self.state_id = []

    def print_service_request_pdf(self):
        self.ensure_one()
        return self.env.ref('sale.action_report_saleorder').report_action([])
        return self.env.ref('account.account_invoices').report_action([])



