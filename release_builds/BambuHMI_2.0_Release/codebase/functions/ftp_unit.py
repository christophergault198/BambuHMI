import ftplib
from tkinter import Tk, Frame, Button, Entry, Label, Listbox, Scrollbar, StringVar, END

class FTPClientGUI:
    def __init__(self, master):
        self.master = master
        master.title("Simple FTP Client")

        self.ftp = None

        # Connection Frame
        self.connection_frame = Frame(master)
        self.connection_frame.pack(pady=10)

        self.host_label = Label(self.connection_frame, text="Host:")
        self.host_label.pack(side="left")
        self.host_entry = Entry(self.connection_frame)
        self.host_entry.pack(side="left")

        self.connect_button = Button(self.connection_frame, text="Connect", command=self.connect_to_ftp)
        self.connect_button.pack(side="left")

        # File List
        self.file_listbox = Listbox(master, width=50)
        self.file_listbox.pack(pady=10)

        # Upload/Download Frame
        self.action_frame = Frame(master)
        self.action_frame.pack(pady=10)

        self.upload_button = Button(self.action_frame, text="Upload File", command=self.upload_file)
        self.upload_button.pack(side="left")

        self.download_button = Button(self.action_frame, text="Download File", command=self.download_file)
        self.download_button.pack(side="left")

    def connect_to_ftp(self):
        host = self.host_entry.get()
        self.ftp = ftplib.FTP_TLS()  # Create the FTP_TLS object without specifying the port
        self.ftp.connect(host, 990)  # Connect to the server using the specified host and port 990
        self.ftp.login('bblp', '4e1cf6eb')  # Use the provided username and password
        self.ftp.prot_p()  # Switch to secure data connection
        self.refresh_file_list()

    def refresh_file_list(self):
        self.file_listbox.delete(0, END)
        files = self.ftp.nlst()
        for file in files:
            self.file_listbox.insert(END, file)

    def upload_file(self):
        # Implement file upload functionality here
        # Example: self.ftp.storbinary('STOR filename.txt', open('filename.txt', 'rb'))
        pass

    def download_file(self):
        # Implement file download functionality here
        # Example: self.ftp.retrbinary('RETR filename.txt', open('filename.txt', 'wb').write)
        pass

if __name__ == "__main__":
    root = Tk()
    gui = FTPClientGUI(root)
    root.mainloop()
