# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


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
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        required=True,
        default='new',
        copy=False,
        string='Status',
        selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer Accepted', 'Offer Accepted'), ('sold and canceled', 'Sold and Canceled')]
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
            

    best_price = fields.Float(compute='_max_offer')

    @api.depends('offer_ids.price')
    def _max_offer(self):
        for best in self:
            max_price = max(best.offer_ids.mapped('price'))
            best.best_price = max_price

    """
    name = fields.Char('Plan Name', required=True, translate=True)
    number_of_months = fields.Integer('# Months', required=True)
    active = fields.Boolean('Active', default=True)
    sequence = fields.Integer('Sequence', default=10)
    """
    """    
    _sql_constraints = [
        ('check_number_of_months', 'CHECK(number_of_months >= 0)', 'The number of month can\'t be negative.'),
    ]
    """
    