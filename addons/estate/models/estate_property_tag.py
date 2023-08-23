# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real estate tag"
    #_inherit = ['estate.property.tag']
    #_order = "sequence"
    
    name = fields.Char(required=True)

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'A property tag name must be unique.'),
    ]