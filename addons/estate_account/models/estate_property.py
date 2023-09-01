from odoo import fields, models, api
import logging

class InheritedEstateProperty(models.Model):
    _inherit = 'estate.property'

    
    def property_sold(self):
        _logger = logging.getLogger(__name__)
        _logger.info("Esta entrando en la funcion, Congratulations!")

        # self.env['account.move'].create(
        #     {
        #         "name": "",
        #         "line_ids": [
        #             Command.create(
        #                 {
        #                     "filed_1": "value_1",
        #                     "filed_2": "value_2",
        #                 }
        #             )
        #         ]
        #     }
        # )

        return super(InheritedEstateProperty, self).property_sold()

    
# class InheritedAccountMove(models.Model):
#     _inherit = 'account.move'
