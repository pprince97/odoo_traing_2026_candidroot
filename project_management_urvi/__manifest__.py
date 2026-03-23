{
    'name': 'Project Management',
    'version': '0.1',
    'summary': 'Summary of project management',
    'description': """
    This is description of project management
    """,
    'category': 'Uncategorized',
    'website': 'https://www.project.com',
    'depends': ['base', 'hr_timesheet','account'],
    'data': [
        'security/project_security.xml',
        'security/ir.model.access.csv',
        'wizard/bill_wizard_view.xml',
        'views/schedule_act.xml',
        'views/stage_view.xml',
        'views/project_view.xml',
        'views/task_view.xml',
        'views/timesheet_view.xml',
        'views/hours_rate_view.xml',
        'views/config_parameter_bill.xml',
        'report/bill_report.xml',
        'report/project_bill_report.xml',
        'demo/stage_demo.xml'
    ],
    'demo': [
        'demo/stage_demo.xml'
    ],
    'application': True,
    'installable': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
