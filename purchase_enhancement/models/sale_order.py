from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def _prepare_invoice_line(self, line):
        invoice_line_vals = super(SaleOrder, self)._prepare_invoice_line(line)

        stock_move = self.env['stock.move'].search([('sale_line_id', '=', line.id)], limit=1)
        if stock_move:
            invoice_line_vals['dimension'] = stock_move.dimension

        return invoice_line_vals
