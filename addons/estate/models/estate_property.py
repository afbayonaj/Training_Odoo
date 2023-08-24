# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, exceptions
from odoo.exceptions import ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate services"
    #_inherit = ['estate.property.type']
    #_order = "sequence"
    
    name = fields.Char(required=True, default="Unknown")
    description = fields.Text()
    postcode = fields.Char()
    #date_availability = fields.Date(copy=False, default=lambda self: (fields.Datetime.now() + fields.timedelta(days=90)).strftime('%Y-%m-%d'))
    #date_availability = fields.Date(copy=False, default=lambda self: (fields.Datetime.now() + fields.timedelta(days=90)))
    #date_availability = fields.Date(copy=False, default=fields.Datetime.now() + fields.timedelta(days=90))
    date_availability = fields.Date(copy=False, default=lambda self: fields.Datetime.now())
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'), 
            ('south', 'South'), 
            ('east', 'East'), 
            ('west', 'West'),
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        required=True,
        default='new',
        copy=False,
        string='Status',
        selection=[
            ('new', 'New'), 
            ('offer received', 'Offer Received'), 
            ('offer Accepted', 'Offer Accepted'), 
            ('sold', 'Sold'), 
            ('canceled', 'Canceled'),
        ]
    )
    last_seen = fields.Datetime("Last Seen", default=lambda self: fields.Datetime.now())
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    seller = fields.Many2one('res.users', string='Salesman', index=True, tracking=True, default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', string='Buyer', copy=False, index=True, tracking=True, default=lambda self: self.env.ref('base.partner_root'))
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Property Offer")
    

    total_area = fields.Integer(compute='_sum_total_area')

    @api.depends('living_area', 'garden_area')
    def _sum_total_area(self):
        for suma in self:
            suma.total_area = suma.living_area + suma.garden_area


    best_price = fields.Float(default=0, compute='_max_offer')

    @api.depends('offer_ids.price')
    def _max_offer(self):
        for best in self:
            max_price = max(best.offer_ids.mapped('price'))
            best.best_price = max_price


    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None


    def property_sold(self):
        for property_state_sold in self:
            if property_state_sold.state == 'sold':
                pass
            elif property_state_sold.state == 'canceled':
                raise exceptions.UserError("Canceled properties cannot be sold")  # Canceled properties cannot be sold
            else:
                property_state_sold.state = 'sold'
        return True


    def property_cancel(self):
        for property_state_cancel in self:
            if property_state_cancel.state == 'sold':
                raise exceptions.UserError("Sold properties cannot be canceled") # Sold properties cannot be canceled
            elif property_state_cancel.state == 'canceled':
                pass
            else:
                property_state_cancel.state = 'canceled'
        return True


    @api.constrains('selling_price', 'expected_price')
    def _validate_selling_price(self):
        for validate_price in self:
            if validate_price.selling_price != 0:
                if validate_price.selling_price < (validate_price.expected_price * 0.9):
                    raise exceptions.ValidationError(f"The selling price cannot be lower than 90% of the expected price.")


    # Si el valor de retorno es -1, significa que el primer valor es menor que el segundo.
    # Si el valor de retorno es 0, significa que ambos valores son iguales o muy cercanos en términos de precisión.
    # Si el valor de retorno es 1, significa que el primer valor es mayor que el segundo.
    # @api.constrains('selling_price', 'expected_price')
    # def _validate_selling_price(self):
    #     # if self.float_is_zero('selling_price', precision_rounding=0.01):
    #     #     pass
    #     for validation in self:
    #         # if self.float_is_zero(validation.selling_price, 0.01):
    #         #     pass
    #         if self.float_compare(validation.selling_price, validation.expected_price * 0.9, 0.01) == -1:
    #             raise ValidationError(f"The selling price cannot be lower than 90% of the expected price.")
    #     return True


    _sql_constraints = [
        ('check_property_expected_price', 'CHECK(expected_price >= 0)', 'The property expected price can\'t be negative.'),
        ('check_property_selling_price', 'CHECK(selling_price >= 0)', 'The property selling price can\'t be negative.'),
        ('check_property_expected_price', 'CHECK(expected_price >= 0)', 'The property expected price can\'t be negative.'),
    ]
    