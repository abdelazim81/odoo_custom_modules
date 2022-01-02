from odoo import api, models, fields

class HospitalSale( models.Model ):
    _inherit = "sale.order"

    sale_description = fields.Text(string="Sale Description")
