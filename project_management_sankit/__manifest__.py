{
    'name': 'Project Management',
    'version': '1.0',

    'summary': 'Project Management Sankit',
    'description': """
    this is Project Management Sankit
    """,
    'depends': ['base', 'contacts', 'account'],
    'data': [
        'security/project_group.xml',
        'security/ir.model.access.csv',
        'demo/project_demo.xml',
        'wizard/task_billing_wizard.xml',
        'wizard/project_billing_wizard.xml',
        'views/projects.xml',
        'views/tasks.xml',
        'views/timesheet.xml',
        'views/stage_view.xml',
        'views/rate_calculation.xml',
        'report/task_report.xml',
        'report/tasks_report.xml',
        'views/res_config_setting.xml',
        'data/project_cron.xml',
    ],
    'installable': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
