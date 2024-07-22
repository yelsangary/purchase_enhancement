{
    'name': 'Purchase Enhancement',
    'author': 'Youssef',
    'depends': ['base', 'purchase', 'mail' ],
    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',
        'views/purchase_request.xml',
        'views/rejection_wizard.xml',
        # 'data/email_templates.xml'
    ],
    'demo': [],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
