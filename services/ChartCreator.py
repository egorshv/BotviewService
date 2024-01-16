import abc

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class AbstractChartCreator(abc.ABC):
    @abc.abstractmethod
    def create_line_chart(self, lines: dict, title: str) -> None:
        raise NotImplemented


class ChartCreator(AbstractChartCreator):
    def __init__(self, filename: str):
        self.filename = filename
        self.fig = go.Figure()

    def create_line_chart(self, lines: dict, title: str) -> None:
        data = pd.DataFrame(data=lines)
        self.fig = px.line(data, x='time', y='value', title=title, color='line')
        self.fig.write_image(self.filename)
