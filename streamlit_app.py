import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4, A3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, A3
from PyPDF2 import PdfWriter, PdfReader
import io
from io import StringIO
from PIL import Image
import pandas as pd



st.title("Easy Homework-pdf maker")
st.sidebar.title("Upload screenshots of questions")
images = st.sidebar.file_uploader("", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
for image in images:
    bytes_data = image.read()
    st.sidebar.write(f"Question {images.index(image)+1}:", image.name)
    st.sidebar.image(image)

def add_image_to_first_page(pdf_path, image_path, output_path, page_size=A3, max_height_px=12000):
    # Open the image to get its size and calculate the aspect ratio
    with Image.open(image_path) as img:
        img_width, img_height = img.size
        aspect_ratio = img_height / img_width

    # Convert the max height from pixels to points (1 point = 1/72 inch)
    max_height_pt = max_height_px * (1 / 72)

    # Calculate the new width based on the max height and aspect ratio
    new_width_pt = max_height_pt / aspect_ratio

    # Create a PDF for the image
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=page_size)

    # Calculate the position to place the image at the top center
    x_position = (page_size[0] - new_width_pt) / 2
    y_position = page_size[1] - max_height_pt

    # Draw the image on the canvas at the calculated position and size
    c.drawImage(image_path, x_position, y_position, width=new_width_pt, height=max_height_pt, preserveAspectRatio=True, mask='auto')
    c.save()

    # Move the buffer position to the beginning
    packet.seek(0)
    new_pdf = PdfReader(packet)
    existing_pdf = PdfReader(open(pdf_path, "rb"))
    output = PdfWriter()

    # Add the image PDF as a watermark to the first page
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)

    # Add the rest of the pages from the existing PDF
    for i in range(1, len(existing_pdf.pages)):
        output.add_page(existing_pdf.pages[i])

    # Write the modified content to the output file
    with open(output_path, "wb") as outputStream:
        output.write(outputStream)

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

  c = canvas.Canvas(filename, pagesize=page_size)

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

  # Add your desired content to the PDF (optional)
  # ... your content code here ...
  c.save()
  add_image_to_first_page(filename, image_path, filename, page_size=A3, max_height_px=12000)

def merger(images, fname="file"):
   pdfs=[]
   for image in images:
      create_pdf(fname, image, num_pages=1, page_size=A3)
      pdfs.append(f"{fname}")

st.button("Make pdf", on_click=merger(images=images))