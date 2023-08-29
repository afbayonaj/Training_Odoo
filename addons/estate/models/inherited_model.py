from odoo import fields, models


class InheritedModel(models.Model):
    _name = 'inherited.model'
    _inherit = 'res_users'
    _description = 'Inheritance Model'

    property_ids = fields.One2many()