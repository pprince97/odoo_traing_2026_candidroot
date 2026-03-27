{
    'name': 'Hotel Management',
    'version': '0.1',
    'category': 'Uncategorized',
    'summary': 'Hotel Management',
    'description': "",
    'author': 'My Company',
    'website': '',
    'depends': ['base','mail'],

    'data':[
        'security/ir.model.access.csv',
        'views/hm_hotel.xml',
        'views/hm_room.xml',
        'views/hm_guest.xml',
        'views/hm_booking.xml',
        'views/hm_service.xml',
    ],
    'installable': True,
    'application': True,
    'license':'LGPL-3',
}