
from odoo import fields, models , api


class GuestDetail(models.Model):
    _name = "guest.count"
    _description = "Guest Count"

    no_of_male = fields.Integer(string="No. of Male")
    no_of_female = fields.Integer(string="No. of Female")
    no_of_guest = fields.Integer(string="No. of Guest")

    # guest_detail_ids = fields.One2many('guest.detail', 'guest_count_id', string="Guest Details" , compute='_compute_guest_detail_ids')
    # guest_count = fields.Integer(string="Count")
    #
    # @api.depends("guest_detail_ids")
    # def _compute_guest_detail_ids(self):
    #     for rec in self:
    #         rec.guest_count = len(rec.guest_detail_ids)



    # def _compute_no_of_guest(self):
    #     for guest in self:
    #         guest.no_of_guest = guest.no_of_male + guest.no_of_female

