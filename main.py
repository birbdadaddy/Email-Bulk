import PySimpleGUI as sg
import smtplib  as smtp
from email.message import EmailMessage
import imghdr
sg.theme('DarkAmber')

def send_an_email(from_address, to_address, subject, message_text, user, password):
    # SMTP Servers for popular free services... add your own if needed. Format is: address, port
    google_smtp_server = 'smtp.gmail.com', 587
    microsoft_smtp_server = 'smtp.office365.com', 587
    yahoo_smtp_server = 'smtp.mail.yahoo.com', 587  # or port 465

    # open the email server connection
    if 'gmail' in user:
        smtp_host, smtp_port = google_smtp_server
    elif 'hotmail' in user or 'live' in user:
        smtp_host, smtp_port = microsoft_smtp_server
    elif 'yahoo' in user:
        smtp_host, smtp_port = yahoo_smtp_server
    else:
        sg.popup('Username does not contain a supported email provider')
        return
    server = smtp.SMTP(host=smtp_host, port=smtp_port)
    server.starttls()
    server.login(user=user, password=password)

    # create the email message headers and set the payload
    msg = EmailMessage()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.set_content(message_text)
    try:
        with open(values['-IMAGE-'], 'rb') as f:
            file_data = f.read()
            file_type = imghdr.what(f.name)
            file_name = f.name
        msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)
    except:
        print('no pic found')

    # open the email server and send the message
    server.send_message(msg)
                
layout = [[sg.Text('Send an Email', font='Default 18')],
            [sg.T('From:', size=(8,1)), sg.Input(key='-EMAIL FROM-', size=(35,1))],
            [sg.T('To(.txt file):', size=(8,1)), sg.T('', size=(2,1)), sg.FileBrowse(key='-EMAIL TO-', size=(10,1))],
            [sg.T('Subject:', size=(8,1)), sg.Input(key='-EMAIL SUBJECT-', size=(35,1))],
            [sg.T('Mail login information', font='Default 18')],
            [sg.T('User:', size=(8,1)), sg.Input(key='-USER-', size=(35,1))],
            [sg.T('Password:', size=(8,1)), sg.Input(password_char='*', key='-PASSWORD-', size=(35,1))],
            [sg.T('Import image: ', size=(10,1)), sg.T(''), sg.FileBrowse(key='-IMAGE-', size=(10,1))],
            [sg.Multiline('Type your message here', size=(60,10), key='-EMAIL TEXT-')],
            [sg.Button('Send'), sg.Button('Exit'), sg.T('', size=(20,1)), sg.Text('Made By ECH-CHARKAOUY')]]
sg.theme('DarkAmber')
window = sg.Window('Auto-Email Bot', layout)

while True:  # Event Loop
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == 'Send':
        bands = list()
        with open(values['-EMAIL TO-']) as fin:
            for line in fin:
                bands.append(line.strip())
        while True:
            try:
                print(bands)
                print(bands[0])
                if sg.__name__ != 'PySimpleGUIWeb':     # auto close popups not yet supported in PySimpleGUIWeb
                    sg.popup_quick_message('Sending your emails... this will take a moment...', background_color='black')
                send_an_email(from_address=values['-EMAIL FROM-'],
                            to_address= bands[0],
                            subject=values['-EMAIL SUBJECT-'],
                            message_text=values['-EMAIL TEXT-'],
                            user=values['-USER-'],
                            password=values['-PASSWORD-'])
                bands.pop(0)
            except:
                print('ERROR')
window.close()   
