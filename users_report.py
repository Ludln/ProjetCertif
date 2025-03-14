from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from vulns.db_functions import get_all_users

def generate_user_list_pdf():
    # Récupérer la liste des utilisateurs depuis la base de données
    users = get_all_users()

    # Nom du fichier PDF de sortie
    output_filename = 'user_list.pdf'

    # Créer le fichier PDF
    pdf_canvas = canvas.Canvas(output_filename, pagesize=letter)
    pdf_canvas.setFont("Helvetica", 12)

    # Titre du document
    pdf_canvas.drawCentredString(letter[0] / 2, letter[1] - 36, "Liste des Utilisateurs Connus")

    # Ligne de séparation
    pdf_canvas.line(30, letter[1] - 60, letter[0] - 30, letter[1] - 60)

    # Contenu de la liste des utilisateurs
    y_position = letter[1] - 80
    for user in users:
        pdf_canvas.drawString(40, y_position, f"ID: {user[0]}, Nom d'utilisateur: {user[1]}, Prénom: {user[3]}, Nom: {user[4]}, Société: {user[5]}, login: {user[2]},")
        y_position -= 20

    # Enregistrez le fichier PDF
    pdf_canvas.save()

if __name__ == '__main__':
    generate_user_list_pdf()
