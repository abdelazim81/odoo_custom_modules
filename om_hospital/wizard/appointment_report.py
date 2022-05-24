from odoo import models, fields, api, _


class AppointmentReportWizard(models.TransientModel):
    _name = "appointment.report.wizard"
    _description = "print report of appointments according to patient and date"

    patient_id = fields.Many2one('hospital.patient', string="Patient")
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date TO")

    def action_create_appointment_report(self):
        domain = []
        patient_id = self.read()[0].get('patient_id')
        if patient_id:
            domain += [('patient_id', '=', patient_id[0])]
        if self.date_from:
            domain += [('date_appointment', '>=', self.date_from)]
        if self.date_from:
            domain += [('date_appointment', '<=', self.date_to)]
        appointments = self.env['hospital.appointment'].search_read(domain)
        data = {
            "form_data": self.read()[0],
            "appointments": appointments
        }
        return self.env.ref('om_hospital.Appointment_report_with_domain').report_action(self, data=data)
