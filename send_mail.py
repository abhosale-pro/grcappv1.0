import smtplib


def send_mail(customer, dealer, rating, comments):
    sender = "Private Person <from@example.com>"
    receiver = "A Test User <to@example.com>"

    message = f"""\
    Subject: Hi Mailtrap
    To: {receiver}
    From: {sender}
    <h3>New Feedback Submission</h3><ul><li>Customer: {customer}</li><li>Dealer: {dealer}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>"""

    # Send email
    with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
        server.starttls()
    server.login("eacc94c41259b0", "8bd10e0ed4a15a")
    server.sendmail(sender, receiver, message)
