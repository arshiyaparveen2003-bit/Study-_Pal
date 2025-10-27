from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(40, 10, 'This is a sample PDF file!')
pdf.ln(20)
pdf.set_font('Arial', '', 12)
pdf.multi_cell(0, 10, 'You can use this PDF to test the upload and question features of your Flask app.\n\nFeel free to edit this script to generate different content.')

pdf.output('sample.pdf')
print('sample.pdf has been created.') 