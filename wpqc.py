"""
Module: Wrapping Paper Quotes Calculator (wpqc.py)
Author: Harsh Jayprakash <harshjayprakash@outlook.com>
Date: (Original) May 2022
License: MIT

Requires Python 3.8 or newer.

A proof of concept calculator application for a department who provide
gift wrapping services based on present shapes. This application was
part of a university assignment.

Changelog:
    v1.0.14 (23-05-2022): Orginal submitted version.
    v1.0.15 (05-01-2026): Added docstrings.
                          Updated application name.
"""
import decimal
import datetime
import math
import os
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkmsg
import typing

# the application metadata.

APPLICATION_NAME: str = "Wrapping Paper Quotes"
APPLICATION_VERSION: str = "1.0.14b-sc2"

# the system.


def round_number(amount: float, /) -> float:
    try:
        result = float(decimal.Decimal(amount).quantize(
            decimal.Decimal(".01"), rounding=decimal.ROUND_HALF_UP))
    except decimal.InvalidOperation:
        result = float(-1)
    return result


def pence_to_pounds(amount: float, /) -> float:
    return float(round_number(amount / 100))


def get_current_time_date() -> str:
    current_time_date = datetime.datetime.now()
    return current_time_date.strftime("%Y-%m-%d %H%M")


class PresentType:
    # abstract class

    def __init__(self) -> None:
        return

    # virtual/overridable method
    def get_recommended_area(self, *, height: float, width: float) -> float:
        if height <= 0 or width <= 0:
            return 0
        return round_number((height + 6) * (width + 6))


class Cube(PresentType):

    def __init__(self, *, length: float) -> None:
        super().__init__()
        self._length = length

    def __str__(self) -> str:
        return (
            f"Cube [l = {self.get_length()}cm] "
            + f"[area = {self.get_recommended_area()}cm^2]")

    def get_length(self) -> float:
        return self._length

    def set_length(self, length: float, /) -> None:
        self._length = length

    def get_recommended_area(self) -> float:
        return super().get_recommended_area(
            height=(3 * self.get_length()),
            width=(4 * self.get_length()))


class Cuboid(PresentType):

    def __init__(self, *, height: float, width: float, depth: float) -> None:
        super().__init__()
        self._height = height
        self._width = width
        self._depth = depth

    def __str__(self) -> str:
        return (
            f"Cuboid [w = {self.get_width()}cm, "
            + f"h = {self.get_height()}cm, "
            + f"d = {self.get_depth()}cm] "
            + f"[area = {self.get_recommended_area()}cm^2]")

    def get_height(self) -> float:
        return self._height

    def set_height(self, height: float, /) -> None:
        self._height = height

    def get_width(self) -> float:
        return self._width

    def set_width(self, width: float, /) -> None:
        self._width = width

    def get_depth(self) -> float:
        return self._depth

    def set_depth(self, depth: float, /) -> None:
        self._depth = depth

    def get_recommended_area(self) -> float:
        return super().get_recommended_area(
            height=((2 * self.get_height()) + (2 * self.get_width())),
            width=((2 * self.get_height()) + self.get_depth()))


class Cylinder(PresentType):

    def __init__(self, *, radius: float, depth: float) -> None:
        super().__init__()
        self._radius = radius
        self._depth = depth

    def __str__(self) -> str:
        return (
            f"Cylinder [r = {self.get_radius()} cm, "
            + f"d = {self.get_depth()}cm] "
            + f"[area = {self.get_recommended_area()} cm^2]")

    def get_radius(self) -> float:
        return self._radius

    def set_radius(self, radius: float, /) -> None:
        self._radius = radius

    def get_depth(self) -> float:
        return self._depth

    def set_depth(self, depth: float, /) -> None:
        self._depth = depth

    def get_recommended_area(self) -> float:
        return super().get_recommended_area(
            height=((4 * self.get_radius()) + self.get_depth()),
            width=(math.pi * (self.get_radius() * 2)))


class WrappingPaper:
    # abstract class

    PRESET_PURPLE: str = "purple"
    PRESET_DARK_SLATE_GREY: str = "DarkSlateGray4"
    PRESET_DEEP_SKY_BLUE: str = "deep sky blue"
    PRESET_LIGHT_SEA_GREEN: str = "light sea green"
    PRESET_VIOLET_RED: str = "VioletRed2"
    PRESET_GOLD: str = "gold"

    colours: typing.Dict[str, str] = {
        PRESET_PURPLE: "Purple",
        PRESET_DARK_SLATE_GREY: "Dark Slate Grey 4",
        PRESET_DEEP_SKY_BLUE: "Deep Sky Blue",
        PRESET_LIGHT_SEA_GREEN: "Light Sea Green",
        PRESET_VIOLET_RED: "Violet Red 2",
        PRESET_GOLD: "Gold"
    }

    def __init__(self, colour: str, price_cm_sq: float, /) -> None:
        self._colour = colour
        self._price_per_cm_sq = price_cm_sq

    def get_colour(self) -> str:
        return self._colour

    def set_colour(self, colour: str) -> None:
        self._colour = colour

    def get_price(self) -> float:
        return self._price_per_cm_sq

    def set_price(self, price: float, /) -> None:
        self._price_per_cm_sq = price

    def calculate_price(self, area: float, /) -> float:
        return area * self.get_price()


class ExpensiveWrappingPaper(WrappingPaper):

    def __init__(self, colour: str, /) -> None:
        super().__init__(colour, 0.75)

    def __str__(self) -> str:
        return (
            f"Expensive Wrapping Paper ["
            + WrappingPaper.colours[super().get_colour()]
            + "]")


class CheapWrappingPaper(WrappingPaper):

    def __init__(self, colour: str, /) -> None:
        super().__init__(colour, 0.40)

    def __str__(self) -> str:
        return (
            f"Cheap Wrapping Paper ["
            + WrappingPaper.colours[super().get_colour()]
            + "]")


class Bow:

    def __init__(self) -> None:
        self._price: float = 1.50

    def __str__(self) -> str:
        return "Bow"

    def get_price(self) -> float:
        return self._price

    def set_price(self, price: float, /) -> None:
        self._price = price


class GiftCard:

    def __init__(self, message: str, /) -> None:
        self._base_rate: float = 0.50
        self._char_rate: float = 0.02
        self._message = message

    def __str__(self) -> str:
        return (
            f"Gift Card ['"
            + f"{self.get_message()}']")

    def get_base_rate(self) -> float:
        return self._base_rate

    def set_base_rate(self, price: float, /) -> None:
        self._base_rate = price

    def get_char_rate(self) -> float:
        return self._char_rate

    def set_char_rate(self, price: float, /) -> None:
        self._char_rate = price

    def get_message(self) -> str:
        return self._message

    def set_message(self, message: str, /) -> None:
        self._message = message

    def calculate_price(self) -> float:
        return (
            self.get_base_rate()
            + (self.get_char_rate() * len(self.get_message())))


