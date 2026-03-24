{
    "name": "Hotel Management",
    "version": "1.0",
    "description": """ Hotel management description""",
    "summary": """ Hotel management summary""",

    "category":"Uncategorized",
    "installable": True,
    "website":"https://www.hotelmanagement.com",
    "depends":["base"],
    "data":[
        "security/ir.model.access.csv",
        "views/hotel.xml",
        "views/room.xml",
        "views/guest.xml",
        "views/booking.xml",
        "views/service.xml",
    ],

    "author": "odoo trainee",
    "license":"LGPL-3",
}