import dash
from dash import dcc, html, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import sqlite3
import webbrowser
import random
from openai import OpenAI

from dotenv import load_dotenv
import os
import time

# Initialize Dash app with Bootstrap stylesheet
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], suppress_callback_exceptions=True)
game_logs=[]
history=[]

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(
    api_key=API_KEY
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
        # "border": "1px solid #ff4500",
    },
    "header": {
        "color": "#ff4500",
        "fontSize": "32px",
        "fontWeight": "bold",
        "textAlign": "center",
        "marginBottom": "20px",
        "textShadow": "0 0 10px #ff4500",
    },
    "subtitle": {
        "color": "#ff4500",
        "fontSize": "20px",
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
    "bottom_button_container": {
        "marginTop": "20px",
        "display": "flex",
        "flexWrap": "wrap",
        "justifyContent": "center",
        "gap": "10px",
    },
    "dropdown": {
        "backgroundColor": "#1a1a1a",
        "color": "#e0e0e0",
        "border": "1px solid #ff4500",
        "borderRadius": "5px",
        "width": "200px",
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
        "minHeight": "400px",
        "overflowY": "auto",
        "maxHeight": "800px",
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
        html.Div("Dungeon Adventure Game", style=custom_css["header"]),
        # Subtitle Section
        html.Div("👨‍👩‍👧‍👦Human ⚔️ AI🤖", style=custom_css["subtitle"]),

        # Banner Image
        html.Img(src="https://raw.githubusercontent.com/ChrisBai1998/AIAgent/refs/heads/main/assets/banner.png",
                 style={"width": "100%", "maxWidth": "800px", "borderRadius": "10px", "marginBottom": "20px", 
                        "display": "block", "marginLeft": "auto", "marginRight": "auto", "box-shadow": "0 0 20px #ff4500"}),

        # Content Section (centered)
        html.Div(
            style=custom_css["content"],
            children=[

                # Game Logs Section (Scrollable)
                html.Div(
                    id="game-logs",
                    style=custom_css["textbox"],
                    children=[
                        html.Div(
                            style=custom_css["bottom_button_container"],
                            children=[
                                html.H4(
                                    "Pixel Dungeon Master:",
                                    style={"color": "#ff4500"},
                                ),
                                html.P(
                                    "Welcome, brave adventurer, to the unknown! Before you stand six doors—snowfields, shadowy forests, scorching deserts, or perhaps something else. Even I forget sometimes.",
                                    style={"color": "#e0e0e0"},
                                ),
                                html.P(
                                    "In this dungeon, your choices shape your fate. I’ll give you some items, but beware—gifts can lead to trouble too.",
                                    style={"color": "#76ff03"},
                                ),
                                html.P(
                                    "our mission? Find the legendary treasure! But watch out for traps and ‘friendly’ monsters. Fail, and the souls of past adventurers might just keep you company!Ready? Hit 'Start' and prove yourself a hero—or the next joke.",
                                    style={"color": "#ff4500"},
                                ),
                                html.P("Type /start to begin.", style={"color": "#ff4500", "fontWeight": "bold"}),
                                
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
                                    placeholder="Enter your Choice ...",
                                    style={"width": "80%", "padding": "10px", "borderRadius": "5px",
                                           "border": "1px solid #ff4500", "color": "#e0e0e0",
                                           "backgroundColor": "#1a1a1a"},
                                ),
                                html.Button(
                                    "Submit",
                                    id="submit-button",
                                    n_clicks=0,
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
                    style={"width": "100%", "maxWidth": "800px", "margin": "0 auto", "display": "flex", "flexWrap": "wrap", "justifyContent": "flex-start"},
                    children=[
                        html.Button(
                            "Rank",
                            id="rank-button",
                            n_clicks=0,
                        ),
                        html.Button(
                            "Whitepaper",
                            id="whitepaper-button",
                            n_clicks=0,
                        ),
                        html.Button(
                            "GitHub",
                            id="github-button",
                            n_clicks=0,
                        ),
                        html.Button(
                            id="twitter-button",
                            n_clicks=0,
                            style={"backgroundColor": "#1DA1F2"},
                            children=[
                                html.Img(src="https://raw.githubusercontent.com/ChrisBai1998/AIAgent/refs/heads/main/assets/twitter-logo.png", style={"width": "20px", "marginRight": "5px"}),
                                "Twitter"
                            ],
                        ),
                        html.Button(
                            "Connect Wallet",
                            id="connect-wallet-button",
                            n_clicks=0,
                            style={"backgroundColor": "#FF5722"},
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
        #save conversation
        dcc.Store(id="history", data=[]),
        dcc.Store(id="start_game", data=False),

        # image flag
        dcc.Store(id="dynamic_image_prompt", data=0),

        # Modal for ranking
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Leaderboard")),
                dbc.ModalBody(id="rank-output"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ml-auto")
                ),
            ],
            id="modal",
            is_open=False,
        ),
    ],
)

# Callback to handle "New Game" button click
@app.callback(
   
    Output("submit-button", "n_clicks"),
    Output("game-logs", "children"),
    Output("history", "data"),
    Output("user-input", "value"),
    Output("start_game", "data"),
    Output("dynamic_image_prompt", "data"),
    Input("submit-button", "n_clicks"),
    Input("game-logs", "children"),
    State("user-input", "value"),
    State("history", "data"),
    State("start_game", "data"),
)
def new_game_or_user_input(submit_clicks, game_logs, user_input, history, start_game):
    dynamic_image_prompt=0
    if submit_clicks > 0 and 'start' in user_input:
        submit_clicks-=1
        start_game=True
        game_logs=[
                    html.H4(
                            "Pixel Dungeon Master:",
                            style={"color": "#ff4500"},
                            ),
                    html.P(
                            "Welcome, brave adventurer, to the unknown! Before you stand six doors—snowfields, shadowy forests, scorching deserts, or perhaps something else. Even I forget sometimes.",
                            style={"color": "#e0e0e0"},
                            ),
                    html.P(
                            "In this dungeon, your choices shape your fate. I’ll give you some items, but beware—gifts can lead to trouble too.",
                            style={"color": "#76ff03"},
                            ),
                    html.P(
                            "our mission? Find the legendary treasure! But watch out for traps and ‘friendly’ monsters. Fail, and the souls of past adventurers might just keep you company!Ready? Hit 'Start' and prove yourself a hero—or the next joke.",
                             style={"color": "#ff4500"},
                                ),
                    html.P("Type /start to begin.", style={"color": "#ff4500", "fontWeight": "bold"}),
                                 ]
        history=[]
        history = [
        {"role": "system",
         "content": "想象你现在是一个地牢游戏的掌管者，地牢游戏的背景随机生成为：雪地，森林，沙漠，现代城市，地下城，古堡，小概率出现地牢。"
                    + "基于用户的选择将出现不同的剧情分支，可能带来不同的结果（惩罚/奖励/）。游戏过程中用户可能会获得不同的物品，请基于物品为玩家量身定做后续剧情，用户赢的条件为找到最终宝藏，用户死亡时，游戏结束。"
                    + "如果用户发与选项无关的东西，必须提醒用户选择一个选项"}]
        history.append({"role": "user", "content": '现在生成初始场景，并给出下一步选项'})
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # your model endpoint ID
            messages=history,
            stream=False,
        )
        # Extract AI's response
        text_response = completion.choices[0].message.content
        history.append({"role": "assistant", "content": text_response})
        # Add the user's input and AI's response to the game logs
        text_with_line_breaks = f"[AI]: {'  \n'.join(text_response.split('\n'))}"
        game_logs.append(dcc.Markdown(text_with_line_breaks, style={"color": "#ff4500"}))

    if submit_clicks > 0 and start_game==True:
        submit_clicks-=1
        if user_input:
            # Add user response to the game logs
            game_logs.append(html.P(f"[User]: {user_input}", style={"color": "#76ff03"}))
            # Send a request to the OpenAI API to get AI's response
            history.append({"role": "user", "content": user_input})
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=history,
                stream=False,
            )

            # Extract AI's response
            text_response = completion.choices[0].message.content
            history.append({"role": "assistant", "content": text_response})

            # First-time flag or random probability
            if "first_time" not in history[-1]:  # First time
                history[-1]["first_time"] = True
                generate_image = True
            else:  # Subsequent clicks
                generate_image = random.random() < 0.2  # 1/5 chance

            # Prob-based image generation
            if generate_image:
                # Generate image with OpenAI DALL-E
                game_logs.append(
                    dcc.Loading(
                        id="image-loading",
                        type="dot",  # "cube", "dot", "circle", "graph"
                        color="purple",
                        children=[
                            html.Img(
                                id="dynamic-img",
                                src="",
                                style={"width": "100%", "maxWidth": "300px", "borderRadius": "10px", "padding-bottom": "5px"}
                            )
                        ]
                    )
                )

                dynamic_image_prompt=text_response

            # Add AI's text response to the game logs
            text_with_line_breaks = f"[AI]: {'  \n'.join(text_response.split('\n'))}"
            game_logs.append(dcc.Markdown(text_with_line_breaks, style={"color": "#ff4500"}))

    return submit_clicks, game_logs, history, '', start_game, dynamic_image_prompt

# Callback for dynamic id/src image
@app.callback(
    Output("dynamic-img", "src"),  # Output for the src of the image
    Output("dynamic-img", "id"),   # Output for the id of the image
    Input("dynamic_image_prompt", "data"),
)
def generate_dynamic_ai_img(prompt):
    if prompt is None or prompt == '':
        return "", ""  # Return empty src and id if there's no input
    
    # Generate a random image source (you can replace this with an actual URL)
    dynamic_ai_img_url = client.images.generate(
                                        model="dall-e-3",
                                        prompt="生成一张场景图片来帮助描述当前场景 以提升用户体验并且请使用像素风格的图片, 并且主色调最好为偏紫色。图片中请不要添加任何文字。以下为场景描述\n" + prompt,
                                        size="1024x1024",
                                        quality="standard",
                                        n=1,
                                    ).data[0].url
    
    # Generate a dynamic ID based on input value and random number
    dynamic_id = f"dynamic-ai-img-{str(int(time.time()))}"
    
    # Return the dynamic id and image URL
    return dynamic_ai_img_url, dynamic_id

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
        webbrowser.open_new_tab("https://github.com/ChrisBai1998/AIAgent/tree/main/whitepaper")
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
    app.run_server(debug=True)
    # app.run_server(debug=True, host='0.0.0.0', port=8051)