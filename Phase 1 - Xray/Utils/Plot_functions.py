import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.io as pio
pio.templates.default = "plotly_white"


# * plotly confusion matrix
def plotly_ROC_curve(
    ytrue: pd.Series,
    classes: list,
    predictions: np.array,
    auto_size: bool = True,
    width: int = 800,
    height: int = 500,
):
    """_summary_
    plot ROC curve for multiclass classification
    args:
        classes: pandas series with the true classes
        predictions: numpy array which is the predictions probabilities for each class
    returns:
        plotly figure for ROC curve for multiclass classification
    """
    # * impots
    import plotly.graph_objects as go
    from sklearn.metrics import roc_curve, auc

    # * data
    # classes_dict = {classes.unique()[i] : i for i in range(len(classes.unique()))}
    classes_dict = {classes[i]: i for i in range(len(classes))}
    y_test = np.array(ytrue.map(classes_dict))

    pred_prob = predictions  # * predictions probabilities
    fpr = {}  # * false positive rate
    tpr = {}  # * true positive rate
    roc_auc = {}  # * area under the curve
    n_class = predictions.shape[1]  # * number of classes

    # * calculate ROC curve and AUC for each class
    for i in range(n_class):
        fpr[i], tpr[i], _ = roc_curve(y_test, pred_prob[:, i], pos_label=i)
        roc_auc[i] = auc(fpr[i], tpr[i])

    # * plot ROC curve
    fig = go.Figure()
    for i in range(n_class):
        name = f"{list(classes_dict.keys())[i]} (AUC={round(roc_auc[i], 3)})"
        fig.add_trace(
            go.Scatter(x=fpr[i], y=tpr[i], name=name, mode="lines", fill="tonexty")
        )

    fig.add_trace(
        go.Scatter(
            x=[0, 1],
            y=[0, 1],
            name="Chance level (AUC = 0.5)",
            mode="lines",
            line=dict(color="black"),
            fill="none",
        )
    )

    # * prettify
    fig.update_layout(
        xaxis_title="False Positive Rate",
        yaxis_title="True Positive Rate",
        yaxis=dict(
            scaleanchor="x",
            scaleratio=1,
        ),
        xaxis=dict(constrain="domain"),
    )
    fig.update_layout(title_text="Multiclass ROC curve", title_x=0.25)
    fig.update_layout(
        autosize=False,
        width=800,
        height=500,
        margin=dict(l=10, r=10, b=25, t=50, pad=1),
    )
    fig.update_layout(yaxis_range=[0, 1])
    if auto_size == False:
        fig.update_layout(
            autosize=False,
            width=width,
            height=height,
        )
    fig.show()


# * matplotlib ROC curve
def matplotlib_ROC_curve(ytrue: pd.Series, classes: list, predictions: np.array):
    """_summary_
     Plot ROC curve for multiclass classification using matplotlib
    Args:
        classes (pd.Series): pandas series with the true classes
        predictions (np.array): numpy array which is the predictions probabilities for each class
    Returns:
        matplotlib figure for ROC curve for multiclass classification
    """
    # * imports
    from sklearn.metrics import roc_curve, auc
    import seaborn as sns

    # * data
    classes_dict = {classes[i]: i for i in range(len(classes))}
    y_test = np.array(ytrue.map(classes_dict))

    pred_prob = predictions
    fpr = {}
    tpr = {}
    thresh = {}
    roc_auc = {}
    n_class = predictions.shape[1]

    # * calculate ROC curve and AUC for each class
    for i in range(n_class):
        fpr[i], tpr[i], thresh[i] = roc_curve(y_test, pred_prob[:, i], pos_label=i)
        roc_auc[i] = auc(fpr[i], tpr[i])

    # * plot ROC curve
    fig, ax = plt.subplots(figsize=(8, 6))
    for x in np.arange(n_class):
        ax.plot(
            fpr[x],
            tpr[x],
            linestyle="-",
            label=f"{list(classes_dict.keys())[x]} - ROC Curve, (AUC = {round(roc_auc[x],3)})",
        )
    ax.plot([0, 1], [0, 1], "k--",) #label="chance level - ROC Curve, (AUC = 0.5)")

    # * prettify
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive rate")
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.legend(loc="best")
    ax.grid(alpha=0.4)
    ax.legend(loc="lower right")
    ax.set_title('Receiver operating characteristic example')
    #ax.grid(False)
    # fig.savefig('Multiclass ROC',dpi=250);
    sns.despine()
    plt.show()


