import os
from reportlab.pdfgen import canvas

import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A5, letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

import sqlite3 as dbapi


class Informes:

    def __init__(self, option, id):
        if option:
            self.new_registration()
        else:
            if id != 0:
                self.monthly_bill(id)

    @staticmethod
    def new_registration():

        c = canvas.Canvas("new_registration.pdf", pagesize=letter)
        c.setLineWidth(.3)
        c.setFont('Helvetica', 12)

        c.drawString(30, 725, 'Academia Seijas')
        c.drawString(30, 710, 'La educacion para tontos')
        c.drawString(440, 750, str(time.ctime()))

        c.drawString(30, 650, 'Apellidos:')
        c.line(88, 647, 580, 647)

        c.drawString(30, 625, 'Nombre:')
        c.line(80, 622, 340, 622)

        c.drawString(360, 625, 'Fecha Nacimiento:')
        c.line(468, 622, 580, 622)

        c.drawString(30, 600, 'Direccion:')
        c.line(83, 597, 362, 597)

        c.drawString(382, 600, 'Codigo Postal:')
        c.line(468, 597, 580, 597)

        c.drawString(30, 575, 'e-mail:')
        c.line(72, 572, 580, 572)

        c.line(35, 535, 45, 535)
        c.line(35, 525, 45, 525)
        c.line(35, 535, 35, 525)
        c.line(45, 535, 45, 525)
        c.drawString(55, 525, "He leido y acepto las normas de convivencia y uso de la academia*")
        c.drawString(40, 490, "* Estos terminos y condiciones estan sujuetos a posibles modificaciones que en ningun momento")
        c.drawString(48, 475, "es necesaria su notificacion por parte de la direccion para que estas se apliquen")

        c.drawString(490, 400, "Academia Seijas")

        c.save()

    def monthly_bill(self, id):

        db = dbapi.connect("database.db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM students WHERE id='" + str(id) + "';")
        student = []
        for fila in cursor:
            student = str(fila[0]), str(fila[1]), int(fila[2])

        bill_name = "monthly_bill_" + student[1].split()[1].strip() + ".pdf"
        doc = SimpleDocTemplate(bill_name, pagesize=A5,
                                                    rightMargin=72,
                                                    leftMargin=72,
                                                    topMargin=72,
                                                    bottomMargin=18)
        Story = []

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

        ptext = '<font size=12>Vigo, %s</font>' % time.ctime()
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(2, 24))

        ptext = '<font size=12>Estimado %s:</font>' % student[1].split()[1].strip()
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))

        ptext = '<font size=12>Un mes mas, nos complace que siga disfrutando de nuestros servicios ' \
                'y que page religiosamente todos los meses la cantidad de: %s euros</font>' % 60
        Story.append(Paragraph(ptext, styles["Justify"]))
        Story.append(Spacer(1, 12))

        ptext = '<font size=12>Gracias por confiar en nuestra educacion</font>'
        Story.append(Paragraph(ptext, styles["Justify"]))
        Story.append(Spacer(1, 12))

        logo = "./views/icons/signed.png"
        im = Image(logo, 2*inch, inch)
        Story.append(im)

        doc.build(Story)
