from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from vulns.db_functions import get_all_vulnerabilities

def generate_vulns_list_pdf():
    all_vulns = get_all_vulnerabilities()

    # Nom du fichier PDF de sortie
    output_filename = 'delivery_list.pdf'

    # Créer le fichier PDF
    pdf_canvas = canvas.Canvas(output_filename, pagesize=letter)
    pdf_canvas.setFont("Helvetica", 12)

    # Titre du document
    pdf_canvas.drawCentredString(letter[0] / 2, letter[1] - 36, "Liste des vulnerabilities")

    # Ligne de séparation
    pdf_canvas.line(30, letter[1] - 60, letter[0] - 30, letter[1] - 60)

    # Contenu de la liste des pièces en cours de livraison
    y_position = letter[1] - 80
    for vuln in all_vulns:
        pdf_canvas.drawString(40, y_position, f"{vuln[0]}, {vuln[1]}, {vuln[2]}, {vuln[3]}")
        y_position -= 20

    # Enregistrez le fichier PDF
    pdf_canvas.save()

if __name__ == '__main__':
    generate_vulns_list_pdf()
