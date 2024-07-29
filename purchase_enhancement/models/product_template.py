from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    dimension = fields.Char(string="Dimension", default='0x0')
