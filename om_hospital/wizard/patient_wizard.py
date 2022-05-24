from odoo import models, fields, api, _


class PatientWizard(models.TransientModel):
    _name = "patient.wizard.report"
    _description = "this model for representing patient report based in age and gender"

    age = fields.Integer(string="Age")
    gender = fields.Selection(
        [
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other')
        ], string="Gender"
    )

    def action_create_patient_report(self):
        return 0
