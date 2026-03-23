from odoo import api, fields, models


class RentalOrder(models.Model):
    _name = 'product.order'
    _description = 'Product Order'
    _rec_name = 'product_id'

    product_id = fields.Many2one('product.template',string='Product')
    list_price = fields.Float(related='product_id.list_price',string='List Price', readonly=True)
    serial_number_ids = fields.Many2many('product.serial.number', string='Serial Numbers')
    rental_id = fields.Many2one('rental.order',string='Rental')

    def write(self, vals):
        for product in self:
            old_serial = product.serial_number_ids

        res = super().write(vals)

        if 'serial_number_ids' in vals:

            for product in self:
                new_serial = product.serial_number_ids
                print(new_serial, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                added_serial = new_serial - old_serial
                removed_serial = old_serial - new_serial
                print(added_serial, removed_serial, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                # mark added users unavailable
                for serial in added_serial:
                    serial.available = False

                # mark removed users available
                for serial in removed_serial:
                    serial.available = True
        return res

    # @api.model_create_multi
    # def create(self, vals_list):
    #     res = super().create(vals_list)
    #     r = super().write(vals_list)
    #     return res
        # for vals in vals_list:
        #     print("-------1-------")
        #     if vals['serial_number_ids']:
        #         print("-------2-------")
        #         for product in vals['serial_number_ids']:
        #             print("-------3-------")
        #             print(product)
        #             for p in product:
        #                 p.available = False
        #
