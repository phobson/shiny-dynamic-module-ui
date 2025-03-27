import string
from shiny import App, module, render, ui, reactive


@module.ui
def row_ui(label):
    return ui.layout_columns(
        ui.card(
            ui.card_header(label),
            ui.input_numeric("num_in", "Enter a Number", 2),
            ui.card_footer(ui.output_text("text_out"))
        ),
    )


@module.server
def row_server(input, output, session):
    @output
    @render.text
    def text_out():
        return f"You entered {input.num_in()}"

    return input.num_in

app_ui = ui.page_fluid(
    ui.input_slider("num_UIs", "How many numbers?", 1, 10, 2),
    ui.output_ui("dyno_ui"),
    ui.output_text("out_sum")
)


def server(input, output, session):
    text = reactive.value([])
    @render.ui
    def dyno_ui():
        letters = list(string.ascii_uppercase)
        N = input.num_UIs()

        left = []
        right = []
        for n in range(N):
            if n % 2:
                right.append(row_ui(f"row_{n+1}", f"Number {letters[n]}"))
            else:
                left.append(row_ui(f"row_{n+1}", f"Number {letters[n]}"))

        return ui.layout_columns(left, right)


    @reactive.effect
    def _():
        _out= [row_server(f"row_{n}") for n in range(1, input.num_UIs()+1)]
        text.set(_out)

    @render.text
    def out_sum():
        _sum = sum([x() for x in text()])
        return f"The sum is {_sum}"


app = App(app_ui, server)