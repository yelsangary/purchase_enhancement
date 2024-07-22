from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Purchase Request'

    name = fields.Char(string='Request Name', required=True)
    requested_by = fields.Many2one('res.users', string='Requested by', required=True, default=lambda self: self.env.user)
    start_date = fields.Date(string='Start Date', default=fields.Date.today)
    end_date = fields.Date(string='End Date')
    rejection_reason = fields.Text(string='Rejection Reason', readonly=True)
    order_line_ids = fields.One2many('purchase.request.line', 'request_id', string='Order Lines')
    total_price = fields.Float(string='Total Price', compute='_compute_total_price', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'To Be Approved'),
        ('approve', 'Approved'),
        ('reject', 'Rejected'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft', readonly=True)

    @api.depends('order_line_ids.total')
    def _compute_total_price(self):
        for request in self:
            request.total_price = sum(request.order_line_ids.mapped('total'))

    def action_submit_for_approval(self):
        if not self.order_line_ids:
            raise UserError(_("You cannot submit an empty purchase request. Please add at least one order line."))
        self.write({'state': 'to_approve'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_draft(self):
        self.write({'state': 'draft'})

    def action_approve(self):
        if self.state != 'to_approve':
            raise UserError(_("You can only approve purchase requests that are in 'To Be Approved' state."))
        self.send_approval_email()
        self.write({'state': 'approve'})


    def action_reject(self):
        return {
            'name': _('Reject Purchase Request'),
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_purchase_request_id': self.id},
        }

    def action_reset_to_draft(self):
        self.write({'state': 'draft'})

    def send_approval_email(self):
        purchase_managers = self.env.ref('purchase_enhancement.purchase_manager_group').users
        subject = f"Purchase Request ({self.name}) has been approved"
        body = f"Purchase request ({self.name}) has been approved."

        for manager in purchase_managers:
            self.env['mail.mail'].create({
                'subject': subject,
                'body_html': body,
                'email_to': manager.email,
            }).send()
            self.message_post(
                body=body,
                subject=subject,
                partner_ids=[manager.partner_id.id],
                subtype_id=self.env.ref('mail.mt_note').id
            )
        return True


    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.request') or '/'
        return super(PurchaseRequest, self).create(vals)


class PurchaseRequestLine(models.Model):
    _name = 'purchase.request.line'
    _description = 'Purchase Request Line'

    request_id = fields.Many2one('purchase.request', string='Purchase Request', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    description = fields.Char(string='Description', related='product_id.name', readonly=True)
    quantity = fields.Float(string='Quantity', default=1)
    cost_price = fields.Float(string='Cost Price', related='product_id.standard_price', readonly=True)
    total = fields.Float(string='Total', compute='_compute_total', store=True)

    @api.depends('quantity', 'cost_price')
    def _compute_total(self):
        for line in self:
            line.total = line.quantity * line.cost_price