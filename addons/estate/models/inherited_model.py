from odoo import fields, models


class InheritedModel(models.Model):
    _name = 'inherited.model'
    _inherit = 'res.users'
    _description = 'Inheritance Model'

    property_ids = fields.One2many('estate.property', 'seller', string='Properties', domain=[('state', '=', 'offer received')])


    # ir.model.access.csv:
    # access_inherited_model,access_inherited_model,model_access_inherited_model,base.group_user,1,1,1,1
