import dash
from dash import dcc, html, Input, Output, State, no_update
import requests
import dash_bootstrap_components as dbc
import sqlite3
import webbrowser
from openai import OpenAI

# Initialize Dash app with Bootstrap stylesheet
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

client = OpenAI(
    api_key='7bb6b5cb-cc26-488c-a436-604cacd9a4d3',
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)

# Custom CSS for a roguelike dungeon pixel aesthetic
custom_css = {
    "container": {
        "backgroundColor": "#0d0d0d",
        "color": "#e0e0e0",
        "fontFamily": "Press Start 2P, monospace",
        "padding": "20px",
        "border": "2px solid #ff4500",
        "borderRadius": "10px",
        "boxShadow": "0 0 20px #ff4500",
    },
    "ca_header": {
        "color": "#e0e0e0",
        "fontSize": "14px",
        "fontWeight": "bold",
        "textAlign": "left",
        "marginBottom": "10px",
        "textShadow": "0 0 10px #ff4500",
        "backgroundColor": "#1a1a1a",
        "padding": "10px",
        "borderRadius": "5px",
        "border": "1px solid #ff4500",
    },
    "header": {
        "color": "#ff4500",
        "fontSize": "32px",
        "fontWeight": "bold",
        "textAlign": "center",
        "marginBottom": "20px",
        "textShadow": "0 0 10px #ff4500",
    },
    "content": {
        "margin": "0 auto",
        "maxWidth": "800px",
        "textAlign": "center",
    },
    "button": {
        "backgroundColor": "#ff4500",
        "color": "#e0e0e0",
        "padding": "10px 20px",
        "border": "none",
        "borderRadius": "5px",
        "cursor": "pointer",
        "boxShadow": "0 0 10px #ff4500",
        "textTransform": "uppercase",
        "margin": "5px",
    },
    "dropdown": {
        "backgroundColor": "#1a1a1a",
        "color": "#e0e0e0",
        "border": "1px solid #ff4500",
        "borderRadius": "5px",
        "width": "200px",
        "padding": "5px",
    },
    "textbox": {
        "backgroundColor": "#1a1a1a",
        "color": "#76ff03",
        "padding": "10px",
        "border": "1px solid #ff4500",
        "borderRadius": "5px",
        "fontSize": "16px",
        "boxShadow": "inset 0 0 10px #ff4500",
        "marginTop": "20px",
        "height": "auto",
        "overflowY": "auto",
        "maxHeight": "400px",
    },
    "icon_button": {
        "backgroundColor": "#ff4500",
        "color": "#e0e0e0",
        "border": "none",
        "borderRadius": "50%",
        "padding": "5px 10px",
        "marginLeft": "5px",
        "cursor": "pointer",
        "boxShadow": "0 0 10px #ff4500",
    },
    "link": {
        "color": "#e0e0e0",
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

        # Banner Image
        html.Img(src="https://github.com/ChrisBai1998/AIAgent/blob/main/asset/banner.png", style={"width": "100%", "borderRadius": "10px", "marginBottom": "20px"}),

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
                                    style={"color": "#ff4500"},
                                ),
                                html.P(
                                    "GAME ROLE: You're here to pitch The Infinite Toaster™. A toaster that only toasts the concept of bread. Meta and pointless. You're seeking to raise $500,000.",
                                    style={"color": "#e0e0e0"},
                                ),
                                html.P(
                                    "[11:05:05 PM] User: I have a gun that shoots money. It is magic and I don't know where it came from but it's mine, I can prove it. And I will give you money for favors.",
                                    style={"color": "#76ff03"},
                                ),
                                html.P(
                                    "[11:05:05 PM] Shark: [Mark Crude-an]: 'I'm out immediately. Not only is this clearly nonsense, but it sounds like you're trying to pitch us stolen property or some kind of counterfeit operation. I don't look good in prison orange.'",
                                    style={"color": "#ff4500"},
                                ),
                                html.P("Outcome: LOSS", style={"color": "#ff4500", "fontWeight": "bold"}),
                            ],
                        ),
                    ],
                ),

                # User Input Section
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                dcc.Input(
                                    id="user-input",
                                    type="text",
                                    placeholder="输入你的命令...",
                                    style={"width": "80%", "padding": "10px", "borderRadius": "5px",
                                           "border": "1px solid #ff4500", "color": "#e0e0e0",
                                           "backgroundColor": "#1a1a1a"},
                                ),
                                html.Button(
                                    "提交",
                                    id="submit-button",
                                    n_clicks=0,
                                    style=custom_css["button"],
                                ),
                            ],
                            style={"display": "flex", "justifyContent": "center", "marginTop": "20px"}
                        ),
                    ]
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
                        html.Button(
                            "GitHub",
                            id="github-button",
                            n_clicks=0,
                            style=custom_css["button"],
                        ),
                        html.Button(
                            id="twitter-button",
                            n_clicks=0,
                            style={**custom_css["button"], "backgroundColor": "#1DA1F2", "display": "flex", "alignItems": "center"},
                            children=[
                                html.Img(src="https://github.com/ChrisBai1998/AIAgent/blob/main/asset/twitter-logo.jpg", style={"width": "20px", "marginRight": "5px"}),
                                "Twitter"
                            ],
                        ),
                        html.Button(
                            "Connect Wallet",
                            id="connect-wallet-button",
                            n_clicks=0,
                            style={**custom_css["button"], "backgroundColor": "#FF5722"},
                        ),
                    ],
                ),
                # Placeholder for whitepaper output
                html.Div(id="whitepaper-output", style={"marginTop": "20px", "color": "white"}),
                html.Div(id="github-output", style={"marginTop": "20px", "color": "white"}),
                html.Div(id="twitter-output", style={"marginTop": "20px", "color": "white"}),
                html.Div(id="connect-wallet-output", style={"marginTop": "20px", "color": "white"}),
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
    Output("game-logs", "children"),
    Input("new-game-button", "n_clicks"),
    Input("submit-button", "n_clicks"),
    State("user-input", "value"),
)
def new_game_or_user_input(new_game_clicks, submit_clicks, user_input):
    history = [
        {"role": "system",
         "content": "想象你是一个地牢游戏的掌控者，现在需要你根据用户描述给出下一步可能出现的场景和选项供用户选择，用户原始生命值为10，武力值为0，如果遇到武力值比他高的怪物扣除两点生命值，用户在游玩过程中会捡到武器.用户赢的条件为找到宝藏，用户生命值为0时，游戏结束."}
    ]
    history.append({"role": "user", "content": '现在生成初始场景，并给出下一步选项'})
    game_logs = [
        html.Div(
            style={"marginBottom": "10px"},
            children=[
                html.H4(
                    "Money Gun: Because Who Needs a Loan When You Can Shoot?",
                    style={"color": "#ff4500"},
                ),
                html.P(
                    "GAME ROLE: You're here to pitch The Infinite Toaster™. A toaster that only toasts the concept of bread. Meta and pointless. You're seeking to raise $500,000.",
                    style={"color": "#e0e0e0"},
                ),
                html.P(
                    "[11:05:05 PM] User: I have a gun that shoots money. It is magic and I don't know where it came from but it's mine, I can prove it. And I will give you money for favors.",
                    style={"color": "#76ff03"},
                ),
                html.P(
                    "[11:05:05 PM] Shark: [Mark Crude-an]: 'I'm out immediately. Not only is this clearly nonsense, but it sounds like you're trying to pitch us stolen property or some kind of counterfeit operation. I don't look good in prison orange.'",
                    style={"color": "#ff4500"},
                ),
                html.P("Outcome: LOSS", style={"color": "#ff4500", "fontWeight": "bold"}),
            ],
        ),
    ]
    if new_game_clicks > 0:
        completion = client.chat.completions.create(
            model="ep-20241224223325-spdq4",  # your model endpoint ID
            messages=history,
            stream=False,
        )
        # Extract AI's response
        ai_response = completion.choices[0].message.content
        history.append({"role": "assistant", "content": ai_response})
        # Add the user's input and AI's response to the game logs
        game_logs.append(html.P(f"[AI]: {ai_response}", style={"color": "#ff4500"}))

    if submit_clicks > 0:
        if user_input:
            # Send a request to the OpenAI API to get AI's response
            history.append({"role": "user", "content": user_input})
            completion = client.chat.completions.create(
                model="ep-20241224223325-spdq4",  # your model endpoint ID
                messages=history,
                stream=False,
            )

            # Extract AI's response
            ai_response = completion.choices[0].message.content
            history.append({"role": "assistant", "content": ai_response})

            # Add the user's input and AI's response to the game logs
            game_logs.append(html.P(f"[User]: {user_input}", style={"color": "#76ff03"}))
            game_logs.append(html.P(f"[AI]: {ai_response}", style={"color": "#ff4500"}))

    return "", game_logs

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
    Output("whitepaper-output", "children"),
    Input("whitepaper-button", "n_clicks"),
    prevent_initial_call=True
)
def open_whitepaper(n_clicks):
    if n_clicks > 0:
        webbrowser.open_new_tab("https://github.com/ChrisBai1998/AIAgent/whitepaper")
    return no_update

# Callback to open GitHub
@app.callback(
    Output("github-output", "children"),
    Input("github-button", "n_clicks"),
    prevent_initial_call=True
)
def open_github(n_clicks):
    if n_clicks > 0:
        webbrowser.open_new_tab("https://github.com/ChrisBai1998/AIAgent")
        return "GitHub opened in a new tab."
    return no_update

# Callback to open Twitter
@app.callback(
    Output("twitter-output", "children"),
    Input("twitter-button", "n_clicks"),
    prevent_initial_call=True
)
def open_twitter(n_clicks):
    if n_clicks > 0:
        webbrowser.open_new_tab("https://twitter.com")
        return "Twitter opened in a new tab."
    return no_update

# Callback to connect wallet
@app.callback(
    Output("connect-wallet-output", "children"),
    Input("connect-wallet-button", "n_clicks"),
    prevent_initial_call=True
)
def connect_wallet(n_clicks):
    if n_clicks > 0:
        # Add your wallet connection logic here
        return "Wallet connected."
    return no_update

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8051)