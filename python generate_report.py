import csv
from statistics import mean, median
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

def read_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            data.append(list(map(float, row))) 
    return headers, data

def analyze_data(data):
    analysis = []
    for col in zip(*data):
        analysis.append({
            "min": min(col),
            "max": max(col),
            "mean": round(mean(col), 2),
            "median": median(col)
        })
    return analysis

def generate_pdf(headers, analysis, output_file):
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "Automated Report")
    
    c.setFont("Helvetica", 12)
    c.drawString(200, height - 70, "Generated using Python and ReportLab")
    
    table_data = [["Column", "Min", "Max", "Mean", "Median"]]
    for i, stats in enumerate(analysis):
        table_data.append([
            headers[i],
            stats["min"],
            stats["max"],
            stats["mean"],
            stats["median"]
        ])
    
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    table.wrapOn(c, width, height)
    table.drawOn(c, 50, height - 200)
    
    c.save()

def main():
    input_file = "Column1,Column2,Column3"
    output_file = " min, max, mean, and median "
    
    headers, data = read_data(input_file)
    analysis = analyze_data(data)
    
    generate_pdf(headers, analysis, output_file)
    printf("Report saved to {output_file}")

if __name__ == "__main__":
    main()
