from xhtml2pdf import pisa
from io import StringIO
from flask import render_template,Flask, Response

app=Flask(__name__)
app.debug=True

@app.route("/")
def create_pdf(pdf_data):
        filename= "file.pdf"
          pdf=pisa.CreatePDF( StringIO(pdf_data),file(filename, "wb"))
        return Response(pdf, mimetype='application/octet-stream',
                        headers={"Content-Disposition": "attachment;filename=%s" % filename})

if __name__ == "__main__":
        app.run()