import wave


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


def ascunde_mesaj_audio(cale_audio_intrare, cale_audio_iesire, mesaj):
    """
    Ascunde un mesaj intr-un fisier audio WAV folosind metoda LSB.
    Se modifica bitul cel mai putin semnificativ al bytes-ilor audio.
    """

    audio = wave.open(cale_audio_intrare, mode="rb")

    params = audio.getparams()
    frames = bytearray(list(audio.readframes(audio.getnframes())))

    audio.close()

    mesaj_final = mesaj + DELIMITATOR
    biti_mesaj = text_in_biti(mesaj_final)

    if len(biti_mesaj) > len(frames):
        raise ValueError("Mesajul este prea mare pentru acest fisier audio.")

    for i in range(len(biti_mesaj)):
        frames[i] = (frames[i] & 254) | int(biti_mesaj[i])

    audio_nou = wave.open(cale_audio_iesire, mode="wb")
    audio_nou.setparams(params)
    audio_nou.writeframes(bytes(frames))
    audio_nou.close()


def extrage_mesaj_audio(cale_audio):
    """
    Extrage mesajul ascuns dintr-un fisier audio WAV folosind metoda LSB.
    Daca nu gaseste delimitatorul, inseamna ca fisierul nu contine mesaj ascuns.
    """

    audio = wave.open(cale_audio, mode="rb")
    frames = bytearray(list(audio.readframes(audio.getnframes())))
    audio.close()

    biti = ""

    for byte in frames:
        biti += str(byte & 1)

    text_extras = ""

    for i in range(0, len(biti), 8):
        byte = biti[i:i + 8]

        if len(byte) == 8:
            caracter = chr(int(byte, 2))
            text_extras += caracter

            if DELIMITATOR in text_extras:
                text_extras = text_extras.replace(DELIMITATOR, "")
                return text_extras

    raise ValueError("Fisierul audio nu contine un mesaj ascuns valid.")