class Quote:

    def __init__(self, *,
                 quote_title: str,
                 present_type: PresentType,
                 wrapping_paper: WrappingPaper,
                 gift_card: GiftCard = None,
                 bow: Bow = None) -> None:
        self.title = quote_title
        self.present = present_type
        self.wrapping_paper = wrapping_paper
        self.gift_card = gift_card
        self.bow = bow

    def __str__(self) -> str:
        result: str = (
            f"£{self.calculate_price():.2f}"
            + f"   '{self.title}'")
        result += f"   |   {str(self.present)}"
        result += f"   |   {str(self.wrapping_paper)}"
        if isinstance(self.bow, Bow):
            result += f"   |   {str(self.bow)}"
        if isinstance(self.gift_card, GiftCard):
            result += f"   |   {str(self.gift_card)}"
        return result

    def calculate_price(self) -> float:
        total: float = 0
        if self.present.get_recommended_area() > 0:
            total += pence_to_pounds(
                self.wrapping_paper.calculate_price(
                    self.present.get_recommended_area()))
            if isinstance(self.gift_card, GiftCard):
                total += self.gift_card.calculate_price()
            if isinstance(self.bow, Bow):
                total += self.bow.get_price()
        return total


class Order:

    def __init__(self, order_number: int, /) -> None:
        self._order_number = order_number
        self.quotes: typing.List[Quote] = []

    def get_order_number(self) -> int:
        return self._order_number

    def calculate_total_price(self) -> float:
        total: float = 0
        for quote in self.quotes:
            total += quote.calculate_price()
        return round_number(total)

    def export_order(self) -> int:
        file = f"{get_current_time_date()} Order {self.get_order_number()}.txt"
        separator = ("-" * 80)
        try:
            with open(file, "w") as handler:
                handler.write(
                    separator
                    + "\n\n\tWrapping Paper Quotes\n\n"
                    + f"\tDate Time:\t\t\t\t\t\t"
                    + f"{get_current_time_date()}\n"
                    + f"\tOrder Number:\t\t\t\t\t"
                    + f"{self.get_order_number()}\n"
                    + f"\tNumber of Quotes:\t\t\t\t"
                    + f"{len(self.quotes)}\n\n"
                    + separator
                    + "\n\n")
                for q in self.quotes:
                    handler.write(
                        q.title
                        + f"   (Total: GBP {q.calculate_price():.2f})\n"
                        + f"\t\t{str(q.present)}\n"
                        + f"\t\t{str(q.wrapping_paper)}"
                        + f"""   (GBP {pence_to_pounds(
                            q.wrapping_paper.calculate_price(
                                q.present.get_recommended_area())):.2f})\n""")
                    if isinstance(q.gift_card, GiftCard):
                        handler.write(
                            f"\t\t{str(q.gift_card)}"
                            + f"   (GBP {q.gift_card.calculate_price():.2f})"
                            + "\n")
                    if isinstance(q.bow, Bow):
                        handler.write(
                            f"\t\t{str(q.bow)}"
                            + f"   (GBP {q.bow.get_price():.2f})\n")
                    handler.write("\n")
                handler.write(
                    "\n"
                    + "Total price for this order: GBP "
                    + f"{self.calculate_total_price():.2f}\n")
        except OSError:
            return 1
        return 0


# the user interface.


class Translator:
    # static class

    CUBE: str = "cube"
    CUBOID: str = "cuboid"
    CYLINDER: str = "cylinder"
    CHEAP_WRAPPING: str = "cheap"
    EXPENSIVE_WRAPPING: str = "expensive"
    BOW: str = "bow"
    GIFT_CARD: str = "giftcard"
    NONE: str = "none"

    @staticmethod
    def check_quote_title(title: str, /) -> str:
        if title == "":
            return "Untitled Quote"
        return title

    @staticmethod
    def translate_present_type(*, shape: str,
                               length_one: str,
                               length_two: str,
                               length_three: str) -> PresentType:
        dimension_one: float = 0
        dimension_two: float = 0
        dimension_three: float = 0
        try:
            dimension_one = abs(float(length_one))
            dimension_two = abs(float(length_two))
            dimension_three = abs(float(length_three))
        except ValueError:
            return None
        if shape == Translator.CUBE:
            return Cube(
                length=dimension_one)
        elif shape == Translator.CUBOID:
            return Cuboid(
                width=dimension_one,
                height=dimension_two,
                depth=dimension_three)
        elif shape == Translator.CYLINDER:
            return Cylinder(
                radius=dimension_one,
                depth=dimension_two)
        else:
            return None

    @staticmethod
    def check_present_lengths(shape: PresentType, /) -> int:
        if isinstance(shape, Cube):
            if (shape.get_length() <= 0):
                return 1
        elif isinstance(shape, Cuboid):
            if (shape.get_width() <= 0 or shape.get_height() <= 0
                    or shape.get_depth() <= 0):
                return 1
        elif isinstance(shape, Cylinder):
            if (shape.get_depth() <= 0 or shape.get_radius() <= 0):
                return 1
        return 0

    @staticmethod
    def translate_wrapping_paper_type(*, paper: str,
                                      colour: str) -> WrappingPaper:
        if paper == Translator.CHEAP_WRAPPING:
            return CheapWrappingPaper(colour)
        elif paper == Translator.EXPENSIVE_WRAPPING:
            return ExpensiveWrappingPaper(colour)
        else:
            return None

    @staticmethod
    def translate_colour(colour: str, /, *,
                         human_readable: bool = True) -> str:
        if human_readable:
            try:
                return WrappingPaper.colours[colour]
            except Exception:
                return "#000000"
        else:
            if (colour == WrappingPaper.colours[
                    WrappingPaper.PRESET_PURPLE]):
                return WrappingPaper.PRESET_PURPLE
            elif (colour == WrappingPaper.colours[
                    WrappingPaper.PRESET_DARK_SLATE_GREY]):
                return WrappingPaper.PRESET_DARK_SLATE_GREY
            elif (colour == WrappingPaper.colours[
                    WrappingPaper.PRESET_DEEP_SKY_BLUE]):
                return WrappingPaper.PRESET_DEEP_SKY_BLUE
            elif (colour == WrappingPaper.colours[
                    WrappingPaper.PRESET_LIGHT_SEA_GREEN]):
                return WrappingPaper.PRESET_LIGHT_SEA_GREEN
            elif (colour == WrappingPaper.colours[
                    WrappingPaper.PRESET_VIOLET_RED]):
                return WrappingPaper.PRESET_VIOLET_RED
            elif (colour == WrappingPaper.colours[
                    WrappingPaper.PRESET_GOLD]):
                return WrappingPaper.PRESET_GOLD
            else:
                return "#000000"

    @staticmethod
    def translate_gift_card(*, gift_card: int, message: str) -> GiftCard:
        if gift_card:
            return GiftCard(message)
        else:
            return None

    @staticmethod
    def translate_bow(*, bow: int) -> Bow:
        if bow:
            return Bow()
        else:
            return None


class ColourScheme:
    # storage class

    WHITE: str = "#FFFFFF"
    BLACK: str = "#000000"
    GREY: str = "#F6F6F6"
    LIGHT_MINT_GREEN: str = "#00858E"
    DARK_MINT_GREEN: str = "#00585E"
    RED: str = "#FF0000"


class WindowHeader(tk.Frame):

    def __init__(self, parent: tk.Tk, /) -> None:
        super().__init__(parent)
        self.config(
            bg=ColourScheme.WHITE, padx=15, pady=10)
        self._construct()
        self._display()

    def _construct(self) -> None:
        self._header_text = tk.StringVar()
        self._header_title = tk.Label(self)
        self._header_title.config(
            bg=ColourScheme.WHITE, fg=ColourScheme.DARK_MINT_GREEN,
            font="helvetica 14 bold", textvariable=self._header_text)

    def _display(self) -> None:
        self._header_title.pack(anchor="w", side="top")

    def set_title(self, title: str, /) -> None:
        self._header_text.set(title)


