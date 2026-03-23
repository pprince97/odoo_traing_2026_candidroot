{
    'name': 'Hotel Management System',
    'version': '19.0.0.1',
    'category': 'uncategorized',
    'summary': 'Hotel Management System',
    'description': "Hotel Management System",
    'author': 'Patel & Patel',
    'depends' : ['base', 'mail'],
    'data' : [
        'security/ir.model.access.csv',
        'views/hotel_hotel.xml',
        'views/hotel_room.xml',
        'views/hotel_guest.xml',
        'views/hotel_booking.xml',
        'views/hotel_service.xml',

    ],

    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}