from odoo import models, fields, api

class Hotel_Room(models.Model):
    _name = 'hotel.room'
    _description = 'Hotel Room'

    name = fields.Char(string='Name', required=True)
    room_number = fields.Char(string='Room Number', required=True)
    price_per_night = fields.Float(string='Price per Night', required=True)
    room_type = fields.Selection([('ac room','Ac Room'),
                                  ('none ac room','None Ac Room'),
                                  ], string='Room Type')
    is_available = fields.Boolean(string='Is Available')
    maintenance_date = fields.Date(string='Maintenance Date')
    last_cleaned = fields.Datetime(string='Last Cleaned')
    notes = fields.Text(string='Notes')
    room_document = fields.Binary(string='Room Document')
    room_image = fields.Image(string='Room Image')

    hotel_id = fields.Many2one('hotel.hotel',string='Hotel_ID')
    guest_ids = fields.One2many('hotel.guest','room_id',string='Guest_IDs')

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if val.get('name'):
                self.env['res.partner'].with_context(teacher=True).create({'name': val.get('name')})
        res = super().create(vals_list)
        return res


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model_create_multi
    def create(self, vals_list):
        print('dddddddddddddddddddddddd', self.env.context)
        res = super().create(vals_list)
        return res