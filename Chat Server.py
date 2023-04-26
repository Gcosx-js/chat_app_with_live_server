
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import ctypes

istifadeciler = {}
cihaz_adresleri = {}

HOST = '127.0.0.1'
PORT = 23847
mesaj_kodlamasi = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def gelen_mesaj():
    while True:
        client, istifadeci_adresleri = SERVER.accept()
        print("%s:%s bağlandı." % istifadeci_adresleri)
        client.send(bytes("Xoş gəldiniz!\n", "utf8"))
        istifadeciler[client] = True  # soketi sözlük anahtarı olarak ekle
        Thread(target=baglan_client, args=(client,)).start()

def baglan_client(client):
    istifadeci_adi = client.recv(mesaj_kodlamasi).decode("utf8")
    cihaz_adresleri[client] = istifadeci_adi
    
    while True:
        try:
            msg = client.recv(mesaj_kodlamasi)
            yayin(bytes(f"", "utf8") + msg, client)
        except:
            client.close()
            del istifadeciler[client]
            del cihaz_adresleri[client]
            ctypes.windll.user32.MessageBoxW(0, "{} adlı istifadəçinin bağlantısı kəsildi.".format(istifadeciler[client]), "Leave Server", 0x10)
            

def yayin(msg, msg_sender):
    for sock in istifadeciler:
        if sock != SERVER and sock != msg_sender:
            sock.send(msg)


if __name__ == "__main__":
    SERVER.listen(10)#user sayi
    ctypes.windll.user32.MessageBoxW(0, "Server işə salındı.\nBağlantı gözlənilir..", "Server məlumatı", 0)
    qebulu_baslat = Thread(target=gelen_mesaj)
    qebulu_baslat.start()
    qebulu_baslat.join()
    SERVER.close()
