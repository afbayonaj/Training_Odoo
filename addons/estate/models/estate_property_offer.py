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


    # Pendiente solo se puede aceptar una oferta por una propiedad determinada!
    def status_accepted(self):
        property_field = self.property_id
        if property_field:
            property_field.write({'selling_price': self.price})
            property_field.write({'buyer': self.partner_id})

        for accepted in self:
            if accepted.status == 'refused' or 'None':
                self.write({'status': 'accepted'}) 
        return True


    def status_refused(self):
        property_field = self.property_id
        if property_field:
            property_field.write({'selling_price': 0})
            property_field.write({'buyer': self.env.ref('base.partner_root')})

        for refused in self:
            if refused.status == 'accepted' or 'None':
                self.write({'status': 'refused'}) 
        return True