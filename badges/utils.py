from fpdf import FPDF
from pdfrw import PageMerge, PdfReader, PdfWriter
from urllib import parse

from post_office import mail
from django.conf import settings

def create_watermark(coords_x=107, coords_y=0, text="Hello", font="helvetica", size=32,r=0,g=0,b=0):
    fpdf = FPDF(orientation="P", unit="mm", format="Letter")
    fpdf.add_page()
    fpdf.add_font(family="Great Vibes",fname="fonts/GreatVibes-Regular.ttf", uni=True)	
    fpdf.set_font(family="Great Vibes", size=size)
    fpdf.set_text_color(r,g,b)
    fpdf.set_xy(coords_x, coords_y)
    fpdf.cell(txt=text,align="C", center=True)
    reader = PdfReader(fdata=bytes(fpdf.output()))
    return reader.pages[0]

def generate_pdf(template_path=None, name=None, coords_y=0, result_path="", r=0,g=0,b=0):
    success = False
    result = ""
    if not template_path:
        result = "No template path provided"
        return success, result
    if not name:
        result = "No name provided"
        return success, result
        
    try:
        trailer = PdfReader(template_path)
    except Exception as e:
        result = "Error reading template: {}".format(e)
        return success, result

#    escaped_name = parse.quote(name)
    escaped_name = name
    relative_path = "{}/{}.pdf".format(result_path, escaped_name)
    full_path = "{}/{}".format(settings.RESULTS_DIR, relative_path)
    wmark = PageMerge().add(create_watermark(
        text=name,
        coords_y=coords_y,
        r=r,g=g,b=b
        ))[0]
    PageMerge(trailer.pages[0]).add(wmark, prepend=False).render()
    PdfWriter(full_path,trailer=trailer).write()
    success = True
    return success, relative_path




