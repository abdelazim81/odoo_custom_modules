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
        data = {
            "form_data": self.read()[0]
        }
        return self.env.ref('om_hospital.patient_wizard_report_action').report_action(self, data)
