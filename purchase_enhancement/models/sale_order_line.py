from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    dimension = fields.Char(string="Dimension", related='product_id.dimension', readonly=0)

    # @api.onchange('product_id')
    # def _onchange_product_id(self):
    #     if self.product_id:
    #         self.dimension = self.product_id.dimension
