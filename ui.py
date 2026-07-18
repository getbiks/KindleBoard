from PIL import ImageDraw

BLACK = 0
WHITE = 255


def draw_card(draw: ImageDraw.ImageDraw, x, y, w, h, title, title_font, body_font):
    """
    Draw a bordered card with a title.
    """
    draw.rounded_rectangle(
        (x, y, x + w, y + h),
        radius=8,
        outline=BLACK,
        width=2,
        fill=WHITE
    )

    draw.text(
        (x + 12, y + 10),
        title,
        fill=BLACK,
        font=title_font
    )


def draw_divider(draw: ImageDraw.ImageDraw, x1, y1, x2, y2):
    draw.line((x1, y1, x2, y2), fill=BLACK, width=1)
