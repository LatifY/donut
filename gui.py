import tkinter as tk
from tkinter import ttk
import config
import main

class GUI(tk.Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.title("Donut Hız")
        self.geometry("500x300")
        self.resizable(False, False)

        self.slider_value = tk.DoubleVar(value=config.SPEED)
        self.speed_label = tk.Label(self, text="Hız", font=("Montserrat", 12))
        self.value_label = tk.Label(self, text=self.get_slider_value())
        self.slider = ttk.Scale(self, from_=0, to=100, orient="horizontal", command=self.slider_changed, variable=self.slider_value)

        self.check_reverse = tk.IntVar()
        self.check_reverse_button = tk.Checkbutton(self, text='Ters Gölge',variable=self.check_reverse, font=("Montserrat", 12), onvalue=1, offvalue=0, command=self.check_reverse_changed)

        #SPEED: 
        self.speed_label.grid(
            row=1,
            columnspan=2,
            sticky='n',
            ipadx=10,
            ipady=10
        )

        #32.50
        self.value_label.grid(
            row=2,
            columnspan=2,
            sticky="n"
        )


        self.slider.grid(
            column=1,
            row=0,
            sticky="we"
        )

        self.check_reverse_button.grid(
            row=4,
            column=1,
            sticky="w"
        )

        self.color_string = tk.StringVar()
        self.color_string.trace('w', self.color_string_changed)
        self.color_choosen = ttk.Combobox(self, width = 27, textvariable = self.color_string, font=("Montserrat", 15))
        self.color_choosen["values"] = list(config.COLORS.keys())
        self.color_choosen.grid(
            row=6,
            column=1,
            sticky="w"
        )
        self.color_choosen.set("Beyaz")


        #CHECK BOX COLORS
        '''
        bottom_row = 5

        color_variables = []
        color_buttons = []

        def change_color(color):
            for button in color_buttons:
                button.deselect()
            print(color)
            main.change_color(color)

        for i in range(len(config.COLORS)):
            color = list(config.COLORS.keys())[i]
            value = tk.IntVar()
            color_button = tk.Checkbutton(self, text=color,variable=value, onvalue=1, offvalue=0, command=lambda: change_color(config.COLORS[color]))

            row = 0
            column = 0
            sticky = ""
            if(i % 2 == 0):
                sticky = "w"
                column = 0
                row = bottom_row
            else:
                sticky = "e"
                column = 1
                row = bottom_row
                bottom_row+=1
            color_button.grid(
                row=row,
                column=column,
                sticky=sticky
            )

            color_variables.append(value)
            color_buttons.append(color_button)
        '''

        self.credit_label = tk.Label(self, text="latif (hayatinda hic donut yemedi)", font=("Montserrat", 20))
        self.credit_label.grid(
            row=20,
            column=1,
            ipady=30
        )

        self.mainloop()


    def get_slider_value(self):
        value = int(self.slider_value.get())
        config.SPEED = value
        return value
    

    def color_string_changed(self,*args):
        main.change_color(config.COLORS[self.color_choosen.get()])

    def slider_changed(self, event):
        self.value_label.configure(text=self.get_slider_value())

    def check_reverse_changed(self):
        if config.REVERSED:
            config.REVERSED = False
        else:
            config.REVERSED = True
        # main.change_illumination()