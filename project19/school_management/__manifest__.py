{
    "name": "School Management",
    "version":"0.1",
    "description" : """School Management description""",
    "summary": "School Management summary",

    "website": "http://www.school.com",
    "category": "Uncategorized",

    "installable":True,

    "depends":["base",'mail','sale_management','contacts'],
    "data":[
        "security/ir.model.access.csv",
        "views/student.xml",
        "views/teacher.xml",
        "views/class_view.xml",
        "views/subject.xml",
        "views/school.xml",
        "views/orm_student.xml",
        "views/orm_subject.xml",
        "views/admission_form.xml",
    ],
    "author":"odoo trainee",
    "license":"LGPL-3"
}