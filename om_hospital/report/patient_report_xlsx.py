from odoo import models
import base64
import io

class PartnerXlsx(models.AbstractModel):
    _name = 'report.om_hospital.report_patient_card_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, patients):
        column = 3
        row = 3
        # add sheet with specific name
        sheet = workbook.add_worksheet("Patients")
        # bold style
        bold = workbook.add_format({'bold': True})
        bold_center_yellow = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'yellow'})
        # customize cell width
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 45)
        # customize border
        bold_center_yellow.set_border(3)

        for obj in patients:
            sheet.merge_range(row, column, row, column + 1, "Patient Table", bold_center_yellow)
            row += 1
            # insert image
            if obj.patient_image:
                patient_image = io.BytesIO(base64.b64decode(obj.patient_image))
                sheet.insert_image(row+1 , column+1, "Patient_Image.png", {'image_data': patient_image, 'x_scale': 0.06, 'y_scale': 0.06, 'align': 'center'})
                row += 6
            # insert data to cells
            sheet.write(row, column, "Name", bold)
            sheet.write(row, column+1, obj.name)
            row += 1
            sheet.write(row, column, "Age", bold)
            sheet.write(row, column+1, obj.age)
            row += 1
            sheet.write(row, column, "Reference", bold)
            sheet.write(row, column + 1, obj.reference)
            row += 4
