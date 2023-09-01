from odoo import fields, models, api
import logging

class InheritedEstateProperty(models.Model):
    _inherit = 'estate.property'

    
    def property_sold(self):
        _logger = logging.getLogger(__name__)
        _logger.info("Esta entrando en la funcion, Congratulations!")

        return super(InheritedEstateProperty, self).property_sold()