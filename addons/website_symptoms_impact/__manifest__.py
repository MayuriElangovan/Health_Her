{   'name': 'Symptoms Website',
    'version': '1.0',
    'author': 'Mitosis Technologies',
    'summary': 'Symptoms and its negative impact in your life',
    'description': """
            Menstrual, Perimenopausal, Menopausal Symptoms and its negative impacts :
            * How can we support you?
            * What symptoms are you experiencing ?
            * Rate the negative impact on your life""",
    'category': 'Website',
    'sequence': 2,
    'website': '',
    'depends': ['website','symptoms','base'],
    'data': ['data/website_menu_data.xml',
             'views/layouts.xml',
             'views/category_page.xml',
             'views/symptoms_page.xml',
             ],
    'installable': True,
    'application': True,
    'auto_install': False,
 }
