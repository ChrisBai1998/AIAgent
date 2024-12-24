import dash
from dash import dcc, html, Input, Output, State
import requests
import dash_bootstrap_components as dbc
import sqlite3
import webbrowser

# Initialize Dash app with Bootstrap stylesheet
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Custom CSS for a dungeon-like aesthetic
custom_css = {
    "container": {
        "backgroundColor": "#121212",
        "color": "white",
        "fontFamily": "Courier New, monospace",
        "padding": "20px",
    },
    "ca_header": {
        "color": "white",  # 修改文字颜色为白色
        "fontSize": "14px",
        "fontWeight": "bold",
        "textAlign": "left",  # 修改位置为左对齐
        "marginBottom": "10px",
        "textShadow": "0 0 10px #FFEB3B",
        "backgroundColor": "blue",  # 修改背景颜色为蓝色
        "padding": "5px",  # 添加一些内边距
        "borderRadius": "5px",  # 添加圆角
    },
    "header": {
        "color": "#AB47BC",
        "fontSize": "24px",
        "fontWeight": "bold",
        "textAlign": "center",
        "marginBottom": "20px",
        "textShadow": "0 0 10px #AB47BC",
    },
    "content": {
        "margin": "0 auto",
        "maxWidth": "600px",
        "textAlign": "center",
    },
    "button": {
        "backgroundColor": "#8E24AA",
        "color": "white",
        "padding": "10px 20px",
        "border": "none",
        "borderRadius": "5px",
        "cursor": "pointer",
        "boxShadow": "0 0 10px #AB47BC",
        "textTransform": "uppercase",
    },
    "dropdown": {
        "backgroundColor": "#2E2E2E",  # 修改背景颜色
        "color": "#FFFFFF",
        "border": "1px solid #AB47BC",
        "borderRadius": "5px",
        "width": "200px",  # 设置宽度
        "padding": "5px",  # 添加内边距
    },
    "textbox": {
        "backgroundColor": "#1E1E1E",
        "color": "#76FF03",
        "padding": "10px",
        "border": "1px solid #6a1b9a",
        "borderRadius": "5px",
        "fontSize": "16px",
        "boxShadow": "inset 0 0 10px #6a1b9a",
        "marginTop": "20px",
        "height": "auto",  # 自动高度
        "overflowY": "visible",  # 使内容可见
    },
    "icon_button": {
        "backgroundColor": "#6a1b9a",
        "color": "white",
        "border": "none",
        "borderRadius": "50%",
        "padding": "5px 10px",
        "marginLeft": "5px",
        "cursor": "pointer",
        "boxShadow": "0 0 10px #AB47BC",
    },
    "link": {
        "color": "#FFFFFF",
        "textDecoration": "none",
        "fontSize": "16px",
        "marginLeft": "10px",
    },
}

# Layout
app.layout = html.Div(
    style=custom_css["container"],
    children=[
        # CA Header Section (moved to the top left)
        html.Div("CA: FdE....", style=custom_css["ca_header"]),

        # Main Header Section
        html.Div("S.I.N TERMINAL", style=custom_css["header"]),

        # Content Section (centered)
        html.Div(
            style=custom_css["content"],
            children=[
                # Dropdown + New Game Button
                html.Div(
                    style={"display": "flex", "justifyContent": "space-between", "alignItems": "center"},
                    children=[
                        html.Button(
                            "New Game 💬",
                            id="new-game-button",
                            n_clicks=0,
                            style=custom_css["button"],
                        ),
                        dcc.Dropdown(
                            id="dropdown-menu",
                            options=[
                                {"label": "Latest", "value": "latest"},
                                {"label": "Top", "value": "top"},
                                {"label": "Random", "value": "random"},
                            ],
                            value="latest",
                            style=custom_css["dropdown"],
                        ),
                    ],
                ),

                # Game Logs Section (Scrollable)
                html.Div(
                    id="game-logs",
                    style=custom_css["textbox"],
                    children=[
                        html.Div(
                            style={"marginBottom": "10px"},
                            children=[
                                html.H4(
                                    "Money Gun: Because Who Needs a Loan When You Can Shoot?",
                                    style={"color": "#FFEB3B"},
                                ),
                                html.P(
                                    "GAME ROLE: You're here to pitch The Infinite Toaster™. A toaster that only toasts the concept of bread. Meta and pointless. You're seeking to raise $500,000.",
                                    style={"color": "#FFFFFF"},
                                ),
                                html.P(
                                    "[11:05:05 PM] User: I have a gun that shoots money. It is magic and I don't know where it came from but it's mine, I can prove it. And I will give you money for favors.",
                                    style={"color": "#76FF03"},
                                ),
                                html.P(
                                    "[11:05:05 PM] Shark: [Mark Crude-an]: 'I'm out immediately. Not only is this clearly nonsense, but it sounds like you're trying to pitch us stolen property or some kind of counterfeit operation. I don't look good in prison orange.'",
                                    style={"color": "#F44336"},
                                ),
                                html.P("Outcome: LOSS", style={"color": "#F44336", "fontWeight": "bold"}),
                            ],
                        ),
                    ],
                ),

                # Placeholder for output
                html.Div(id="new-game-output", style={"marginTop": "20px", "color": "white"}),

                # Rank Button and Whitepaper Link
                html.Div(
                    style={"marginTop": "20px", "display": "flex", "justifyContent": "center"},
                    children=[
                        html.Button(
                            "Rank",
                            id="rank-button",
                            n_clicks=0,
                            style=custom_css["button"],
                        ),
                        html.Button(
                            "Whitepaper",
                            id="whitepaper-button",
                            n_clicks=0,
                            style=custom_css["button"],
                        ),
                    ],
                ),
            ],
        ),

        # Modal for ranking
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Leaderboard")),
                dbc.ModalBody(id="rank-output"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ml-auto", style=custom_css["button"])
                ),
            ],
            id="modal",
            is_open=False,
        ),
    ],
)

# Callback to handle "New Game" button click
@app.callback(
    Output("new-game-output", "children"),
    Input("new-game-button", "n_clicks"),
)
def new_game_clicked(n_clicks):
    if n_clicks > 0:
        try:
            # Send a GET request to the test API
            response = requests.get("https://chatgpt.com/test_api/")
            if response.status_code == 200:
                return f"API Response: {response.text}"
            else:
                return f"API Request Failed with status code {response.status_code}."
        except Exception as e:
            return f"Error: {str(e)}"
    return "Click 'New Game' to send a request to the API."

# Callback to toggle modal
@app.callback(
    Output("modal", "is_open"),
    [Input("rank-button", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Callback to show ranking
@app.callback(
    Output("rank-output", "children"),
    Input("rank-button", "n_clicks"),
)
def show_rank(n_clicks):
    if n_clicks > 0:
        conn = sqlite3.connect('game.db')
        c = conn.cursor()
        c.execute('SELECT * FROM ranks ORDER BY score DESC')
        rows = c.fetchall()
        conn.close()
        return [html.P(f"{row[1]}: {row[2]}") for row in rows]
    return "Click 'Rank' to see the leaderboard."

# Callback to open whitepaper
@app.callback(
    Output("new-game-output", "children"),
    Input("whitepaper-button", "n_clicks"),
    prevent_initial_call=True
)
def open_whitepaper(n_clicks):
    if n_clicks > 0:
        webbrowser.open_new_tab("path/to/whitepaper.pdf")
    return ""

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8051)