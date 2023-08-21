# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real estate offer"
    #_inherit = ['estate.property.offer']
    #_order = "sequence"
    
    price = fields.Float()
    status = fields.Selection(copy=False,  selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    create_date = fields.Datetime(readonly=True, default=fields.Datetime.now())
    date_deadline = fields.Date(compute='_calculate_deadline', inverse='_inverse_calculate_deadline')

    @api.depends('create_date', 'validity')
    def _calculate_deadline(self):
        for deadline in self:
            if deadline.create_date and deadline.validity:
                create_date = fields.Datetime.from_string(deadline.create_date)
                date_deadline = create_date + timedelta(days=deadline.validity)
                deadline.date_deadline = date_deadline.date()
            else:
                deadline.date_deadline = False

    def _inverse_calculate_deadline(self):
        for deadline in self:
            if deadline.create_date and deadline.date_deadline:
                create_date = fields.Datetime.from_string(deadline.create_date)
                validity = create_date - timedelta(days=deadline.date_deadline)
                deadline.validity = validity.date()
            else:
                deadline.validity = False