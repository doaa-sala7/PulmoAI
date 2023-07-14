import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly
import plotly.io as io
import json
import numpy as np
from PIL import Image
import urllib.request


def plot_image(image_path):
    try:
        image = np.array(Image.open(image_path))
    except:
        image = np.array(Image.open(urllib.request.urlopen(image_path)))
    fig = px.imshow(
        image.astype(np.uint8),
        color_continuous_scale="gray",
    )
    fig.update_coloraxes(showscale=False)
    fig.update_layout(
        xaxis=dict(
            showticklabels=False,  # Hide x-axis tick labels
            showgrid=False,  # Hide x-axis gridlines
            zeroline=False,  # Hide x-axis zeroline
        ),
        yaxis=dict(
            showticklabels=False,  # Hide y-axis tick labels
            showgrid=False,  # Hide y-axis gridlines
            zeroline=False,  # Hide y-axis zeroline
        ),
    )
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    fig.update_layout()

    return fig


def plot_prediction(
    predictions=[0.00428376, 0.98603815, 0.00967801], image_type="Xray"
):
    fig = go.Figure()
    values = [round(i * 100, 2) for i in predictions]

    if image_type == "Xray":
        columns = ["Covid", "Normal", "Pneumonia"]
        for i in range(len(columns)):
            fig.add_trace(
                go.Bar(
                    x=[columns[i]],
                    y=[values[i]],
                    # marker=dict(color=colors[i]),  #*Assign color to the bar
                    name=columns[i],  # Add name for the legend
                    width=0.5,  # Custom bar width
                )
            )

    elif image_type == "CT":
        columns = ["Normal", "Covid", "Pneumonia"]
        fig.add_trace(go.Bar(x=[columns[1]], y=[values[1]], name=columns[1], width=0.5))
        fig.add_trace(go.Bar(x=[columns[0]], y=[values[0]], name=columns[0], width=0.5))
        fig.add_trace(go.Bar(x=[columns[2]], y=[values[2]], name=columns[2], width=0.5))

    colors = ["#3F729B", "#80B1D3", "#B0D3E3"]


    # Set y-axis range to 0-100%
    fig.update_yaxes(range=[0, 100])

    # Set the layout title and axis labels
    fig.update_layout(
        title="Model Prediction",
        xaxis_title="Class",
        yaxis_title="Prediction Score (%)",
        legend_title_text="classes",
    )
    # change plot width and height
    fig.update_layout(
        autosize=False,
        width=429.55,
        height=345,
    )

    return fig


if __name__ == "__main__":
    predictions = [0.00428376, 0.98603815, 0.00967801]
    fig = plot_prediction(predictions)
    fig.show()