class QuoteSummaryPane(tk.Frame):

    def __init__(self, parent: tk.Tk, /):
        super().__init__(parent)
        self._shape_displayed: str = Translator.NONE
        self._pattern_displayed: str = Translator.NONE
        self._colour_displayed: str = "#000000"
        self.config(
            bg=ColourScheme.WHITE, height=100, padx=15, pady=15)
        self._construct()
        self._display()

    def _construct(self) -> None:
        self._shape_preview = tk.Canvas(self)
        self._shape_preview.config(
            bg=ColourScheme.WHITE, height=100, width=100)
        self._pattern_preview = tk.Canvas(self)
        self._pattern_preview.config(
            bg=ColourScheme.WHITE, height=100, width=100)
        self._info_container = tk.Frame(self)
        self._info_container.config(
            bg=ColourScheme.WHITE, padx=10, pady=10)
        self._title = tk.StringVar()
        self._quote_title = tk.Label(self._info_container)
        self._quote_title.config(
            bg=ColourScheme.WHITE, font="helvetica 10 bold",
            textvariable=self._title)
        self._shape = tk.StringVar()
        self._quote_shape = tk.Label(self._info_container)
        self._quote_shape.config(
            bg=ColourScheme.WHITE, font="helvetica 10",
            textvariable=self._shape)
        self._paper = tk.StringVar()
        self._quote_paper = tk.Label(self._info_container)
        self._quote_paper.config(
            bg=ColourScheme.WHITE, font="helvetica 10",
            textvariable=self._paper)
        self._additional = tk.StringVar()
        self._quote_additional = tk.Label(self._info_container)
        self._quote_additional.config(
            bg=ColourScheme.WHITE, font="helvetica 10",
            textvariable=self._additional)

    def _display(self) -> None:
        self._shape_preview.pack(
            anchor="w", side="left")
        self._pattern_preview.pack(
            anchor="w", padx=10, side="left")
        self._info_container.pack(
            anchor="nw", fill="both", side="left")
        self._quote_title.pack(
            anchor="nw", side="top")
        self._quote_shape.pack(
            anchor="nw", side="top")
        self._quote_paper.pack(
            anchor="nw", side="top")
        self._quote_additional.pack(
            anchor="nw", side="top")

    def get_shape_displayed(self) -> str:
        return self._shape_displayed

    def set_shape_displayed(self, shape: str, /) -> None:
        self._shape_displayed = shape

    def get_pattern_displayed(self) -> str:
        return self._pattern_displayed

    def set_pattern_displayed(self, pattern: str, /) -> None:
        self._pattern_displayed = pattern

    def get_colour_displayed(self) -> str:
        return self._colour_displayed

    def set_colour_displayed(self, colour: str, /) -> None:
        self._colour_displayed = colour

    def set_quote_title(self, price: float, title: str, /) -> None:
        self._title.set(f"£{price:.2f}     {title}")

    def set_quote_shape(self, shape: PresentType, /) -> None:
        if shape.get_recommended_area() > 0:
            self._shape.set(str(shape))
            if isinstance(shape, Cube):
                self.preview_cube_shape()
            elif isinstance(shape, Cuboid):
                self.preview_cuboid_shape()
            elif isinstance(shape, Cylinder):
                self.preview_cylinder_shape()
        else:
            self._shape.set("Invalid dimensions")

    def set_quote_paper(self, paper: WrappingPaper, /) -> None:
        self._paper.set(str(paper))
        self.set_colour_displayed(paper.get_colour())
        if isinstance(paper, CheapWrappingPaper):
            self.preview_cheap_pattern()
        if isinstance(paper, ExpensiveWrappingPaper):
            self.preview_expensive_pattern()

    def set_additional_options(self, bow: Bow, gift_card: GiftCard, /) -> None:
        display_string: str = ""
        if isinstance(bow, Bow):
            display_string += f"   {str(bow)}"
        if isinstance(gift_card, GiftCard):
            display_string += f"   {str(gift_card)}"
        self._additional.set(display_string)

    def clear_preview(self) -> None:
        self._shape_preview.delete(tk.ALL)
        self._pattern_preview.delete(tk.ALL)
        self._title.set("")
        self._shape.set("")
        self._paper.set("")
        self._additional.set("")
        self.set_pattern_displayed(Translator.NONE)
        self.set_shape_displayed(Translator.NONE)

    def preview_cube_shape(self) -> None:
        self._shape_preview.delete(tk.ALL)
        self.set_shape_displayed(Translator.CUBE)
        self._shape_preview.create_rectangle(
            42, 42, 72, 72, outline="#000000")
        self._shape_preview.create_rectangle(
            27, 27, 57, 57, outline="#000000")
        self._shape_preview.create_line(
            27, 27, 42, 42, fill="#000000")
        self._shape_preview.create_line(
            57, 57, 72, 72, fill="#000000")
        self._shape_preview.create_line(
            57, 27, 72, 42, fill="#000000")
        self._shape_preview.create_line(
            27, 57, 42, 72, fill="#000000")

    def preview_cuboid_shape(self) -> None:
        self._shape_preview.delete(tk.ALL)
        self.set_shape_displayed(Translator.CUBOID)
        self._shape_preview.create_rectangle(
            36, 52, 81, 72, outline="#000000")
        self._shape_preview.create_rectangle(
            21, 37, 66, 57, outline="#000000")
        self._shape_preview.create_line(
            21, 37, 36, 52, fill="#000000")
        self._shape_preview.create_line(
            66, 57, 81, 72, fill="#000000")
        self._shape_preview.create_line(
            66, 37, 81, 52, fill="#000000")
        self._shape_preview.create_line(
            21, 57, 36, 72, fill="#000000")

    def preview_cylinder_shape(self) -> None:
        self._shape_preview.delete(tk.ALL)
        self.set_shape_displayed(Translator.CYLINDER)
        self._shape_preview.create_oval(
            35, 27, 66, 42, outline="#000000")
        self._shape_preview.create_oval(
            35, 57, 66, 72, outline="#000000")
        self._shape_preview.create_line(
            35, 34, 35, 67, fill="#000000")
        self._shape_preview.create_line(
            66, 34, 66, 67, fill="#000000")

    def preview_cheap_pattern(self) -> None:
        self._pattern_preview.delete(tk.ALL)
        self.set_pattern_displayed(Translator.CHEAP_WRAPPING)
        for num in range(5):
            if num % 2 == 0:
                self._pattern_preview.create_rectangle(
                    0 + (num * 10), 0 + (num * 10),
                    20 + (num * 10), 20 + (num * 10),
                    fill=self.get_colour_displayed(),
                    outline=self.get_colour_displayed())
                self._pattern_preview.create_rectangle(
                    80 - (num * 10), 20 + (num * 10),
                    100 - (num * 10), 0 + (num * 10),
                    fill=self.get_colour_displayed(),
                    outline=self.get_colour_displayed())
                self._pattern_preview.create_rectangle(
                    100 - (num * 10), 100 - (num * 10),
                    80 - (num * 10), 80 - (num * 10),
                    fill=self.get_colour_displayed(),
                    outline=self.get_colour_displayed())
                self._pattern_preview.create_rectangle(
                    0 + (num * 10), 80 - (num * 10),
                    20 + (num * 10), 100 - (num * 10),
                    fill=self.get_colour_displayed(),
                    outline=self.get_colour_displayed())
            else:
                self._pattern_preview.create_rectangle(
                    0 + (num * 10), 0 + (num * 10),
                    20 + (num * 10), 20 + (num * 10),
                    fill="#ffffff",
                    outline=self.get_colour_displayed())
                self._pattern_preview.create_rectangle(
                    80 - (num * 10), 20 + (num * 10),
                    100 - (num * 10), 0 + (num * 10),
                    fill="#ffffff",
                    outline=self.get_colour_displayed())
                self._pattern_preview.create_rectangle(
                    100 - (num * 10), 100 - (num * 10),
                    80 - (num * 10), 80 - (num * 10),
                    fill="#ffffff",
                    outline=self.get_colour_displayed())
                self._pattern_preview.create_rectangle(
                    0 + (num * 10), 80 - (num * 10),
                    20 + (num * 10), 100 - (num * 10),
                    fill="#ffffff",
                    outline=self.get_colour_displayed())

    def preview_expensive_pattern(self) -> None:
        self._pattern_preview.delete(tk.ALL)
        self.set_pattern_displayed(Translator.EXPENSIVE_WRAPPING)
        for num in range(2):
            self._pattern_preview.create_rectangle(
                0 + (num * 50), 0 + (num * 50),
                50 + (num * 50), 50 + (num * 50),
                fill=self.get_colour_displayed(),
                outline=self.get_colour_displayed())
        for num in range(5):
            if num % 2 == 0:
                self._pattern_preview.create_rectangle(
                    50 + (num * 10), 0 - (num * 10),
                    100 + (num * 10), 50 - (num * 10),
                    fill="#ffffff",
                    outline="#000000")
                self._pattern_preview.create_rectangle(
                    0 - (num * 10), 50 + (num * 10),
                    50 - (num * 10), 100 + (num * 10),
                    fill="#ffffff",
                    outline="#000000")
            else:
                self._pattern_preview.create_rectangle(
                    50 + (num * 10), 0 - (num * 10),
                    100 + (num * 10), 50 - (num * 10),
                    fill=self.get_colour_displayed(),
                    outline="#000000")
                self._pattern_preview.create_rectangle(
                    0 - (num * 10), 50 + (num * 10),
                    50 - (num * 10), 100 + (num * 10),
                    fill=self.get_colour_displayed(),
                    outline="#000000")


