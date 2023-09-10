# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, exceptions
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real estate offer"
    _order = "price desc"
    
    price = fields.Float()
    status = fields.Selection(copy=False,  selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    create_date = fields.Datetime(readonly=True, default=fields.Datetime.now())
    date_deadline = fields.Date(compute='_calculate_deadline', inverse='_inverse_calculate_deadline')
    property_type_id = fields.Many2one(related='property_id.property_type_id', string='Property Type', store=True)

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
            if deadline.date_deadline:
                date_deadline = fields.Date.from_string(deadline.date_deadline)
                create_date = fields.Date.from_string(fields.Datetime.now())
                deadline.validity = (date_deadline - create_date).days


    def status_accepted(self):
        property_field = self.property_id
        if property_field.selling_price == 0:
            if property_field:
                property_field.write({'selling_price': self.price})
                property_field.write({'buyer': self.partner_id})

                for accepted in self:
                    if accepted.status == 'refused' or 'None':
                        self.write({'status': 'accepted'}) 
                return True
        else:
            raise exceptions.ValidationError("There is already an accepted offer.")


    def status_refused(self):
        property_field = self.property_id
        if property_field:
            property_field.write({'selling_price': 0})
            property_field.write({'buyer': self.env.ref('base.partner_root')})

        for refused in self:
            if refused.status == 'accepted' or 'None':
                self.write({'status': 'refused'}) 
        return True


    # @api.constrains('price')
    # def _check_offer_price(self):
    #     if self.property_id.offer_ids and self.price < min(self.property_id.offer_ids.mapped('price')):
    #         raise exceptions.ValidationError("Offer amount cannot be less than an existing offer.")


    @api.model
    def create(self, vals):
        offer = super(EstatePropertyOffer, self).create(vals)
        if offer.property_id:
            property_record = self.env['estate.property'].browse(offer.property_id.id)
            #self._check_offer_price()
            property_record.write({'state': 'offer received'})
        return offer


    _sql_constraints = [
        ('check_offer_price', 'CHECK(price >= 0)', 'The offer price can\'t be negative.'),
    ]