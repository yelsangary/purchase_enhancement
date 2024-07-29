from odoo import models, fields


class AccountInvoiceLine(models.Model):
    _inherit = 'account.move.line'

    dimension = fields.Char(string="Dimension", default=0, readonly=True)
