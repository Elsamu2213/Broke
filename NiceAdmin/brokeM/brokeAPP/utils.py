from mailjet_rest import Client
from django.conf import settings

def enviar_correo_mailjet(destinatario, asunto, mensaje, archivo_adjunto=None):
    mailjet = Client(auth=(settings.MAILJET_API_KEY, settings.MAILJET_SECRET_KEY), version='v3.1')
    
    # Configuración del mensaje
    datos = {
        'Messages': [
            {
                "From": {
                    "Email": "pepeulmo@gmail.com",
                    "Name": "brokeee"
                },
                "To": [
                    {
                        "Email": destinatario,
                        "Name": "Nombre Destinatario"
                    }
                ],
                "Subject": asunto,
                "TextPart": mensaje,
                "Attachments": [
                    {
                        "ContentType": "application/pdf",
                        "Filename": "archivo.pdf",
                        "Base64Content": archivo_adjunto
                    }
                ] if archivo_adjunto else []
            }
        ]
    }
    
    result = mailjet.send.create(data=datos)
    return result.status_code == 200
