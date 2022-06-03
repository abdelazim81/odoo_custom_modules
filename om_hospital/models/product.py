from odoo import api, models, _, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    detailed_type = fields.Selection(selection_add=[('test', 'Test')],
                                     ondelete={'test': 'cascade'})
