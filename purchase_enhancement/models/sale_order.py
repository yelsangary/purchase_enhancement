from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Quotation Sent'),
        ('awaiting_first_approval', 'Awaiting First Approval'),
        ('awaiting_second_approval', 'Awaiting Second Approval'),
        ('awaiting_third_approval', 'Awaiting Third Approval'),
        ('sale', 'Sale Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    so_type = fields.Selection([
        ('local', 'Local'),
        ('export', 'Export')
    ], string='SO Type', default='local')

    def action_approval_first_level(self):
        if self.state != 'draft':
            self.state = 'awaiting_second_approval'

    def action_approval_second_level(self):
        if self.state != 'awaiting_second_approval':
            self.state = 'awaiting_third_approval'

    def action_approval_third_level(self):
        if self.state != 'awaiting_third_approval':
            self.state = 'sale'

    @api.model
    def _prepare_invoice_line(self, line):
        invoice_line_vals = super(SaleOrder, self)._prepare_invoice_line(line)

        stock_move = self.env['stock.move'].search([('sale_line_id', '=', line.id)], limit=1)
        if stock_move:
            invoice_line_vals['dimension'] = stock_move.dimension

        return invoice_line_vals
