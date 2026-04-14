import time

import datetime
from odoo import api, fields, models


class Task(models.Model):
    _name = 'project.tasks'
    _description = 'Task'

    name = fields.Char(string="Task Name", required=True)
    task_manager_id = fields.Many2one('res.users', string='Manager', readonly=True)
    assignees_ids = fields.Many2many(related='project_id.project_assignees_ids')
    task_assignees_ids = fields.Many2many('res.users', 'task_assignees_user_rel', 'task_user_id', 'task_assignees_id', string='Assignees',
                                          domain="[('id', 'in', assignees_ids),('available', '=', True)]")

    project_id = fields.Many2one('project.projects', string='Project')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Datetime(string='End Date')
    end_date_only = fields.Date(string="End Date Only")


    timesheet_ids = fields.One2many('project.timesheet', 'tasks_id', string='Timesheets')
    total_hours = fields.Float(string='Total Hours')
    total_amount = fields.Float(string='Total Amount')



    stage_id = fields.Many2one('dynamic.stages', string="Stage", group_expand='_read_group_stage_ids')
    # stage_id = fields.Many2one('maintenance.stage', string='Stage', ondelete='restrict', tracking=True,
    #                            group_expand='_read_group_stage_ids', default=_default_stage, copy=False)

    # dynamic_stages = fields.Integer(string="dynamic_stages", compute='_compute_team_count')

    # def _read_group_stage_ids(self):
    #     dynamic_stages = self.env['dynamic.stages'].search([])
    #     return dynamic_stages.id

    @api.model
    def _read_group_stage_ids(self, stages, domain):
        stage_ids = stages.sudo()._search([])
        return stages.browse(stage_ids)

    # @api.model
    # def _read_group_stage_ids(self, stages, domain, order):
    #     stage_ids = stages._search([], order=order,
    #                                access_rights_uid=SUPERUSER_ID)
    #     return stages.browse(stage_ids)

    @api.onchange('project_id')
    def _onchange_project_id(self):
        self.task_manager_id = self.project_id.project_manager_id


    def generate_task_bill(self):
        return {
            'name': "Generate Bill",
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'views': [(self.env.ref('account.view_move_form').id, "form")],
            'context': {
                'default_move_type': 'in_invoice',
                'default_partner_id': self.project_id.customer_id,

            }

        }

    # # @api.depends('timesheet_ids')
    @api.onchange('timesheet_ids')
    def _onchange_timesheet_hours(self):
        self.total_hours = 0.0
        self.total_amount = 0.0
        for task in self.timesheet_ids:
            self.total_hours += task.spend_hours
            self.total_amount += task.price
        print(self.total_hours,"------------")
    # def _onchange_timesheet_amount(self):
    #     self.total_amount = 0.0
    #     for task in self.timesheet_ids:
    #         self.total_amount += task.price
    #     print(self.total_amount, "------------")

    # @api.depends('company_id')
    # def _compute_timesheet(self):
    #     for task in self.timesheet_ids:
    #         self.total_hours += task.spend_hours
    #     print(self.total_hours, "------------")
    #
    # def _inverse_timesheet(self):
    #     for task in self.timesheet_ids:
    #         self.timesheet_ids = task

    # smart button
    def action_timesheet_button(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Timesheets',
            'view_mode': 'list,form',
            'res_model': 'project.timesheet',
            'domain': [('tasks_id', '=', self.id)],
        }

    # @api.onchange('task_assignees_ids')
    # def _onchange_task_assignees_ids(self):
    #     for i in self.task_assignees_ids:
    #         i.active = False

    # def write(self, vals):
    #     for i in self :
    #         before = i.task_assignees_ids
    #     res = super().write(vals)
    #
    #     if self.task_assignees_ids:
    #         for i in self:
    #             new = i.task_assignees_ids
    #             print(new,"---------")
    #             added_users = new - before
    #             removed_users = before - new
    #             print(added_users , removed_users , "---------")
    #             for u in added_users:
    #                 u.active = False
    #             for u in removed_users:
    #                 u.active = True
    #     return res

    def write(self, vals):

        for task in self:
            old_users = task.task_assignees_ids

        res = super().write(vals)

        if 'task_assignees_ids' in vals:

            for task in self:
                new_users = task.task_assignees_ids
                print(new_users, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                added_users = new_users - old_users
                removed_users = old_users - new_users
                print(added_users, removed_users, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                # mark added users unavailable
                for user in added_users:
                    user.available = False
                # mark removed users available
                for user in removed_users:
                    user.available = True

        return res