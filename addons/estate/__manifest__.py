{
    'name': "Real Estate",
    'depends': ['base'],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_menus.xml',
        'views/estate_property_tree_views.xml',
        'views/estate_property_form_views.xml',

        'views/estate_property_type_views.xml',
        'views/estate_property_type_menus.xml',
        'views/estate_property_type_tree_views.xml',
        #'views/estate_property_type_form_views.xml',

        'views/estate_property_tag_views.xml',
        'views/estate_property_tag_menus.xml',
        #'views/estate_property_tag_tree_views.xml',

        'views/estate_property_offer_tree_views.xml',
        'views/estate_property_offer_form_views.xml',


    ]
}