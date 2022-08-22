from dash import dcc
from dash import html
from datetime import datetime, timedelta
time_slutt = (datetime.now() - timedelta(days=1))
time_slutt = time_slutt.strftime("%d-%m-%Y")

def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])

def get_menu():
    menu = html.Div(
        [
            # dcc.Link(
            #     "Austria",
            #     href="/dash-P2P-report/Austria",
            #     className="tab first", style={"color":"rgb(69,157,175)", "font-weight":"500", "text-align":"center"}
            # ),
            # dcc.Link(
            #     "Click here to see your P2P platform",
            #     href="/dash-P2P/Finland",
            #     className="tab", style={"color":"rgb(69,157,175)", "font-weight":"500"}
            # ),
            # dcc.Link(
            #     "Spain",
            #     href="/dash-P2P/Spain",
            #     className="tab", style={"color":"rgb(69,157,175)", "font-weight": "500", "margin-right":"31%"}
            # ),


            # dcc.Link(
            #     "Monthly data",
            #     href="/dash-funancial-report/fees",
            #     className="tab",

        ],
        className="row all-tabs",
        # style={"margin-left": "200px", "margin-right":"0px", "margin-top": "-100px"},
    )
    
    return menu
def get_header(app):
    header = html.Div(
        [
            html.Div(
                [
                    html.A(
                        html.Img(
                            src=app.get_asset_url("senderP2Plogo.png"),
                            className="logo",
                        ),
                        href="/dash-P2P/overview",
                    ),                    
                    html.A(
                        html.Button(
                            "Home",
                            id="learn-more-button",
                            style={"margin-right": "5%", "color":"rgb(69,157,175)"},
                        ),
                        href="/dash-P2P/overview"
                    ), 
    html.H1(
        children='P2P-market',
        style={
            'textAlign': 'center',
            "color":"rgb(69,157,175)", 
            "margin-bottom":"10mm"

        }
    ),
                

                        
        
                    
                ],
                className="row",
            ),

        ],
        className="row",
    )
    return header






def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table