# * plotly bar chart
def plotly_bar_chart(
    classes: pd.Series,
    predicted_classes: pd.Series,
    ymin: int = 0,
    ymax: int = 102,
    accuacy: bool = True,
    precision: bool = True,
    recall: bool = True,
    specificity: bool = True,
    sensitivity: bool = True,
    f1_score: bool = True,
    auto_size: bool = True,
    width: int = 800,
    height: int = 500,
):
    """_summary_
    Plot a bar chart with the metrics for each class

    Args:
        classes (pd.Series): pandas series with the true classes
        predicted_classes (pd.Series): pandas series with the predicted classes
        ymin (int, optional): minimum value for the y axis. Defaults to 0.
        ymax (int, optional): minimum value for the y axis. Defaults to 102.
        accuacy (bool, optional): whether to plot the accuracy metric. Defaults to True.
        precision (bool, optional): whether to plot the precision metric. Defaults to True.
        recall (bool, optional): whether to plot the recall metric. Defaults to True.
        specificity (bool, optional): whether to plot the specificity metric. Defaults to True.
        sensitivity (bool, optional): whether to plot the sensitivity metric. Defaults to True.
        f1_score (bool, optional): whether to plot the f1_score metric. Defaults to True.

    Returns:
        plotly bar chart with the metrics for each class
    """

    from sklearn.metrics import multilabel_confusion_matrix
    import plotly.graph_objects as go

    # * Creating a dictionary with the classes and their respective metrics
    class_dict = {label: i for i, label in enumerate(list(classes.unique()))}
    list_class = {
        list(class_dict.keys())[0]: {},
        list(class_dict.keys())[1]: {},
        list(class_dict.keys())[2]: {},
    }

    # * Calculating metrics
    for key, value in class_dict.items():
        tn, fp, fn, tp = multilabel_confusion_matrix(classes, predicted_classes)[
            value
        ].ravel()
        if accuacy:
            list_class[key]["accuracy"] = (tp + tn) / (tp + tn + fp + fn)
        if precision:
            list_class[key]["Precision"] = tp / (tp + fp)
        if recall:
            list_class[key]["recall"] = tp / (tp + fn)
        if specificity:
            list_class[key]["specificity"] = tn / (tn + fp)
        if sensitivity:
            list_class[key]["sensitivity"] = tp / (tp + fn)
        if f1_score:
            list_class[key]["f1_score"] = (2 * tp) / (2 * tp + fp + fn)

    # * Plotting
    fig = go.Figure()
    trace1 = go.Bar(
        x=list(list_class[list(list_class.keys())[2]].keys()),
        y=[x * 100 for x in list_class[list(list_class.keys())[2]].values()],
        name=f"{list(list_class.keys())[2]}",
    )
    trace2 = go.Bar(
        x=list(list_class[list(list_class.keys())[1]].keys()),
        y=[x * 100 for x in list_class[list(list_class.keys())[1]].values()],
        name=f"{list(list_class.keys())[1]}",
    )
    trace3 = go.Bar(
        x=list(list_class[list(list_class.keys())[0]].keys()),
        y=[x * 100 for x in list_class[list(list_class.keys())[0]].values()],
        name=f"{list(list_class.keys())[0]}",
    )
    fig.add_trace(trace1)
    fig.add_trace(trace2)
    fig.add_trace(trace3)
    fig.update_layout(title_text="Classes Metrics Bar Chart", title_x=0.45)
    fig.update_layout(yaxis_range=[ymin, ymax])
    if auto_size == False:
        fig.update_layout(
            autosize=False,
            width=width,
            height=height,
        )
    fig.show()
    print(list_class)


