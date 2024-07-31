{
    'name': 'Purchase Enhancement',
    'author': 'Youssef',
    'depends': ['base', 'purchase', 'mail', 'sale', 'product', 'stock' ],
    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',
        'views/purchase_request.xml',
        'views/rejection_wizard.xml',
        'views/sale_order.xml',
        'views/product_template.xml',
        'views/stock_move.xml',
        'views/account_invoice_line.xml',
        # 'data/email_templates.xml'
    ],
    'demo': [],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
