import customtkinter as ctk

from controller import Controller


def main():
    """Запускает программу."""
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = Controller(root)

    root.mainloop()


if __name__ == "__main__":
    main()
