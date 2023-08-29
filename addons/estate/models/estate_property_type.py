# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate type"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Property")
    sequence = fields.Integer()
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Property Offer")
    offer_count = fields.Integer(string='Number of Offers', compute='_compute_offer_count')


    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)
        return True


    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'A property type name must be unique.'),
    ]