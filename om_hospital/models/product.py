from odoo import api, models, _, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"
    #  if new item before x item add new item then x item
    # if new item after x item add x item then new item
    detailed_type = fields.Selection(selection_add=[('test', 'Test'),
                                                    ('service',)
                                                    ],
                                     ondelete={'test': 'cascade'})
