import tkinter as tk
from tkinter import filedialog, messagebox

from crypto_utils import cripteaza_mesaj, decripteaza_mesaj
from stego_utils import ascunde_mesaj, extrage_mesaj
from audio_stego_utils import ascunde_mesaj_audio, extrage_mesaj_audio


class AplicatieStegoCrypto:
    def __init__(self, root):
        self.root = root
        self.root.title("Criptare si Steganografie")
        self.root.geometry("1000x750")
        self.root.minsize(850, 600)
        self.root.resizable(True, True)

        self.cale_imagine_originala = ""
        self.cale_imagine_extragere = ""
        self.cale_audio_original = ""
        self.cale_audio_extragere = ""

        self.creeaza_container_scrollabil()
        self.creeaza_interfata()

    def creeaza_container_scrollabil(self):
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(
            self.root,
            orient="vertical",
            command=self.canvas.yview
        )

        self.container = tk.Frame(self.canvas)

        self.container.bind(
            "<Configure>",
            lambda event: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.container,
            anchor="n"
        )

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind(
            "<Configure>",
            lambda event: self.canvas.itemconfig(
                self.canvas_window,
                width=event.width
            )
        )

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def creeaza_interfata(self):
        titlu = tk.Label(
            self.container,
            text="Aplicatie pentru Criptare si Steganografie",
            font=("Arial", 18, "bold")
        )
        titlu.pack(pady=(15, 8))

        explicatie = tk.Label(
            self.container,
            text=(
                "Criptarea ascunde continutul mesajului.\n"
                "Steganografia ascunde existenta mesajului intr-un fisier multimedia.\n"
                "Aplicatia permite ascunderea mesajelor in imagini PNG si fisiere audio WAV."
            ),
            font=("Arial", 11),
            justify="center"
        )
        explicatie.pack(pady=(0, 8))

        # MESAJ
        frame_mesaj = tk.LabelFrame(self.container, text="Mesaj", padx=10, pady=8)
        frame_mesaj.pack(fill="x", padx=25, pady=6)

        mesaj_inner = tk.Frame(frame_mesaj)
        mesaj_inner.pack()

        self.text_mesaj = tk.Text(
            mesaj_inner,
            height=3,
            width=95,
            wrap="word"
        )
        self.text_mesaj.pack()

        # CRIPTARE
        frame_crypto = tk.LabelFrame(self.container, text="Criptare RSA", padx=10, pady=8)
        frame_crypto.pack(fill="x", padx=25, pady=6)

        crypto_inner = tk.Frame(frame_crypto)
        crypto_inner.pack()

        btn_cripteaza = tk.Button(
            crypto_inner,
            text="Cripteaza mesaj",
            width=30,
            command=self.cripteaza
        )
        btn_cripteaza.grid(row=0, column=0, padx=12, pady=4)

        btn_decripteaza = tk.Button(
            crypto_inner,
            text="Decripteaza mesaj",
            width=30,
            command=self.decripteaza
        )
        btn_decripteaza.grid(row=0, column=1, padx=12, pady=4)

        # IMAGINE
        frame_imagini = tk.LabelFrame(
            self.container,
            text="Steganografie imagine PNG",
            padx=10,
            pady=8
        )
        frame_imagini.pack(fill="x", padx=25, pady=6)

        imagini_inner = tk.Frame(frame_imagini)
        imagini_inner.pack()

        btn_select_originala = tk.Button(
            imagini_inner,
            text="Alege imagine originala",
            width=30,
            command=self.alege_imagine_originala
        )
        btn_select_originala.grid(row=0, column=0, padx=12, pady=4)

        self.label_originala = tk.Label(
            imagini_inner,
            text="Nicio imagine aleasa",
            width=35,
            anchor="w"
        )
        self.label_originala.grid(row=0, column=1, padx=12, pady=4)

        btn_select_extragere = tk.Button(
            imagini_inner,
            text="Alege imagine pentru extragere",
            width=30,
            command=self.alege_imagine_extragere
        )
        btn_select_extragere.grid(row=1, column=0, padx=12, pady=4)

        self.label_extragere = tk.Label(
            imagini_inner,
            text="Nicio imagine aleasa",
            width=35,
            anchor="w"
        )
        self.label_extragere.grid(row=1, column=1, padx=12, pady=4)

        btn_ascunde_img = tk.Button(
            imagini_inner,
            text="Ascunde mesaj in imagine",
            width=30,
            command=self.ascunde_in_imagine
        )
        btn_ascunde_img.grid(row=2, column=0, padx=12, pady=4)

        btn_extrage_img = tk.Button(
            imagini_inner,
            text="Extrage mesaj din imagine",
            width=30,
            command=self.extrage_din_imagine
        )
        btn_extrage_img.grid(row=2, column=1, padx=12, pady=4)

        btn_cripteaza_ascunde_img = tk.Button(
            imagini_inner,
            text="Cripteaza + ascunde in imagine",
            width=30,
            command=self.cripteaza_si_ascunde_in_imagine
        )
        btn_cripteaza_ascunde_img.grid(row=3, column=0, padx=12, pady=4)

        btn_extrage_decripteaza_img = tk.Button(
            imagini_inner,
            text="Extrage + decripteaza din imagine",
            width=30,
            command=self.extrage_si_decripteaza_din_imagine
        )
        btn_extrage_decripteaza_img.grid(row=3, column=1, padx=12, pady=4)

        # AUDIO
        frame_audio = tk.LabelFrame(
            self.container,
            text="Steganografie audio WAV",
            padx=10,
            pady=8
        )
        frame_audio.pack(fill="x", padx=25, pady=6)

        audio_inner = tk.Frame(frame_audio)
        audio_inner.pack()

        btn_select_audio_original = tk.Button(
            audio_inner,
            text="Alege audio original WAV",
            width=30,
            command=self.alege_audio_original
        )
        btn_select_audio_original.grid(row=0, column=0, padx=12, pady=4)

        self.label_audio_original = tk.Label(
            audio_inner,
            text="Niciun fisier audio ales",
            width=35,
            anchor="w"
        )
        self.label_audio_original.grid(row=0, column=1, padx=12, pady=4)

        btn_select_audio_extragere = tk.Button(
            audio_inner,
            text="Alege audio pentru extragere",
            width=30,
            command=self.alege_audio_extragere
        )
        btn_select_audio_extragere.grid(row=1, column=0, padx=12, pady=4)

        self.label_audio_extragere = tk.Label(
            audio_inner,
            text="Niciun fisier audio ales",
            width=35,
            anchor="w"
        )
        self.label_audio_extragere.grid(row=1, column=1, padx=12, pady=4)

        btn_ascunde_audio = tk.Button(
            audio_inner,
            text="Ascunde mesaj in audio",
            width=30,
            command=self.ascunde_in_audio
        )
        btn_ascunde_audio.grid(row=2, column=0, padx=12, pady=4)

        btn_extrage_audio = tk.Button(
            audio_inner,
            text="Extrage mesaj din audio",
            width=30,
            command=self.extrage_din_audio
        )
        btn_extrage_audio.grid(row=2, column=1, padx=12, pady=4)

        btn_cripteaza_ascunde_audio = tk.Button(
            audio_inner,
            text="Cripteaza + ascunde in audio",
            width=30,
            command=self.cripteaza_si_ascunde_in_audio
        )
        btn_cripteaza_ascunde_audio.grid(row=3, column=0, padx=12, pady=4)

        btn_extrage_decripteaza_audio = tk.Button(
            audio_inner,
            text="Extrage + decripteaza din audio",
            width=30,
            command=self.extrage_si_decripteaza_din_audio
        )
        btn_extrage_decripteaza_audio.grid(row=3, column=1, padx=12, pady=4)

        # REZULTAT
        frame_rezultat = tk.LabelFrame(self.container, text="Rezultat", padx=10, pady=8)
        frame_rezultat.pack(fill="x", padx=25, pady=6)

        rezultat_inner = tk.Frame(frame_rezultat)
        rezultat_inner.pack()

        scroll_rezultat = tk.Scrollbar(rezultat_inner)
        scroll_rezultat.pack(side="right", fill="y")

        self.text_rezultat = tk.Text(
            rezultat_inner,
            height=8,
            width=95,
            wrap="word",
            yscrollcommand=scroll_rezultat.set
        )
        self.text_rezultat.pack(side="left")

        scroll_rezultat.config(command=self.text_rezultat.yview)

        # BUTON CURATARE
        btn_curata = tk.Button(
            self.container,
            text="Curata campurile",
            width=30,
            command=self.curata
        )
        btn_curata.pack(pady=(8, 18))

    def citeste_mesaj(self):
        return self.text_mesaj.get("1.0", tk.END).strip()

    def afiseaza_rezultat(self, text):
        self.text_rezultat.delete("1.0", tk.END)
        self.text_rezultat.insert(tk.END, text)

    def cripteaza(self):
        mesaj = self.citeste_mesaj()

        if mesaj == "":
            messagebox.showwarning("Atentie", "Introdu un mesaj.")
            return

        try:
            mesaj_criptat = cripteaza_mesaj(mesaj)
            self.afiseaza_rezultat(mesaj_criptat)
        except Exception as e:
            messagebox.showerror("Eroare", str(e))

    def decripteaza(self):
        mesaj_criptat = self.citeste_mesaj()

        if mesaj_criptat == "":
            messagebox.showwarning("Atentie", "Introdu mesajul criptat.")
            return

        try:
            mesaj = decripteaza_mesaj(mesaj_criptat)
            self.afiseaza_rezultat(mesaj)
        except Exception:
            messagebox.showerror(
                "Eroare",
                "Mesajul nu poate fi decriptat. Verifica mesajul sau cheia."
            )

    def alege_imagine_originala(self):
        cale = filedialog.askopenfilename(
            title="Alege imagine originala",
            filetypes=[
                ("Imagini PNG", "*.png"),
                ("Toate fisierele", "*.*")
            ]
        )

        if cale:
            self.cale_imagine_originala = cale
            self.label_originala.config(text=self.scurteaza_cale(cale))

    def alege_imagine_extragere(self):
        cale = filedialog.askopenfilename(
            title="Alege imagine pentru extragere",
            filetypes=[
                ("Imagini PNG", "*.png"),
                ("Toate fisierele", "*.*")
            ]
        )

        if cale:
            self.cale_imagine_extragere = cale
            self.label_extragere.config(text=self.scurteaza_cale(cale))

    def alege_audio_original(self):
        cale = filedialog.askopenfilename(
            title="Alege fisier audio original",
            filetypes=[
                ("Fisiere WAV", "*.wav"),
                ("Toate fisierele", "*.*")
            ]
        )

        if cale:
            self.cale_audio_original = cale
            self.label_audio_original.config(text=self.scurteaza_cale(cale))

    def alege_audio_extragere(self):
        cale = filedialog.askopenfilename(
            title="Alege fisier audio pentru extragere",
            filetypes=[
                ("Fisiere WAV", "*.wav"),
                ("Toate fisierele", "*.*")
            ]
        )

        if cale:
            self.cale_audio_extragere = cale
            self.label_audio_extragere.config(text=self.scurteaza_cale(cale))

    def scurteaza_cale(self, cale):
        if len(cale) <= 40:
            return cale

        return "..." + cale[-37:]

    def alege_salvare_imagine(self):
        cale = filedialog.asksaveasfilename(
            title="Salveaza imaginea rezultata",
            defaultextension=".png",
            filetypes=[
                ("Imagini PNG", "*.png")
            ]
        )

        return cale

    def alege_salvare_audio(self):
        cale = filedialog.asksaveasfilename(
            title="Salveaza fisierul audio rezultat",
            defaultextension=".wav",
            filetypes=[
                ("Fisiere WAV", "*.wav")
            ]
        )

        return cale

    def ascunde_in_imagine(self):
        mesaj = self.citeste_mesaj()

        if self.cale_imagine_originala == "":
            messagebox.showwarning("Atentie", "Alege o imagine originala.")
            return

        if mesaj == "":
            messagebox.showwarning("Atentie", "Introdu mesajul de ascuns.")
            return

        cale_iesire = self.alege_salvare_imagine()

        if cale_iesire == "":
            return

        try:
            ascunde_mesaj(self.cale_imagine_originala, cale_iesire, mesaj)
            self.afiseaza_rezultat(
                "Mesajul a fost ascuns cu succes in imagine.\n\n"
                f"Imagine salvata la:\n{cale_iesire}"
            )
            messagebox.showinfo("Succes", "Mesajul a fost ascuns in imagine.")
        except Exception as e:
            messagebox.showerror("Eroare", str(e))

    def extrage_din_imagine(self):
        if self.cale_imagine_extragere == "":
            messagebox.showwarning("Atentie", "Alege imaginea din care extragi mesajul.")
            return

        try:
            mesaj = extrage_mesaj(self.cale_imagine_extragere)
            self.afiseaza_rezultat(mesaj)
        except Exception as e:
            messagebox.showerror("Eroare", str(e))

    def cripteaza_si_ascunde_in_imagine(self):
        mesaj = self.citeste_mesaj()

        if self.cale_imagine_originala == "":
            messagebox.showwarning("Atentie", "Alege o imagine originala.")
            return

        if mesaj == "":
            messagebox.showwarning("Atentie", "Introdu mesajul secret.")
            return

        cale_iesire = self.alege_salvare_imagine()

        if cale_iesire == "":
            return

        try:
            mesaj_criptat = cripteaza_mesaj(mesaj)
            ascunde_mesaj(self.cale_imagine_originala, cale_iesire, mesaj_criptat)

            self.afiseaza_rezultat(
                "Mesajul a fost criptat si apoi ascuns in imagine.\n\n"
                f"Mesaj criptat:\n{mesaj_criptat}\n\n"
                f"Imagine salvata la:\n{cale_iesire}"
            )

            messagebox.showinfo("Succes", "Mesajul criptat a fost ascuns in imagine.")
        except Exception as e:
            messagebox.showerror("Eroare", str(e))

    def extrage_si_decripteaza_din_imagine(self):
        if self.cale_imagine_extragere == "":
            messagebox.showwarning("Atentie", "Alege imaginea din care extragi mesajul.")
            return

        try:
            mesaj_criptat = extrage_mesaj(self.cale_imagine_extragere)
            mesaj = decripteaza_mesaj(mesaj_criptat)

            self.afiseaza_rezultat(
                f"Mesaj criptat extras:\n{mesaj_criptat}\n\n"
                f"Mesaj final decriptat:\n{mesaj}"
            )

        except Exception:
            messagebox.showerror(
                "Eroare",
                "Mesajul nu a putut fi extras sau decriptat."
            )

    def ascunde_in_audio(self):
        mesaj = self.citeste_mesaj()

        if self.cale_audio_original == "":
            messagebox.showwarning("Atentie", "Alege un fisier audio WAV original.")
            return

        if mesaj == "":
            messagebox.showwarning("Atentie", "Introdu mesajul de ascuns.")
            return

        cale_iesire = self.alege_salvare_audio()

        if cale_iesire == "":
            return

        try:
            ascunde_mesaj_audio(self.cale_audio_original, cale_iesire, mesaj)
            self.afiseaza_rezultat(
                "Mesajul a fost ascuns cu succes in fisierul audio.\n\n"
                f"Fisier audio salvat la:\n{cale_iesire}"
            )
            messagebox.showinfo("Succes", "Mesajul a fost ascuns in fisierul audio.")
        except Exception as e:
            messagebox.showerror("Eroare", str(e))

    def extrage_din_audio(self):
        if self.cale_audio_extragere == "":
            messagebox.showwarning("Atentie", "Alege fisierul audio din care extragi mesajul.")
            return

        try:
            mesaj = extrage_mesaj_audio(self.cale_audio_extragere)
            self.afiseaza_rezultat(mesaj)
        except Exception as e:
            messagebox.showerror("Eroare", str(e))

    def cripteaza_si_ascunde_in_audio(self):
        mesaj = self.citeste_mesaj()

        if self.cale_audio_original == "":
            messagebox.showwarning("Atentie", "Alege un fisier audio WAV original.")
            return

        if mesaj == "":
            messagebox.showwarning("Atentie", "Introdu mesajul secret.")
            return

        cale_iesire = self.alege_salvare_audio()

        if cale_iesire == "":
            return

        try:
            mesaj_criptat = cripteaza_mesaj(mesaj)
            ascunde_mesaj_audio(self.cale_audio_original, cale_iesire, mesaj_criptat)

            self.afiseaza_rezultat(
                "Mesajul a fost criptat si apoi ascuns in fisierul audio.\n\n"
                f"Mesaj criptat:\n{mesaj_criptat}\n\n"
                f"Fisier audio salvat la:\n{cale_iesire}"
            )

            messagebox.showinfo("Succes", "Mesajul criptat a fost ascuns in fisierul audio.")
        except Exception as e:
            messagebox.showerror("Eroare", str(e))

    def extrage_si_decripteaza_din_audio(self):
        if self.cale_audio_extragere == "":
            messagebox.showwarning("Atentie", "Alege fisierul audio din care extragi mesajul.")
            return

        try:
            mesaj_criptat = extrage_mesaj_audio(self.cale_audio_extragere)
            mesaj = decripteaza_mesaj(mesaj_criptat)

            self.afiseaza_rezultat(
                f"Mesaj criptat extras:\n{mesaj_criptat}\n\n"
                f"Mesaj final decriptat:\n{mesaj}"
            )

        except Exception:
            messagebox.showerror(
                "Eroare",
                "Mesajul nu a putut fi extras sau decriptat din fisierul audio."
            )

    def curata(self):
        self.text_mesaj.delete("1.0", tk.END)
        self.text_rezultat.delete("1.0", tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = AplicatieStegoCrypto(root)
    root.mainloop()