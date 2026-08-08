import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def invia_email(config, articoli):

    smtp_config = config["smtp"]

    numero_articoli = len(articoli)

    oggetto = (
        f"Rifornimento necessario - "
        f"{numero_articoli} articoli"
    )

    # Costruzione righe della tabella HTML
    righe_html = ""

    for articolo in articoli:

        righe_html += f"""
        <tr>
            <td style="
                border: 1px solid #cccccc;
                padding: 8px;
                text-align: left;
            ">
                {articolo['articolo']}
            </td>

            <td style="
                border: 1px solid #cccccc;
                padding: 8px;
                text-align: right;
            ">
                {articolo['giacenza']}
            </td>

            <td style="
                border: 1px solid #cccccc;
                padding: 8px;
                text-align: right;
            ">
                {articolo['soglia']}
            </td>
        </tr>
        """

    # Corpo HTML
    testo_html = f"""
    <html>
        <body>

            <p>
                Sono presenti <strong>{numero_articoli} articoli</strong>
                che necessitano di rifornimento.
            </p>

            <table style="
                border-collapse: collapse;
                width: 600px;
                font-family: Arial, sans-serif;
            ">

                <thead>
                    <tr style="background-color: #eeeeee;">
                        <th style="
                            border: 1px solid #cccccc;
                            padding: 8px;
                            text-align: left;
                        ">
                            Articolo
                        </th>

                        <th style="
                            border: 1px solid #cccccc;
                            padding: 8px;
                            text-align: right;
                        ">
                            Giacenza
                        </th>

                        <th style="
                            border: 1px solid #cccccc;
                            padding: 8px;
                            text-align: right;
                        ">
                            Soglia
                        </th>
                    </tr>
                </thead>

                <tbody>
                    {righe_html}
                </tbody>

            </table>

            <p>
                Si consiglia di procedere con il rifornimento.
            </p>

        </body>
    </html>
    """

    # Versione testuale per client che non supportano HTML
    testo_plain = f"""
    Sono presenti {numero_articoli} articoli
    che necessitano di rifornimento.

    Articolo - Giacenza - Soglia

    """

    for articolo in articoli:

        testo_plain += (
            f"{articolo['articolo']} - "
            f"{articolo['giacenza']} - "
            f"{articolo['soglia']}\n"
        )

    testo_plain += """
    Si consiglia di procedere con il rifornimento.
    """

    # Creazione email multipart
    messaggio = MIMEMultipart("alternative")

    messaggio["Subject"] = oggetto
    messaggio["From"] = smtp_config["from"]
    messaggio["To"] = smtp_config["to"]

    # Prima versione plain text
    messaggio.attach(
        MIMEText(
            testo_plain,
            "plain",
            "utf-8"
        )
    )

    # Seconda versione HTML
    messaggio.attach(
        MIMEText(
            testo_html,
            "html",
            "utf-8"
        )
    )

    # Invio
    with smtplib.SMTP(
        smtp_config["server"],
        smtp_config["port"]
    ) as server:

        server.starttls()

        server.login(
            smtp_config["username"],
            smtp_config["password"]
        )

        server.send_message(messaggio)

    print(
        f"[MAIL] Inviata notifica per "
        f"{numero_articoli} articoli"
    )