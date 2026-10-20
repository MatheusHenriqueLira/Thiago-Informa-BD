from tkinter import Tk, filedialog

janela = Tk()
janela.withdraw()

caminho = filedialog.askopenfilename(
    title="Selecione uma imagem",
    filetypes=[
        ("Imagens", "*.png *.jpg *.jpeg *.webp")
    ]
)

janela.destroy()

if caminho:
    print("Imagem selecionada:", caminho)
else:
    print("Nenhuma imagem selecionada.")