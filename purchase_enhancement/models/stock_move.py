from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    dimension = fields.Char(string="Dimension")

    @api.model
    def create(self, vals):
        if 'sale_line_id' in vals:
            sale_line = self.env['sale.order.line'].browse(vals['sale_line_id'])
            vals['dimension'] = sale_line.dimension
        return super(StockMove, self).create(vals)
