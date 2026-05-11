from PIL import Image


DELIMITATOR = "###STOP###"


def text_in_biti(text):
    """
    Transforma textul in sir de biti.
    Fiecare caracter este reprezentat pe 8 biti.
    """
    biti = ""

    for caracter in text:
        biti += format(ord(caracter), "08b")

    return biti


def biti_in_text(biti):
    """
    Transforma un sir de biti inapoi in text.
    """
    text = ""

    for i in range(0, len(biti), 8):
        byte = biti[i:i + 8]

        if len(byte) == 8:
            text += chr(int(byte, 2))

    return text


def ascunde_mesaj(cale_imagine_intrare, cale_imagine_iesire, mesaj):
    """
    Ascunde un mesaj intr-o imagine folosind metoda LSB.
    Se modifica bitul cel mai putin semnificativ al canalelor RGB.
    """
    imagine = Image.open(cale_imagine_intrare)
    imagine = imagine.convert("RGB")

    pixeli = list(imagine.getdata())

    mesaj_final = mesaj + DELIMITATOR
    biti_mesaj = text_in_biti(mesaj_final)

    capacitate = len(pixeli) * 3

    if len(biti_mesaj) > capacitate:
        raise ValueError("Mesajul este prea mare pentru aceasta imagine.")

    pixeli_noi = []
    index_bit = 0

    for pixel in pixeli:
        r, g, b = pixel

        if index_bit < len(biti_mesaj):
            r = (r & ~1) | int(biti_mesaj[index_bit])
            index_bit += 1

        if index_bit < len(biti_mesaj):
            g = (g & ~1) | int(biti_mesaj[index_bit])
            index_bit += 1

        if index_bit < len(biti_mesaj):
            b = (b & ~1) | int(biti_mesaj[index_bit])
            index_bit += 1

        pixeli_noi.append((r, g, b))

    imagine_noua = Image.new("RGB", imagine.size)
    imagine_noua.putdata(pixeli_noi)
    imagine_noua.save(cale_imagine_iesire)

    print("Mesajul a fost ascuns cu succes in imagine.")


def extrage_mesaj(cale_imagine):
    """
    Extrage mesajul ascuns dintr-o imagine folosind metoda LSB.
    Daca nu gaseste delimitatorul, inseamna ca imaginea nu contine mesaj ascuns valid.
    """
    imagine = Image.open(cale_imagine)
    imagine = imagine.convert("RGB")

    pixeli = list(imagine.getdata())

    biti = ""

    for pixel in pixeli:
        r, g, b = pixel

        biti += str(r & 1)
        biti += str(g & 1)
        biti += str(b & 1)

    text_extras = ""

    for i in range(0, len(biti), 8):
        byte = biti[i:i + 8]

        if len(byte) == 8:
            caracter = chr(int(byte, 2))
            text_extras += caracter

            if DELIMITATOR in text_extras:
                text_extras = text_extras.replace(DELIMITATOR, "")
                return text_extras

    raise ValueError("Imaginea nu contine un mesaj ascuns valid.")