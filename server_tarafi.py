    def handle_client(self, client_socket):
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            self.process_received_data(data.decode('utf-8'))

        client_socket.close()

    def process_received_data(self, data):
        parts = data.split(':')
    
        if parts[0] == "Token" and parts[1] == self.SECRET_TOKEN:
            print(f"Gelen Veri: {parts[2]}")
            if parts[2] == "CONNECTION ACCEPT":
                print("KARSI TARAFTAN BAGLANTI ISTEGI GONDERILDI")
    
        elif parts[0] == "START_CHECKERS":
            proxy_method = parts[1]
    
            mapping = {
                "HTTP": "HTTP",
                "SOCKS4": "SOCKS4",
                "SOCKS5": "SOCKS5",
                "USER-PASS-HTTP": "USER:PASS (HTTP)",
                "USER-PASS-SOCKS4": "USER:PASS (SOCKS4)",
                "USER-PASS-SOCKS5": "USER:PASS (SOCKS5)"
            }
    
            if proxy_method in mapping:
                self.selected_option = mapping[proxy_method]
                self.degerdegistir(self.selected_option)
                indexx = self.selectproxymethod.findText(self.selected_option)
                self.selectproxymethod.setCurrentIndex(indexx)
                print(self.selected_option)
            else:
                print("Invalid proxy method:", proxy_method)
    
            checker_method = parts[2]
            checker_methods_list = ["BLUTV", "EXXEN", "VALORANT", "DISNEY", "DIGITURK",
                                        "CRUNCHYROLL", "TOD", "A101", "BKMKITAP", "DSMARTGO",
                                        "DUOLINGO", "FACEBOOK", "GAINTV", "LETGO"]
    
            if checker_method in checker_methods_list:
                self.checkername = checker_method
                self.degerdegistir2(self.checkername)
                index = self.selectchecker.findText(self.checkername)
                self.selectchecker.setCurrentIndex(index)
                print(self.checkername)
    
            else:
                print("Invalid checker method:", checker_method)
    
            bots_count = int(parts[3])
            self.threadcount = bots_count
            print(self.threadcount)
    
            print("START_CHECKERS")
            self.calistir()
    
        elif parts[0] == "STOP_CHECKERS":
            print("STOP_CHECKERS")
            self.durdur()
    
        else:
            print("Geçersiz token veya format.")
    
    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', 5000))
        server.listen(5)
        print("[*] Server dinleniyor...")

        while True:
            client, addr = server.accept()
            print(f"[*] Bağlantı kabul edildi: {addr[0]}:{addr[1]}")

            client_handler = threading.Thread(target=self.handle_client, args=(client,))
            client_handler.start()

    def calistir(self):
        self.stop.setEnabled(True)
        self.start_bt.setEnabled(False)
        print(self.checkername)
        print(self.selected_option)
        threading.Thread(target=self.main,daemon=True).start()

    def durdur(self):
        self.start_bt.setEnabled(True)
        self.stop.setEnabled(False)
        self.is_starting = False

    def sayfacagir(self):
        self.ana_sayfa.show() 
        self.close()
        
    def serverstarter(self):
        threading.Thread(target=self.start_server,daemon=True).start()