class QuoteConfigurationWindow(tk.Toplevel):

    window_running_check: bool = False

    @staticmethod
    def raise_window_running_message() -> None:
        tkmsg.showinfo(
            "Information",
            "An instance of the quote configuration window is open. "
            + "Please close the previous instance before opening another.")

    def __new__(cls,
                parent: tk.Tk,
                new_quote: bool,
                quote_list: typing.List[Quote],
                quote_index: int = None, /) -> None:
        cls.window_running_check = True
        return super(QuoteConfigurationWindow, cls).__new__(cls)

    def __init__(self,
                 parent: tk.Tk,
                 new_quote: bool,
                 quote_list: typing.List[Quote],
                 quote_index: int = None, /) -> None:
        super().__init__(parent)
        self._new_quote = new_quote
        self._quote_list = quote_list
        self._quote_index = quote_index
        self.minsize(800, 600)
        self.resizable(False, False)
        self.title(f"Quote Configuration | {APPLICATION_NAME}")
        self._avoid_message_box_exit: bool = False
        self._the_quote: Quote = None
        self._construct()
        self._actions()
        self._track()
        self._display()
        self._load_quote()

    def _construct(self) -> None:
        self._construct_header()
        self._construct_quote_preview()
        self._construct_quote_options()
        self._construct_footer()

    def _construct_header(self) -> None:
        self._header = WindowHeader(self)
        self._header.set_title("Quote configuration.")

    def _construct_quote_preview(self) -> None:
        self._preview_pane = QuoteSummaryPane(self)

    def _construct_quote_options(self) -> None:
        self._options = tk.Frame(self)
        self._options.config(
            bg=ColourScheme.GREY, padx=25, pady=15)
        self._options_col_shape = tk.Label(self._options)
        self._options_col_shape.config(
            bg=ColourScheme.GREY, font="helvetica 10 bold", pady=2,
            text="Shape")
        self._options_shape = tk.LabelFrame(self._options)
        self._options_shape.config(
            bg=ColourScheme.GREY, padx=5, pady=5, text="Shape Type")
        self._shape = tk.StringVar()
        self._shape_cube = tk.Radiobutton(self._options_shape)
        self._shape_cube.config(
            bg=ColourScheme.GREY, padx=5, pady=5, text="Cube",
            value=Translator.CUBE, variable=self._shape)
        self._shape_cuboid = tk.Radiobutton(self._options_shape)
        self._shape_cuboid.config(
            bg=ColourScheme.GREY, padx=5, pady=5, text="Cuboid",
            value=Translator.CUBOID, variable=self._shape)
        self._shape_cylinder = tk.Radiobutton(self._options_shape)
        self._shape_cylinder.config(
            bg=ColourScheme.GREY, padx=5, pady=5, text="Cylinder",
            value=Translator.CYLINDER, variable=self._shape)
        self._options_dimensions = tk.LabelFrame(self._options)
        self._options_dimensions.config(
            bg=ColourScheme.GREY, padx=5, pady=5, text="Shape Dimensions")
        self._length_one = tk.StringVar()
        self._dimension_one_label = tk.Label(self._options_dimensions)
        self._dimension_one_label.config(
            bg=ColourScheme.GREY, padx=5, pady=5, text=" - ")
        self._dimension_one = tk.Entry(self._options_dimensions)
        self._dimension_one.config(
            textvariable=self._length_one)
        self._length_two = tk.StringVar()
        self._dimension_two_label = tk.Label(self._options_dimensions)
        self._dimension_two_label.config(
            bg=ColourScheme.GREY, padx=5, pady=5, text=" - ")
        self._dimension_two = tk.Entry(self._options_dimensions)
        self._dimension_two.config(
            textvariable=self._length_two)
        self._length_three = tk.StringVar()
        self._dimension_three_label = tk.Label(self._options_dimensions)
        self._dimension_three_label.config(
            bg=ColourScheme.GREY, padx=5, pady=5, text=" - ")
        self._dimension_three = tk.Entry(self._options_dimensions)
        self._dimension_three.config(
            textvariable=self._length_three)
        self._options_col_paper = tk.Label(self._options)
        self._options_col_paper.config(
            bg=ColourScheme.GREY, font="helvetica 10 bold", pady=2,
            text="Wrapping Paper")
        self._options_paper = tk.LabelFrame(self._options)
        self._options_paper.config(
            bg=ColourScheme.GREY, padx=5, pady=5,
            text="Wrapping Paper Type")
        self._paper = tk.StringVar()
        self._paper_cheap = tk.Radiobutton(self._options_paper)
        self._paper_cheap.config(
            bg=ColourScheme.GREY, padx=5, pady=5, text="Cheap",
            value=Translator.CHEAP_WRAPPING, variable=self._paper)
        self._paper_expensive = tk.Radiobutton(self._options_paper)
        self._paper_expensive.config(
            bg=ColourScheme.GREY, padx=5, pady=5, text="Expensive",
            value=Translator.EXPENSIVE_WRAPPING, variable=self._paper)
        self._options_colour = tk.LabelFrame(self._options)
        self._options_colour.config(
            bg=ColourScheme.GREY, padx=5, pady=5,
            text="Wrapping Paper Colour")
        self._colour = tk.StringVar()
        self._colour_selection = ttk.Combobox(self._options_colour)
        self._colour_selection.config(
            textvariable=self._colour)
        self._colour_selection["values"] = [
            Translator.translate_colour(WrappingPaper.PRESET_DARK_SLATE_GREY),
            Translator.translate_colour(WrappingPaper.PRESET_DEEP_SKY_BLUE),
            Translator.translate_colour(WrappingPaper.PRESET_GOLD),
            Translator.translate_colour(WrappingPaper.PRESET_LIGHT_SEA_GREEN),
            Translator.translate_colour(WrappingPaper.PRESET_PURPLE),
            Translator.translate_colour(WrappingPaper.PRESET_VIOLET_RED)]
        self._colour_selection["state"] = "readonly"
        self._colour_black_disclaimer = tk.Label(self._options_colour)
        self._colour_black_disclaimer.config(
            bg=ColourScheme.GREY, fg=ColourScheme.BLACK,
            font="helvetica 10 bold", pady=5, text=" ", justify="left")
        self._options_col_additional = tk.Label(self._options)
        self._options_col_additional.config(
            bg=ColourScheme.GREY, font="helvetica 10 bold", pady=2,
            text="Additional")
        self._options_bow = tk.LabelFrame(self._options)
        self._options_bow.config(
            bg=ColourScheme.GREY, padx=5, pady=5, text="Bow")
        self._bow = tk.IntVar()
        self._bow_addition = tk.Checkbutton(self._options_bow)
        self._bow_addition.config(
            bg=ColourScheme.GREY, padx=5, pady=5, text="Add Bow",
            variable=self._bow)
        self._options_giftcard = tk.LabelFrame(self._options)
        self._options_giftcard.config(
            bg=ColourScheme.GREY, padx=5, pady=5, text="Gift Card")
        self._giftcard = tk.IntVar()
        self._giftcard_addition = tk.Checkbutton(self._options_giftcard)
        self._giftcard_addition.config(
            bg=ColourScheme.GREY, padx=5, pady=5, text="Add Gift Card",
            variable=self._giftcard)
        self._giftcard_message_label = tk.Label(self._options_giftcard)
        self._giftcard_message_label.config(
            bg=ColourScheme.GREY, padx=5, pady=5, text="Message ")
        self._giftcard_message = tk.StringVar()
        self._giftcard_message_entry = tk.Entry(self._options_giftcard)
        self._giftcard_message_entry.config(
            textvariable=self._giftcard_message)
        self._options_quote_id = tk.LabelFrame(self._options)
        self._options_quote_id.config(
            bg=ColourScheme.GREY, padx=5, pady=5,
            text="Quote Identification")
        self._id_name_label = tk.Label(self._options_quote_id)
        self._id_name_label.config(
            bg=ColourScheme.GREY, padx=5, pady=5, text="Quote Name ")
        self._quote_name = tk.StringVar()
        self._id_name = tk.Entry(self._options_quote_id)
        self._id_name.config(
            textvariable=self._quote_name)

    def _construct_footer(self) -> None:
        self._footer = tk.Frame(self)
        self._footer.config(
            bg=ColourScheme.WHITE, padx=5, pady=5)
        self._footer_save = tk.Button(self._footer)
        self._footer_save.config(
            bg=ColourScheme.DARK_MINT_GREEN, borderwidth=1,
            fg=ColourScheme.WHITE, font="helvetica 10 bold",
            highlightthickness=1, highlightcolor=ColourScheme.GREY,
            padx=10, pady=3, text="Save")
        self._footer_cancel = tk.Button(self._footer)
        self._footer_cancel.config(
            bg=ColourScheme.WHITE, borderwidth=1,
            fg=ColourScheme.DARK_MINT_GREEN, font="helvetica 10 bold",
            highlightthickness=1, highlightcolor=ColourScheme.GREY,
            padx=10, pady=3, text="Cancel")

    def _actions(self) -> None:
        self._shape_cube.config(
            command=lambda: [
                self._preview_pane.preview_cube_shape(),
                self._handle_dimension_display_change()])
        self._shape_cuboid.config(
            command=lambda: [
                self._preview_pane.preview_cuboid_shape(),
                self._handle_dimension_display_change()])
        self._shape_cylinder.config(
            command=lambda: [
                self._preview_pane.preview_cylinder_shape(),
                self._handle_dimension_display_change()])
        self._paper_cheap.config(
            command=lambda: [
                self._preview_pane.preview_cheap_pattern(),
                self._handle_colour_check()])
        self._paper_expensive.config(
            command=lambda: [
                self._preview_pane.preview_expensive_pattern(),
                self._handle_colour_check()])
        self._colour_selection.bind(
            "<<ComboboxSelected>>", lambda event: [
                self._handle_colour_selection_change(event),
                self._handle_colour_check()])
        self._footer_cancel.config(
            command=self._handle_cancel_button)
        self._footer_save.config(
            command=self._handle_save_button)

    def _track(self) -> None:
        self._quote_name.trace("w", self._handle_callback_quote_update)
        self._length_one.trace("w", self._handle_callback_quote_update)
        self._length_two.trace("w", self._handle_callback_quote_update)
        self._length_three.trace("w", self._handle_callback_quote_update)
        self._shape.trace("w", self._handle_callback_quote_update)
        self._paper.trace("w", self._handle_callback_quote_update)
        self._colour.trace("w", self._handle_callback_quote_update)
        self._bow.trace("w", self._handle_callback_quote_update)
        self._giftcard.trace("w", self._handle_callback_quote_update)
        self._giftcard_message.trace("w", self._handle_callback_quote_update)

    def _display(self) -> None:
        self._header.pack(
            anchor="w", fill="x", side="top")
        self._preview_pane.pack(
            anchor="nw", fill="x", side="top")
        self._footer.pack(
            anchor="e", fill="x", side="bottom")
        self._footer_save.pack(
            anchor="e", side="right")
        self._footer_cancel.pack(
            anchor="e", padx=10, side="right")
        self._options.pack(
            anchor="nw", expand=True, fill="both", side="left")
        self._options_col_shape.grid(
            column=0, row=0, padx=5, pady=5)
        self._options_shape.grid(
            column=0, row=1, padx=5, pady=5, sticky="nesw")
        self._shape_cube.grid(
            column=0, row=0, padx=5, pady=5)
        self._shape_cuboid.grid(
            column=1, row=0, padx=5, pady=5)
        self._shape_cylinder.grid(
            column=2, row=0, padx=5, pady=5)
        self._options_dimensions.grid(
            column=0, row=2, padx=5, pady=5, sticky="nesw")
        self._dimension_one_label.grid(
            column=0, row=0, padx=5, pady=5)
        self._dimension_one.grid(
            column=1, row=0, padx=5, pady=5)
        self._dimension_two_label.grid(
            column=0, row=1, padx=5, pady=5)
        self._dimension_two.grid(
            column=1, row=1, padx=5, pady=5)
        self._dimension_three_label.grid(
            column=0, row=2, padx=5, pady=5)
        self._dimension_three.grid(
            column=1, row=2, padx=5, pady=5)
        self._options_paper.grid(
            column=1, row=1, padx=5, pady=5, sticky="nesw")
        self._paper_cheap.grid(
            column=0, row=0, padx=5, pady=5)
        self._paper_expensive.grid(
            column=1, row=0, padx=5, pady=5)
        self._options_colour.grid(
            column=1, row=2, padx=5, pady=5, sticky="nesw")
        self._colour_selection.grid(
            column=0, row=0, padx=5, pady=5, sticky="nesw")
        self._colour_black_disclaimer.grid(
            column=0, row=1, padx=5, pady=5, sticky="nesw")
        self._options_col_paper.grid(
            column=1, row=0, padx=5, pady=5)
        self._options_col_additional.grid(
            column=2, row=0, padx=5, pady=5)
        self._options_bow.grid(
            column=2, row=1, padx=5, pady=5, sticky="nesw")
        self._bow_addition.grid(
            column=0, row=0, padx=5, pady=5)
        self._options_giftcard.grid(
            column=2, row=2, padx=5, pady=5, sticky="nesw")
        self._giftcard_addition.grid(
            column=0, row=0, padx=5, pady=5)
        self._giftcard_message_label.grid(
            column=0, row=1, padx=5, pady=5)
        self._giftcard_message_entry.grid(
            column=1, row=1, padx=5, pady=5)
        self._options_quote_id.grid(
            column=0, row=3, columnspan=3, padx=5, pady=5, sticky="nesw")
        self._id_name_label.grid(
            column=0, row=0, padx=5, pady=5)
        self._id_name.grid(
            column=1, row=0, padx=5, pady=5)

    def _handle_dimension_display_change(self) -> None:
        if self._shape.get() == Translator.CUBE:
            self._dimension_one_label.config(
                text="Length (cm)   ")
            self._dimension_two_label.config(
                text=" ")
            self._dimension_two.config(
                state="disabled")
            self._dimension_three_label.config(
                text=" ")
            self._dimension_three.config(
                state="disabled")
        elif self._shape.get() == Translator.CUBOID:
            self._dimension_one_label.config(
                text="Width (cm)   ")
            self._dimension_two_label.config(
                text="Height (cm)   ")
            self._dimension_two.config(
                state="normal")
            self._dimension_three_label.config(
                text="Depth (cm)   ")
            self._dimension_three.config(
                state="normal")
        elif self._shape.get() == Translator.CYLINDER:
            self._dimension_one_label.config(
                text="Radius (cm)   ")
            self._dimension_two_label.config(
                text="Depth (cm)   ")
            self._dimension_two.config(
                state="normal")
            self._dimension_three_label.config(
                text=" ")
            self._dimension_three.config(
                state="disabled")

    def _handle_colour_selection_change(self, event: tk.Event, /) -> None:
        self._preview_pane.set_colour_displayed(
            Translator.translate_colour(
                self._colour.get(), human_readable=False))
        if self._paper.get() == Translator.CHEAP_WRAPPING:
            self._preview_pane.preview_cheap_pattern()
        elif self._paper.get() == Translator.EXPENSIVE_WRAPPING:
            self._preview_pane.preview_expensive_pattern()

    def _handle_colour_check(self) -> None:
        if self._preview_pane.get_colour_displayed() == "#000000":
            self._colour_black_disclaimer.config(
                text=(
                    "Please Note:\n"
                    + "   Black is not a wrapping\n   paper colour option."))
        else:
            self._colour_black_disclaimer.config(text=" ")

    def _handle_callback_quote_update(self, var, index, mode) -> int:
        ready_to_calculate: bool = True
        the_shape: PresentType = Translator.translate_present_type(
            shape=self._shape.get(),
            length_one=self._length_one.get(),
            length_two=self._length_two.get(),
            length_three=self._length_three.get())
        the_paper: WrappingPaper = Translator.translate_wrapping_paper_type(
            paper=self._paper.get(),
            colour=self._preview_pane.get_colour_displayed())
        the_gift_card: GiftCard = Translator.translate_gift_card(
            gift_card=self._giftcard.get(),
            message=self._giftcard_message.get())
        the_bow: Bow = Translator.translate_bow(bow=self._bow.get())
        if (not the_shape) or (not the_paper):
            ready_to_calculate = False
            return 1
        if ready_to_calculate:
            self._the_quote = Quote(
                quote_title=self._quote_name.get(),
                present_type=the_shape,
                wrapping_paper=the_paper,
                gift_card=the_gift_card,
                bow=the_bow)
            self._preview_pane.set_quote_title(
                self._the_quote.calculate_price(),
                self._quote_name.get())
            self._preview_pane.set_quote_shape(
                the_shape)
        if self._preview_pane.get_colour_displayed() == "#000000":
            return 2
        if Translator.check_present_lengths(the_shape):
            return 3
        if the_shape.get_recommended_area() <= 0:
            return 3
        return 0

    def _handle_cancel_button(self) -> None:
        self._avoid_message_box_exit = True
        self.destroy()

    def _handle_save_button(self) -> None:
        self._avoid_message_box_exit = True
        if not self._check_quote():
            self._save_quote()
            self.destroy()

    def _check_quote(self) -> int:
        if (value := self._handle_callback_quote_update(None, None, None)):
            if value == 1:
                tkmsg.showerror(
                    "Quote Error",
                    "This quote is not complete.")
            elif value == 2:
                tkmsg.showerror(
                    "Quote Error",
                    "Invalid wrapping paper colour within the quote..")
            elif value == 3:
                tkmsg.showerror(
                    "Quote Error",
                    "Invalid dimensions provided for present.")
            return 1
        return 0

    def _load_quote(self) -> None:
        self._length_one.set("0")
        self._length_two.set("0")
        self._length_three.set("0")
        if not self._new_quote:
            self._quote_name.set(self._quote_list[self._quote_index].title)
            if isinstance(self._quote_list[self._quote_index].present,
                          Cube):
                self._shape.set(Translator.CUBE)
                self._preview_pane.preview_cube_shape()
                self._length_one.set(
                    str(self._quote_list[
                            self._quote_index].present.get_length()))
            elif isinstance(self._quote_list[self._quote_index].present,
                            Cuboid):
                self._shape.set(Translator.CUBOID)
                self._preview_pane.preview_cuboid_shape()
                self._length_one.set(
                    str(self._quote_list[
                            self._quote_index].present.get_width()))
                self._length_two.set(
                    str(self._quote_list[
                            self._quote_index].present.get_height()))
                self._length_three.set(
                    str(self._quote_list[
                            self._quote_index].present.get_depth()))
            elif isinstance(self._quote_list[self._quote_index].present,
                            Cylinder):
                self._shape.set(Translator.CYLINDER)
                self._preview_pane.preview_cylinder_shape()
                self._length_one.set(
                    str(self._quote_list[
                            self._quote_index].present.get_radius()))
                self._length_two.set(
                    str(self._quote_list[
                            self._quote_index].present.get_depth()))
            self._preview_pane.set_colour_displayed(
                self._quote_list[
                    self._quote_index].wrapping_paper.get_colour())
            self._colour.set(WrappingPaper.colours[
                self._preview_pane.get_colour_displayed()])
            if isinstance(self._quote_list[self._quote_index].wrapping_paper,
                          CheapWrappingPaper):
                self._paper.set(Translator.CHEAP_WRAPPING)
                self._preview_pane.preview_cheap_pattern()
            elif isinstance(self._quote_list[self._quote_index].wrapping_paper,
                            ExpensiveWrappingPaper):
                self._paper.set(Translator.EXPENSIVE_WRAPPING)
                self._preview_pane.preview_expensive_pattern()
            if isinstance(self._quote_list[self._quote_index].bow,
                          Bow):
                self._bow.set(1)
            if isinstance(self._quote_list[self._quote_index].gift_card,
                          GiftCard):
                self._giftcard.set(1)
                self._giftcard_message.set(
                    self._quote_list[
                        self._quote_index].gift_card.get_message())
            self._handle_dimension_display_change()

    def _save_quote(self) -> None:
        if not self._new_quote:
            self._quote_list[self._quote_index].title = (
                Translator.check_quote_title(self._quote_name.get()))
            del self._quote_list[self._quote_index].present
            self._quote_list[self._quote_index].present = (
                Translator.translate_present_type(
                    shape=self._preview_pane.get_shape_displayed(),
                    length_one=self._length_one.get(),
                    length_two=self._length_two.get(),
                    length_three=self._length_three.get()))
            del self._quote_list[self._quote_index].wrapping_paper
            self._quote_list[self._quote_index].wrapping_paper = (
                Translator.translate_wrapping_paper_type(
                    paper=self._preview_pane.get_pattern_displayed(),
                    colour=self._preview_pane.get_colour_displayed()))
            if isinstance(self._quote_list[self._quote_index].bow, Bow):
                del self._quote_list[self._quote_index].bow
            self._quote_list[self._quote_index].bow = (
                Translator.translate_bow(bow=self._bow.get()))
            if isinstance(self._quote_list[self._quote_index].gift_card,
                          GiftCard):
                del self._quote_list[self._quote_index].gift_card
            self._quote_list[self._quote_index].gift_card = (
                Translator.translate_gift_card(
                    gift_card=self._giftcard.get(),
                    message=self._giftcard_message.get()))
        else:
            self._quote_list.append(
                Quote(
                    quote_title=Translator.check_quote_title(
                        self._quote_name.get()),
                    present_type=Translator.translate_present_type(
                        shape=self._preview_pane.get_shape_displayed(),
                        length_one=self._length_one.get(),
                        length_two=self._length_two.get(),
                        length_three=self._length_three.get()),
                    wrapping_paper=Translator.translate_wrapping_paper_type(
                        paper=self._preview_pane.get_pattern_displayed(),
                        colour=self._preview_pane.get_colour_displayed()),
                    gift_card=Translator.translate_gift_card(
                        gift_card=self._giftcard.get(),
                        message=self._giftcard_message.get()),
                    bow=Translator.translate_bow(
                        bow=self._bow.get())))

    def destroy(self) -> None:
        if not self._avoid_message_box_exit:
            result = tkmsg.askyesnocancel(
                "Save Quote?",
                "Would you want save the current quote?")
            if result:
                if self._check_quote():
                    return
                self._save_quote()
            elif result is None:
                return
        __class__.window_running_check = False
        self.master.update()
        return super().destroy()


