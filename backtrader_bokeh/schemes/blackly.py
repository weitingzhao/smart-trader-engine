from .scheme import Scheme


class Blackly(Scheme):
    def _set_params(self):
        super()._set_params()

        self.barup = '#ff9896'
        self.bardown = '#98df8a'
        self.volup = '#ff9896'
        self.voldown = '#98df8a'
        self.barup_wick = self.barup
        self.bardown_wick = self.bardown
        self.barup_outline = self.barup
        self.bardown_outline = self.bardown

        self.crosshair_line_color = '#999999'

        self.legend_background_color = '#3C3F41'
        self.legend_text_color = 'lightgrey'

        self.background_fill = '#222222'
        self.body_background_color = '#2B2B2B'
        self.border_fill = '#3C3F41'
        self.legend_click = 'hide'  # or 'mute'
        self.axis_line_color = 'darkgrey'
        self.tick_line_color = self.axis_line_color
        self.grid_line_color = '#444444'
        self.axis_text_color = 'lightgrey'
        self.plot_title_text_color = 'darkgrey'
        self.axis_label_text_color = 'darkgrey'

        self.tab_active_background_color = '#666666'
        self.tab_active_color = '#bbbbbb'

        self.table_color_even = '#404040'
        self.table_color_odd = '#333333'
        self.table_header_color = '#707070'

        self.tooltip_background_color = '#4C4F51'
        self.tooltip_text_label_color = '#848EFF'
        self.tooltip_text_value_color = '#aaaaaa'

        self.tag_pre_background_color = '#222222'
        self.tag_pre_text_color = 'lightgrey'
