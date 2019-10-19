import mysql.connector


class InvoiceOverdue:

    def __init__(self):
        # Make connection with database
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="your-password",
            database="vidsi"
        )

    # Get outstanding invoice
    def get_invoice_overdue(self):
        # Get results as dictionary
        mycursor = self.mydb.cursor(dictionary=True)
        # Query users with outstanding balance
        mycursor.execute('SELECT '
                            'subscriber.email, '
                            'subscriber.first_name, '
                            'subscriber.last_name, '
                            'subscriber_id, '
                            'invoice.id as invoice_number, '
                            'balance, '
                            'due_date '
                         'FROM'
                            ' invoice INNER JOIN subscriber '
                            'ON invoice.subscriber_id = subscriber.id '
                         'WHERE invoice.balance > 0;')
        # Get all invoices with outstanding balance
        return mycursor.fetchall()

    # Receives a dictionary of users with outstanding invoice balance
    def send_email(self, subscribers):
        for subscriber in subscribers:
            print("---------------------------------------")
            # Header for email
            email_header = 'From: account@vidsi.com\n' \
                           'To: ' + subscriber["email"] + \
                           '\nsubject: Cancellation Notice - Outstanding Balance\n\n'
            # Body of the message
            email_body = email_header + subscriber["first_name"] + \
                      ',\nOur records show that we haven’t yet received payment of $' + str(subscriber["balance"]) + \
                      ' for Invoice #' + str(subscriber["invoice_number"]) + \
                      ', which was due on ' + str(subscriber["due_date"]) + \
                      '. Failure to pay will lead to cancellation of your account.'
            # Create message and send
            message = "{}{}".format(email_header, email_body)
            print(message)


def main():
    # Call interface for Overdue invoice
    invoice_overdue = InvoiceOverdue()
    # Get subscribers who owe payment
    subscribers = invoice_overdue.get_invoice_overdue()
    # Send email to subscribers who have not paid
    invoice_overdue.send_email(subscribers)


if __name__ == "__main__":
    main()
