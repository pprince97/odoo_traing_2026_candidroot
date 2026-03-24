{
    'name':'Project Management',
    'version':'0.1',
    'author':'jui',
    'category':'Uncategorized',

    'summary':"Project management summary",
    'description':"Project management description",

    'website':"http://www.project.com",
    'license':'LGPL-3',
    'installable':True,
    'application':True,

    'depends': ['base','account'],
    'data':[
        'security/project_groups_security.xml',
        'security/ir_rules.xml',
        'security/ir.model.access.csv',
        'data/scheduled_actions.xml',
        'report/bill_report.xml',
        'demo/stage_demo.xml',
        'wizard/bill_wizard.xml',
        'views/res_config_settings.xml',
        'views/project_view.xml',
        'views/task_view.xml',
        'views/stage_view.xml',
        'views/timesheet_view.xml',
    ]
}