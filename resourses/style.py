from .font_weight_enum import font_weight

title_label_style = """
                   QLabel {
                       color: #FFFFFF;
                       font-size: 16px;
                       font-family: Poppins;
                       font-size: 20px;
                       padding: 5px 0px 0px 20px;
                   }
               """

profile_list_style = """
            QListWidget {
                background-color: #383838;
                border: 2px solid #2D2D2D;
            }
            QListWidget::item {
                color: #FFFFFF;
                background-color: #484848;
                border: 1px solid #2D2D2D;
                width: 180px;
                height: 43px;
                border-radius: 10px;
                font-size: 20px;
                font-family: Poppins;
                font-weight: medium;
            }
            QListWidget::item:selected {
                background-color: #717171;
            }
            QListWidget::item:selected:!active {
                background-color: #484848;
            }
            QListWidget::item:selected:active {
                background-color: #717171;
            }
        """

drag_and_drop_style = """
            QLabel {
                color: #FFFFFF;
                font-size: 18px;
                font-family: Poppins;
                background-color: #383838;
                border: 2px solid #2D2D2D;
                border-radius: 10px;
                min-width: 200px; /* Ширина */
                min-height: 200px; /* Высота */
            }
        """

checkbox_style = """
    QCheckBox {
        color: #FFFFFF;
        font-size: 18px;
        font-family: Poppins;
        background-color: #383838;
        border: 2px solid #2D2D2D;
        border-radius: 10px;
        padding: 5px; /* Отступ внутри чекбокса */
    }

    QCheckBox::indicator {
        width: 20px; /* Ширина индикатора */
        height: 20px; /* Высота индикатора */
    }
"""

log_style = """
    QTextEdit {
        background-color: #383838; 
        color: #FFFFFF; border-radius: 
        10px; border: 2px solid #2D2D2D; 
        font-size: 18px; line-height: 1;
    }
"""

def button_style(bg_color, hover_color=None, weight=None, size=None, padding=None):
    hover = hover_color if hover_color is not None else bg_color
    weight = weight if weight is not None else font_weight.NORMAL
    size = size if size is not None else ''
    padding = padding if padding is not None else ''
    return f"""
        QPushButton {{
            background-color: {bg_color};
            color: white;
            border: 1px solid #2D2D2D;
            font-family: Poppins;
            font-weight: {weight.value};
            font-size: {size}px;
            border-radius: 10px;
            padding: {padding}px;
            min-width: 47px;
            min-height: 30px;
        }}
        QPushButton:hover {{
            background-color: { hover };
        }}
    """