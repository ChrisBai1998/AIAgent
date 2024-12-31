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
import yaml

# Initialize Dash app with Bootstrap stylesheet
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], suppress_callback_exceptions=True)
game_logs=[]
history=[]

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(
    api_key=API_KEY
)

# Layout
app.layout = html.Div(
    id="main-container",
    children=[
        # floating pixels
        html.Div(className="pixel"),html.Div(className="pixel"),
        html.Div(className="pixel"),html.Div(className="pixel"),
        html.Div(className="pixel"),html.Div(className="pixel"),
        html.Div(className="pixel"),html.Div(className="pixel"),
        html.Div(className="pixel"),html.Div(className="pixel"),
        html.Div(className="pixel"),html.Div(className="pixel"),
        html.Div(className="pixel"),html.Div(className="pixel"),

        # CA Header Section
        html.Div("CA: 0x2170ed0880ac9a755fd29b2688956bd959f933f8", id="ca-header"),

        # Main Header Section
        html.Div("Pixel Dungeon", id="main-header"),

        # Subtitle Section
        html.Div("👨‍👩‍👧‍👦Human ⚔️ AI🤖", id="subtitle"),

        # Banner Image
        html.Img(src="./assets/banner.jpg",
                 id="banner-image"),

        # Content Section
        html.Div(
            id="content-section",
            children=[
                # Languages Section
                html.Div(
                    id="language-selection",
                    children=[
                        html.Img(
                            src="./assets/language.png",
                            id="language-icon"
                        ),
                        
                        # Dropdown
                        dcc.Dropdown(
                            id="language-dropdown",
                            options=[
                                {"label": "English", "value": "en"},
                                {"label": "Español", "value": "es"},
                                {"label": "Français", "value": "fr"},
                                {"label": "Deútsch", "value": "de"},
                                {"label": "polski", "value": "pl"},
                                {"label": "한국어", "value": "ko"},
                                {"label": "日本語", "value": "ja"},
                                {"label": "中文", "value": "zh"},
                            ],
                            placeholder="English",
                            value="en",  # Default value
                        ),
                    ]
                ),

                # Game Logs Section
                html.Div(
                    id="game-logs",
                    children=[
                        html.Div(
                            id="game-master-dialogue",
                            children=[
                                dcc.Markdown(
                                    '''
                                    [Pixel Dungeon Master]: Welcome, brave adventurer, to the unknown! Before you stand six doors—snowfields, shadowy forests, scorching deserts, or perhaps something else. Even I forget sometimes.
                                    In this dungeon, your choices shape your fate. I’ll give you some items, but beware—gifts can lead to trouble too.
                                    our mission? Find the legendary treasure! But watch out for traps and ‘friendly’ monsters. Fail, and the souls of past adventurers might just keep you company!Ready? Hit 'Start' and prove yourself a hero—or the next joke.
                                    Type /start to begin.
                                    ''',
                                    id="dungeon-master-dialogue",
                                ),
                            ],
                        ),
                    ],
                ),

                # User Input Section
                html.Div(
                    id="user-input-section",
                    children=[
                        html.Div(
                            children=[
                                dcc.Input(
                                    id="user-input",
                                    type="text",
                                    placeholder="Enter your Choice ...",
                                ),
                                html.Button(
                                    "Submit",
                                    id="submit-button",
                                    n_clicks=0,
                                ),
                            ],
                            id="submit-button-container",
                        ),
                    ]
                ),

                # Rank Button and Whitepaper Link
                html.Div(
                    id="button-section",
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
                                html.Img(src="./assets/twitter-logo.png", alt="twi-logo", style={"width": "20px", "marginRight": "5px"}),
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
                    # dcc.Markdown(
                    #         '''
                    #         [Pixel Dungeon Master]: Welcome, brave adventurer, to the unknown! Before you stand six doors—snowfields, shadowy forests, scorching deserts, or perhaps something else. Even I forget sometimes."
                    #         In this dungeon, your choices shape your fate. I’ll give you some items, but beware—gifts can lead to trouble too.
                    #         our mission? Find the legendary treasure! But watch out for traps and ‘friendly’ monsters. Fail, and the souls of past adventurers might just keep you company!Ready? Hit 'Start' and prove yourself a hero—or the next joke.
                    #         Type /start to begin.
                    #         ''',
                    #         style={"color": "#8c12bc"},
                    #         ),
                    "initial conversation from Pixel Dungeon Master",
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
                                style={"width": "100%", "maxWidth": "300px", "borderRadius": "10px",
                                        "padding-bottom": "5px", "box-shadow": "0 0 20px #950392"}
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
                                        prompt="生成一张场景图片来帮助描述当前场景 以提升用户体验并且请使用像素风格的图片, 并且主色调最好为偏紫色。以下为场景描述\n" 
                                                + prompt + " 生成的像素图片中绝对不允许以任何形式添加任何文字。",
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

# Callback to select language
@app.callback(
    [
        Output("submit-button", "children"),
        Output("rank-button", "children"),
        Output("whitepaper-button", "children"),
        Output("github-button", "children"),
        Output("twitter-button", "children"),
        Output("connect-wallet-button", "children"),
        Output("dungeon-master-dialogue", "children"),
    ],
    Input("language-dropdown", "value")
)
def update_language(selected_language):
    with open('./cfgs/button_languages.yml', 'r', encoding='utf-8') as file:
        btn_languages = yaml.safe_load(file)
    with open('./cfgs/dungeon_master_languages.yml', 'r', encoding='utf-8') as file:
        dm_languages = yaml.safe_load(file)

    languages = btn_languages['en']
    languages.append(dm_languages['en'])

    if selected_language not in btn_languages or selected_language not in dm_languages:
        return icon_helper(languages)
    
    languages = btn_languages[selected_language]
    languages.append(dm_languages[selected_language])

    return icon_helper(languages)

def icon_helper(elem_text_list):
    # hardcoded icons: submit, rank, whitepaper, github, twitter, wallet, dialogue
    icon_list, n = [], 0
    # submit
    icon_list.append("🚀"+elem_text_list[n])
    n += 1
    # rank
    icon_list.append("🏅"+elem_text_list[n])
    n += 1
    # whitepaper
    icon_list.append("📄"+elem_text_list[n])
    n += 1
    # github
    icon_list.append([html.Img(src="assets/github-logo.png", alt="Twitter Logo", style={"width": "20px", "marginRight": "5px"}), elem_text_list[n]])
    n += 1
    # twitter
    icon_list.append([html.Img(src="assets/twitter-logo.png", alt="Twitter Logo", style={"width": "20px", "marginRight": "5px"}), elem_text_list[n]])
    n += 1
    # wallet
    icon_list.append("🪙"+elem_text_list[n])
    n += 1
    # dialogue
    icon_list.append(elem_text_list[n])

    return icon_list

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
    # app.run_server(debug=True, host='0.0.0.0', port=8051)