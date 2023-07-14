from django.utils.html import mark_safe


class DynamicColumn:
    def __init__(self, column_name, name):
        self.column_name = column_name
        self.__name__ = ""
        self.short_description = mark_safe(name)

    def __call__(self, widget) -> str:
        number = getattr(widget, self.column_name, "-")
        if str(number).isnumeric():
            price = int(getattr(widget, "price"))
            number = int(number)
            number_str = "{:,}".format(int(number)).replace(",", " ")
            if number <= price:
                return mark_safe(
                    '<span style="color: #000;background-color:'
                    " #f7d466;border-color: #bcd0c7;"
                    ' ">%s</span>' % number_str
                )
            if number > price:
                return mark_safe(
                    '<span style="color: #000;background-color:'
                    " #66f79f;border-color: #bcd0c7;"
                    ' ">%s</span>' % number_str
                )
        return number
