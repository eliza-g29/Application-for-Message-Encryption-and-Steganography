from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import os
import base64


PRIVATE_KEY_FILE = "cheie_privata_rsa.pem"
PUBLIC_KEY_FILE = "cheie_publica_rsa.pem"


def genereaza_chei_rsa():
    """
    Genereaza o pereche de chei RSA:
    - cheia publica este folosita pentru criptare
    - cheia privata este folosita pentru decriptare
    """

    cheie_privata = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    cheie_publica = cheie_privata.public_key()

    private_pem = cheie_privata.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = cheie_publica.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(PRIVATE_KEY_FILE, "wb") as f:
        f.write(private_pem)

    with open(PUBLIC_KEY_FILE, "wb") as f:
        f.write(public_pem)


def verifica_sau_genereaza_chei():
    """
    Verifica daca exista cheile RSA.
    Daca nu exista, le genereaza automat.
    """

    if not os.path.exists(PRIVATE_KEY_FILE) or not os.path.exists(PUBLIC_KEY_FILE):
        genereaza_chei_rsa()


def incarca_cheie_publica():
    """
    Incarca cheia publica RSA din fisier.
    """

    verifica_sau_genereaza_chei()

    with open(PUBLIC_KEY_FILE, "rb") as f:
        cheie_publica = serialization.load_pem_public_key(f.read())

    return cheie_publica


def incarca_cheie_privata():
    """
    Incarca cheia privata RSA din fisier.
    """

    verifica_sau_genereaza_chei()

    with open(PRIVATE_KEY_FILE, "rb") as f:
        cheie_privata = serialization.load_pem_private_key(
            f.read(),
            password=None
        )

    return cheie_privata


def cripteaza_mesaj(mesaj):
    """
    Cripteaza un mesaj folosind RSA.

    Pentru criptare se foloseste cheia publica.
    Rezultatul este codificat Base64 ca sa poata fi afisat ca text
    si ascuns ulterior intr-o imagine.
    """

    cheie_publica = incarca_cheie_publica()

    mesaj_bytes = mesaj.encode("utf-8")

    mesaj_criptat = cheie_publica.encrypt(
        mesaj_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    mesaj_criptat_base64 = base64.b64encode(mesaj_criptat)

    return mesaj_criptat_base64.decode("utf-8")


def decripteaza_mesaj(mesaj_criptat):
    """
    Decripteaza un mesaj criptat cu RSA.

    Pentru decriptare se foloseste cheia privata.
    """

    cheie_privata = incarca_cheie_privata()

    mesaj_criptat_bytes = base64.b64decode(mesaj_criptat.encode("utf-8"))

    mesaj_decriptat = cheie_privata.decrypt(
        mesaj_criptat_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return mesaj_decriptat.decode("utf-8")