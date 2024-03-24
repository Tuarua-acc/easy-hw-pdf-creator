import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4, A3
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4, A3
from PyPDF2 import PdfWriter, PdfReader
import io
from io import StringIO, BytesIO
from PIL import Image
import pandas as pd



st.title("Easy Homework-pdf maker")
st.sidebar.title("Upload screenshots of questions")
images = st.sidebar.file_uploader("", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
for image in images:
    bytes_data = image.read()
    st.sidebar.write(f"Question {images.index(image)+1}:", image.name)
    st.sidebar.image(image)

# def add_image_to_first_page(pdf_path, image_path, output_path, page_size=A3, max_height_px=12000):   

def create_pdf(filename, image_path, num_pages=1, page_size=A3, grid_spacing=20, grid_color="#cccccc", grid_line_width=0.5):
  """Creates a PDF with a square grid on each page and page numbers.

  Args:
      filename (str): Name of the output PDF file.
      num_pages (int, optional): Number of pages in the PDF (default is 1).
      page_size (tuple, optional): Size of the PDF page in points (default is A4).
      grid_spacing (int, optional): Spacing between grid lines in points (default is 20).
      grid_color (str, optional): Color of the grid lines (default is "#cccccc").
      grid_line_width (float, optional): Width of the grid lines in points (default is 0.5).
  """
  buffer = BytesIO()
  c = canvas.Canvas(buffer, pagesize=page_size)

  # Define functions to draw grid lines and page number
  def draw_horizontal_line(y):
    c.setStrokeColor(grid_color)
    c.setLineWidth(grid_line_width)
    c.line(0, y, page_size[0], y)

  def draw_vertical_line(x):
    c.setStrokeColor(grid_color)
    c.setLineWidth(grid_line_width)
    c.line(x, 0, x, page_size[1])

  # Draw grid and page number for each page
  for page_num in range(1, num_pages + 1):
    # Draw grid
    num_h_lines = int(page_size[1] / grid_spacing) + 1
    num_v_lines = int(page_size[0] / grid_spacing) + 1

    for i in range(num_h_lines):
      y = i * grid_spacing
      draw_horizontal_line(y)

    for i in range(num_v_lines):
      x = i * grid_spacing
      draw_vertical_line(x)

    # Start a new page for subsequent iterations
    if page_num < num_pages:
      c.showPage()  # Explicitly create a new page for multi-page PDFs
  #Add image of question
  image = ImageReader(image_path)
  image_width, image_height = image.getSize()
  aspect_ratio = image_width / image_height
  new_height = page_size[1] / 6
  new_width = new_height * aspect_ratio
  if new_width > page_size[0]:
    new_width = page_size[0]
    new_height = new_width / aspect_ratio


  x = 0  # adjust as needed
  y = page_size[1] - new_height  # adjust as needed
  c.drawImage(image, x, y, width=new_width, height=new_height)
  # ... your content code here ...
  c.save()
  pdf_data=buffer.getvalue()
  return pdf_data

def merger(images, fname="file"):
   pdfs=[]
   for image in images:
      file = create_pdf(fname, image, num_pages=1, page_size=A3)
      pdfs.append(file)
      st.text(pdfs)
    # Create a PdfWriter object
   merge = PdfWriter()
   for pdf in pdfs:
    merge.append(BytesIO(pdf))
   
   buffer = BytesIO()
   
   merge.write(buffer)
   merge.close()
   pdf_data = buffer.getvalue()
   # Create a download button for the merged PDF
   st.download_button("Download Merged PDF", data=pdf_data, file_name="merged.pdf", mime='application/pdf')

    


result=st.button("Make pdf")
if result:
   merger(images)