class MainWindow(tk.Tk):

    def __init__(self) -> None:
        super().__init__()
        self.minsize(800, 600)
        self.title(f"Main Window | {APPLICATION_NAME}")
        self._order_count: int = 1
        self._order = Order(self._order_count)
        self._ask_export: bool = True
        self._selected_index: int = -1
        self._currently_editing_index: int = -1
        self._construct()
        self._actions()
        self._display()

    def _construct(self) -> None:
        self._construct_header()
        self._construct_sidebar()
        self._construct_quote_viewer()

    def _construct_header(self) -> None:
        self._header = WindowHeader(self)
        self._header.set_title("Current quotes for this order.")

    def _construct_sidebar(self) -> None:
        self._sidebar = tk.Frame(self)
        self._sidebar.config(
            bg=ColourScheme.WHITE, padx=15, pady=15, width=100)
        self._sidebar_quote_actions = tk.Label(self._sidebar)
        self._sidebar_quote_actions.config(
            bg=ColourScheme.WHITE, font="helvetica 11 bold",
            text="Quote actions")
        self._sidebar_add_quote = tk.Button(self._sidebar)
        self._sidebar_add_quote.config(
            bg=ColourScheme.WHITE, borderwidth=0,
            fg=ColourScheme.DARK_MINT_GREEN, font="helvetica 10 bold",
            text="Add quote")
        self._sidebar_edit_quote = tk.Button(self._sidebar)
        self._sidebar_edit_quote.config(
            bg=ColourScheme.WHITE, borderwidth=0,
            fg=ColourScheme.DARK_MINT_GREEN, font="helvetica 10 bold",
            text="Edit quote")
        self._sidebar_del_quote = tk.Button(self._sidebar)
        self._sidebar_del_quote.config(
            bg=ColourScheme.WHITE, borderwidth=0,
            fg=ColourScheme.DARK_MINT_GREEN, font="helvetica 10 bold",
            text="Delete quote")
        self._sidebar_actions_seperator = tk.Frame(self._sidebar)
        self._sidebar_actions_seperator.config(
            bg=ColourScheme.WHITE, height=20)
        self._sidebar_order_actions = tk.Label(self._sidebar)
        self._sidebar_order_actions.config(
            bg=ColourScheme.WHITE, font="helvetica 11 bold",
            text="Order actions")
        self._sidebar_export_order = tk.Button(self._sidebar)
        self._sidebar_export_order.config(
            bg=ColourScheme.WHITE, borderwidth=0,
            fg=ColourScheme.DARK_MINT_GREEN, font="helvetica 10 bold",
            text="Export order")
        self._sidebar_new_order = tk.Button(self._sidebar)
        self._sidebar_new_order.config(
            bg=ColourScheme.WHITE, borderwidth=0,
            fg=ColourScheme.DARK_MINT_GREEN, font="helvetica 10 bold",
            text="New order")
        self._sidebar_checkout = tk.Button(self._sidebar)
        self._sidebar_checkout.config(
            bg=ColourScheme.WHITE, borderwidth=0,
            fg=ColourScheme.DARK_MINT_GREEN, font="helvetica 10 bold",
            text="Checkout")
        self._sidebar_version = tk.Label(self._sidebar)
        self._sidebar_version.config(
            bg=ColourScheme.WHITE, font="helvetica 9", text="Version")
        self._sidebar_version_number = tk.Label(self._sidebar)
        self._sidebar_version_number.config(
            bg=ColourScheme.WHITE, font="helvetica 9",
            text=APPLICATION_VERSION)

    def _construct_quote_viewer(self) -> None:
        self._quotes_frame = tk.Frame(self)
        self._quotes_frame.config(bg=ColourScheme.GREY, padx=15, pady=15)
        self._order_details = tk.StringVar()
        self._order_summary = tk.Label(self._quotes_frame)
        self._order_summary.config(
            bg=ColourScheme.GREY, borderwidth=0, fg=ColourScheme.BLACK,
            font="helvetica 11 bold", textvariable=self._order_details)
        self._order_details.set(
            f"Order {self._order.get_order_number()}     "
            + f"      {len(self._order.quotes)} Quote(s)     "
            + f"      £{self._order.calculate_total_price():.2f}")
        self._quotes_listbox = tk.Listbox(self._quotes_frame)
        self._quotes_listbox.config(font="helvetica 10")
        self._quote_preview_pane = QuoteSummaryPane(self._quotes_frame)

    def _actions(self) -> None:
        self._sidebar_add_quote.config(
            command=lambda: self._handle_add_quote())
        self._sidebar_edit_quote.config(
            command=lambda: self._handle_edit_quote())
        self._sidebar_del_quote.config(
            command=lambda: self._handle_delete_quote())
        self._sidebar_export_order.config(
            command=lambda: self._handle_export_order())
        self._sidebar_new_order.config(
            command=lambda: self._handle_new_order())
        self._sidebar_checkout.config(
            command=lambda: self._handle_checkout())
        self._quotes_listbox.bind(
            "<<ListboxSelect>>", self._handle_quote_selection_change)

    def _display(self) -> None:
        self._header.pack(
            anchor="w", fill="x", side="top")
        self._sidebar.pack(
            anchor="nw", fill="y", side="left")
        self._sidebar_quote_actions.pack(
            anchor="nw", side="top")
        self._sidebar_add_quote.pack(
            anchor="nw", side="top")
        self._sidebar_edit_quote.pack(
            anchor="nw", side="top")
        self._sidebar_del_quote.pack(
            anchor="nw", side="top")
        self._sidebar_actions_seperator.pack(
            anchor="nw", side="top")
        self._sidebar_order_actions.pack(
            anchor="nw", side="top")
        self._sidebar_export_order.pack(
            anchor="nw", side="top")
        self._sidebar_new_order.pack(
            anchor="nw", side="top")
        self._sidebar_checkout.pack(
            anchor="nw", side="top")
        self._sidebar_version_number.pack(
            anchor="nw", side="bottom")
        self._sidebar_version.pack(
            anchor="nw", side="bottom")
        self._quotes_frame.pack(
            anchor="nw", expand=True, fill="both", side="top")
        self._quote_preview_pane.pack(
            anchor="nw", fill="x", side="bottom")
        self._order_summary.pack(
            anchor="nw", side="top")
        self._quotes_listbox.pack(
            anchor="nw", expand=True, fill="both", pady=10, side="top")

    def _handle_quote_update(self) -> None:
        self._ask_export = True
        self._quotes_listbox.delete(0, "end")
        for i in range(len(self._order.quotes)):
            self._quotes_listbox.insert(
                i, f" {str(self._order.quotes[i])}")
        self._order_details.set(
            f"Order {self._order.get_order_number()}     "
            + f"      {len(self._order.quotes)} Quote(s)     "
            + f"      £{self._order.calculate_total_price():.2f}")

    def _handle_add_quote(self) -> None:
        if not QuoteConfigurationWindow.window_running_check:
            quote_config_window = QuoteConfigurationWindow(
                self, True, self._order.quotes, len(self._order.quotes))
        else:
            QuoteConfigurationWindow.raise_window_running_message()

    def _handle_edit_quote(self) -> None:
        try:
            if self._selected_index != -1:
                if not QuoteConfigurationWindow.window_running_check:
                    self._currently_editing_index = self._selected_index
                    quote_config_window = QuoteConfigurationWindow(
                        self, False, self._order.quotes, self._selected_index)
                else:
                    QuoteConfigurationWindow.raise_window_running_message()
            else:
                raise IndexError
        except IndexError:
            tkmsg.showerror(
                "Selection Error",
                "No quote selected to edit.")

    def _handle_delete_quote(self) -> None:
        try:
            if (self._selected_index == self._currently_editing_index
                    and self._selected_index != -1):
                tkmsg.showerror(
                    "Deletion Error",
                    "You cannot delete the quote you are currently editing.")
            else:
                del self._order.quotes[self._selected_index]
        except IndexError:
            tkmsg.showerror(
                "Selection Error",
                "No quote selected to delete.")
        self._handle_quote_update()
        self._quote_preview_pane.clear_preview()
        self._selected_index = -1

    def _handle_export_order(self) -> None:
        if len(self._order.quotes) == 0:
            tkmsg.showerror(
                "Export Error",
                "You cannot export an empty order.")
            return
        if not self._order.export_order():
            self._ask_export = False
            tkmsg.showinfo(
                "Quotes Exported",
                f"Quotes have been successfully exported to:\n"
                + f"{os.path.dirname(os.path.abspath(__file__))}")
        else:
            tkmsg.showerror(
                "Export Error",
                f"Failed to export quotes.\n"
                + "Please ensure the program has write access to the "
                + "relative directory.")

    def _handle_new_order(self) -> None:
        if self._ask_export and len(self._order.quotes) > 0:
            result = tkmsg.askyesno(
                "New Order",
                "Export the quotes before starting a new order?")
            if result:
                self._order.export_order()
        del self._order
        self._order_count += 1
        self._order = Order(self._order_count)
        self._order_details.set(
            f"Order {self._order.get_order_number()}     "
            + f"      {len(self._order.quotes)} Quote(s)     "
            + f"      £{self._order.calculate_total_price():.2f}")
        self.update()
        self._ask_export = True

    def _handle_checkout(self) -> None:
        if not QuoteConfigurationWindow.window_running_check:
            tkmsg.showwarning(
                "Checkout Warning",
                "The checkout procedure has not been implemented "
                + "as this is a proof of concept.\n\n"
                + "The order will now be exported to the relative directory "
                + "and a new order will be started to simulate the "
                + "checkout process.\n\n"
                + "If the order is empty, there will not be an exported file.")
            if len(self._order.quotes) > 0:
                self._handle_export_order()
            self._ask_export = False
            self._handle_new_order()
        else:
            tkmsg.showerror(
                "Checkout Error",
                "Please make sure that the quote configuration window is "
                + "closed before checking out.")

    def _handle_quote_selection_change(self, event: tk.Event, /) -> None:
        selection = event.widget.curselection()
        try:
            self._selected_index = selection[0]
        except IndexError:
            return
        self._quote_preview_pane.set_quote_title(
            self._order.quotes[self._selected_index].calculate_price(),
            self._order.quotes[self._selected_index].title)
        self._quote_preview_pane.set_quote_shape(
            self._order.quotes[self._selected_index].present)
        self._quote_preview_pane.set_quote_paper(
            self._order.quotes[self._selected_index].wrapping_paper)
        self._quote_preview_pane.set_additional_options(
            self._order.quotes[self._selected_index].bow,
            self._order.quotes[self._selected_index].gift_card)

    def destroy(self) -> None:
        if not QuoteConfigurationWindow.window_running_check:
            if self._ask_export and len(self._order.quotes) > 0:
                result = tkmsg.askyesnocancel(
                    "Export Quotes?",
                    "Export the quotes before exiting application?")
                if result:
                    self._order.export_order()
                elif result is None:
                    return
            return super().destroy()
        else:
            tkmsg.showinfo(
                "Window Instances Information",
                "Please close all windows before exiting the application.")

    def show(self) -> None:
        self.mainloop()

    def update(self) -> None:
        self._handle_quote_update()
        self._quote_preview_pane.clear_preview()
        self._ask_export = True
        if not QuoteConfigurationWindow.window_running_check:
            self._currently_editing_index = -1
        return super().update()


def main() -> None:
    window = MainWindow()
    window.show()


if __name__ == "__main__":
    main()
