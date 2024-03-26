from pathlib import Path
import pandas as pd
import plotly.express as px


def means_to_work(geoid20: str):
    csv_path = (
        Path(__file__).parent.parent.parent
        / f"data/CSV/means_to_work/{geoid20}.csv"
    )
    if not csv_path.exists():
        print(csv_path)
        return {}
    print(csv_path)
    means_to_work_df = pd.read_csv(csv_path)
    fig = px.line(
        means_to_work_df,
        x="year",
        y="value",
        color="means_to_work",
        markers=True,
        template="plotly_dark",
        # color_discrete_sequence=px.colors.qualitative.Dark2
    )
    fig.update_layout(
        xaxis=dict(type="category", title=None),
        yaxis=dict(title=None),
        # width=800,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.05,
            title="means to work",
            bgcolor="rgba(0, 0, 0, 0)",
        ),
        yaxis_range=[0, means_to_work_df["value"].max() * 1.1],
        margin=dict(l=0, r=0, t=0, b=0),
        # plot_bgcolor='rgba(0, 0, 0, 0)',
        # paper_bgcolor='rgba(0, 0, 0, 0)',
    )
    # fig.show(config={'displayModeBar': False})
    return fig
