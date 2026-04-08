from odoo import models
import ast

class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    def open_attachment_wizard(self):
        self.ensure_one()

        print("MODEL:", self.model)
        print("RES_IDS RAW:", self.res_ids)
        print("TYPE:", type(self.res_ids))
        print("CONTEXT RES_IDS:", self.env.context.get('default_res_ids'))
        print("TYPE CONTEXT:", type(self.env.context.get('default_res_ids')))

        ctx = self.env.context

        res_ids = (
                self.res_ids or []
        )

        if isinstance(res_ids, str):
            # safety fallback if string sneaks in
            res_ids = ast.literal_eval(res_ids)

        res_id = res_ids[0] if res_ids else None

        print("RES_IDS RAW:", type(res_id))

        model = self.model or ctx.get('default_model')

        return {
            'type': 'ir.actions.act_window',
            'name': 'Attach Files',
            'res_model': 'attachment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'res_model': model,
                'res_id': res_id,
            }
        }