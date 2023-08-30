from odoo import fields, models


class InheritedModel(models.Model):
    _name = 'inherited.model'
    _inherit = 'res.users'
    _description = 'Inheritance Model'

    property_ids = fields.One2many('estate.property', 'seller', string='Properties', domain=[('state', '=', 'offer received')])
