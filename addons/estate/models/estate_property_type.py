# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate type"
    #_order = "sequence"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'A property type name must be unique.'),
    ]