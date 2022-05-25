from odoo import fields, api, models


class AllPatientReport(models.AbstractModel):
    # name convention    report.module_name.report_template_id
    _name = "report.om_hospital.template_patient_wizard_report"
    _description = "Patients list"

    # the name of function is fixed

    @api.model
    def _get_report_values(self, docids, data=None):
        domain = []
        gender = data.get('form_data').get('gender')
        if gender:
            domain += [('gender', '=', gender)]
        age = data.get('form_data').get('age')
        if age !=0 :
            domain += [('age', '=', age)]
        docs = self.env['hospital.patient'].search(domain)
        return {
            "docs": docs
        }