# * seaborn confusion matrix plot
def sns_confusion_matrix_plot(
    conf_mat: np.array, classes: list, title: str = "Confusion Matrix"
):
    """_summary_
     Plot confusion matrix using seaborn
    Args:
        conf_mat (np.array): numpy array with the confusion matrix
        classes (list): list with the classes names
    Returns:
        seaborn figure for confusion matrix
    """
    # * imports
    import warnings

    warnings.filterwarnings("ignore")
    import seaborn as sns
    import matplotlib.pyplot as plt

    # * plot
    fig, ax = plt.subplots(figsize=(8, 6))
    ax = sns.heatmap(
        conf_mat,
        annot=True,
        linewidth=0.5,
        cmap=plt.get_cmap("Blues"),
        fmt=".0f",
        xticklabels=classes,
        yticklabels=classes,
    )

    # * prettify
    ax.set_xlabel(title, fontsize=18)
    ax.set_ylabel("True Class", fontsize=16)
    ax.set_title("Predicted Class", fontsize=16)
    ax.xaxis.tick_top()

    sns.despine()
    sns.set(font_scale=1.2)
    sns.set_style("white")
    fig.show()


# * Plotly confusion matrix
def plotly_confusion_matrix_plot(
    conf_mat: np.array,
    labels: list,
    title: str = "Confusion Matrix",
    width: int = 800,
    height: int = 600,
    auto_size: bool = True,
):
    """_summary_
    Plot confusion matrix using plotly
    Args:
        conf_mat (np.array):  numpy array with the confusion matrix
        labels (list,): list with the classes names
    """
    # * imports
    import plotly.express as px

    # * plot
    fig = px.imshow(
        conf_mat,
        labels=dict(x="Actual-class", y="Predicted-class"),
        color_continuous_scale="blues",
        x=labels,
        y=labels,
        text_auto=True,
        aspect="auto",
        height=600,
        width=800,
    )
    # * prettify
    fig.update_xaxes(side="top")
    fig.update_layout(title_text=title, title_x=0.5, title_y=0.05, title_font_size=20)
    fig.update_xaxes(
        title="Actual class", title_font=dict(size=22, family="Arial", color="black")
    )
    fig.update_yaxes(
        title="Predicted class",
        title_font=dict(
            size=22,
            family="Arial",
            color="black",
        ),
    )
    fig.update_xaxes(showline=True, linewidth=2, linecolor="black", mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor="black", mirror=True)
    fig.update_layout(font=dict(color="black"))
    fig.update_layout(
        xaxis=dict(
            tickfont=dict(size=16, color="black")  # set font size  # set font color
        ),
        yaxis=dict(
            tickfont=dict(size=16, color="black")  # set font size  # set font color
        ),
    )
    fig.update_layout(font_size=15)
    if auto_size == False:
        fig.update_layout(
            autosize=False,
            width=width,
            height=height,
        )
    fig.show()


cmps = [
    "aggrnyl",
    "agsunset",
    "algae",
    "amp",
    "armyrose",
    "balance",
    "blackbody",
    "bluered",
    "blues",
    "blugrn",
    "bluyl",
    "brbg",
    "brwnyl",
    "bugn",
    "bupu",
    "burg",
    "burgyl",
    "cividis",
    "curl",
    "darkmint",
    "deep",
    "delta",
    "dense",
    "earth",
    "edge",
    "electric",
    "emrld",
    "fall",
    "geyser",
    "gnbu",
    "gray",
    "greens",
    "greys",
    "haline",
    "hot",
    "hsv",
    "ice",
    "icefire",
    "inferno",
    "jet",
    "magenta",
    "magma",
    "matter",
    "mint",
    "mrybm",
    "mygbm",
    "oranges",
    "orrd",
    "oryel",
    "oxy",
    "peach",
    "phase",
    "picnic",
    "pinkyl",
    "piyg",
    "plasma",
    "plotly3",
    "portland",
    "prgn",
    "pubu",
    "pubugn",
    "puor",
    "purd",
    "purp",
    "purples",
    "purpor",
    "rainbow",
    "rdbu",
    "rdgy",
    "rdpu",
    "rdylbu",
    "rdylgn",
    "redor",
    "reds",
    "solar",
    "spectral",
    "speed",
    "sunset",
    "sunsetdark",
    "teal",
    "tealgrn",
    "tealrose",
    "tempo",
    "temps",
    "thermal",
    "tropic",
    "turbid",
    "turbo",
    "twilight",
    "viridis",
    "ylgn",
    "ylgnbu",
    "ylorbr",
    "ylorrd",
]
