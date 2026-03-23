from odoo import models, fields, api

class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    def _load_menus_blacklist(self):
        res = super()._load_menus_blacklist()
        if self.env.user.has_group('library_management_man.group_library_admin'):
            res.append(self.env.ref('library_management_man.library_librarian_menu_1').id)
        return res