import os
from typing import Literal

import pandas as pd
from dotenv import load_dotenv

import plotly.express as px
from plotly.figure_factory import create_distplot
import plotly.graph_objs as go


load_dotenv()
BASE_COLOR = os.getenv("BASE_COLOR", "#000060")


def unilabel_dist_plot(
    df: pd.DataFrame,
    label,
    type_=Literal[
        "histogram", "bar chart", "boxplot", "violin chart", "kde plot", "pie"
    ],
) -> go.Figure:
    """
    Generate a distribution plot for a single label in a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        label: The label/column name to plot.
        type_ (Literal["histogram", "bar chart", "boxplot", "violin chart", "kde plot", "pie"]):
            The type of plot to generate. Options are:
            - "histogram": Generate a histogram plot.
            - "bar chart": Generate a bar chart plot.
            - "boxplot": Generate a boxplot plot.
            - "violin chart": Generate a violin chart plot.
            - "kde plot": Generate a kernel density estimation plot.
            - "pie": Generate a pie chart plot.

    Returns:
        go.Figure: The generated plot as a Plotly Figure object.
    """
    fig = go.Figure()
    yaxis_title = "Count"
    xaxis_title = label

    if type_ == "histogram":
        fig.add_trace(go.Histogram(x=df[label]))
    elif type_ == "bar chart":
        fig.add_trace(
            go.Bar(x=df[label].value_counts().index, y=df[label].value_counts().values)
        )
    elif type_ == "boxplot":
        fig.add_trace(go.Box(y=df[label], boxmean=True))
    elif type_ == "violin chart":
        fig.add_trace(go.Violin(y=df[label], box_visible=True, meanline_visible=True))
        yaxis_title = label
        xaxis_title = ""
    elif type_ == "kde plot":
        if type(df[label].iloc[0]) == str:
            return "Cannot plot a KDE plot for a non-numeric column."
        fig = create_distplot(
            [df[label].dropna().values], group_labels=[label], show_hist=False
        )
        yaxis_title = "Density"
    elif type_ == "pie":
        fig.add_trace(
            go.Pie(
                labels=df[label].value_counts().index,
                values=df[label].value_counts().values,
            )
        )
        yaxis_title = ""
        xaxis_title = ""
    else:
        raise ValueError(
            "Invalid type. It must be either 'histogram', 'bar chart', 'boxplot', 'violin chart', 'kde plot', or 'pie."
        )

    fig.update_layout(
        title=f"{type_.title()} of {label.title()} Distribution",
        colorway=[BASE_COLOR],
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
    )
    return fig


def bilable_dist_plot(
    df: pd.DataFrame,
    label1,
    label2,
    type_=Literal["boxplot", "violin chart"],
) -> go.Figure:
    """
    Generate a distribution plot based on the given data and plot type.

    Args:
        df (pd.DataFrame): The input DataFrame containing the data.
        label1: The column label for the x-axis.
        label2: The column label for the y-axis.
        type_ (Literal["boxplot", "violin chart"]): The type of plot to generate.

    Returns:
        go.Figure: The generated plot as a Plotly Figure object.
    """
    fig = go.Figure()
    xaxis_title = label1
    yaxis_title = label2

    if type_ == "boxplot":
        fig.add_trace(go.Box(x=df[label1], y=df[label2], boxmean=True))
        yaxis_title = label2
        xaxis_title = label1
    elif type_ == "violin chart":
        fig.add_trace(
            go.Violin(
                x=df[label1], y=df[label2], box_visible=True, meanline_visible=True
            )
        )
        yaxis_title = label2
        xaxis_title = label1
    else:
        raise ValueError("Invalid type. It must be either 'boxplot', or 'violin chart.")
    fig.update_layout(
        title=f"{type_.title()} of {label1.title()} vs {label2.title()}",
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
    )
    return fig


def multiabel_dist_plot(
    df: pd.DataFrame,
    label1,
    label2,
    label3,
    label4=None,
) -> go.Figure:
    """
    Generate a multi-dimensional distribution plot using Plotly.

    Args:
        df (pd.DataFrame): The input DataFrame containing the data.
        label1: The column name to be plotted on the x-axis.
        label2: The column name to be used for row-wise faceting.
        label3: The column name to be used for column-wise faceting.
        label4: The column name to be used for animation frames (optional).

    Returns:
        go.Figure: The generated Plotly figure.

    """
    fig = px.histogram(
        df,
        x=label1,
        facet_row=label2,
        facet_col=label3,
        animation_frame=label4,
        title=f"{label1.title()} vs {label2.title()} vs {label3.title()}",
    )

    return fig
