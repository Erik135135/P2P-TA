from dash import dcc
from dash import html
from utils import Header, make_dash_table
from API import text_full



def create_layout(app):
    return html.Div(
        [
            Header(app),
            # page 4
            html.Div(
                [
                    # Row 1
                    dcc.Link(
                        "Click here to see your P2P trading algorithm results",
                        href="/dash-P2P/Finland",
                        className="row all-tabs", style={"color":"rgb(69,157,175)", "margin-buttom":"30px", "font-weight":"500", }
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    
                                    html.H5(
                                        ["Feedback from the P2P trading algorithm"], style={"color":"white"}
                                    ), 

    

            html.P(
             '\
             ' + text_full, style = {"color":"white"},
),


    
                                ], 
                                className="five columns textboxleft",
                            ),
                            html.Div(
                                [
                                    html.H5(
                                        "What is a P2P market? ",
                                        style = {"color":"white"},
                                    ),
                                    html.P(\
                                           "A P2P market is a marketplace where prosumers and consumers can trade electricity at an agreed price.\
                                            The P2P market created by NTNU will mainly simulate a P2P market and illustrate\
                                            possible economic viability to participants (end-users).\
                                            The results from the P2P market will be presented and available for end-users to access through this webpage.", 
                                            style= {"color":"white"},),
                            html.Div(
                        [
                            html.Img(
                            src=app.get_asset_url("senderP2P.png"),
                            className="picp2ptrade",
                        ),
                        ],

                    ),

                                    
                                ],
                                className="five columns textboxright"
                            ),
                        ],
                        className="row",
                        style={"margin-left": "19%", "margin-right":"5%", "margin-bottom": "0px"},
                    ),
                    # Row 4
                    # Row 2
html.Div(
                                [
                                    
                                    html.H5(
                                        ["P2P engagement"], style={"color":"white"}
                                    ), 

    

            html.P(
             'The P2P market introduces new stakeholders to the electriciy market.  \
             As new actors such as consumers/prosumers and local authorities are introduced to the electricity market \
             the existing boundaries need to be negotiated and also re-drawn. \
             As a result, new market designs and propositions are being tested to create a secure supply and efficient market. [2] \
             Some papers are pointing at regulations to be the main challenge to implement P2P markets into the existing national electricity grid. \
             Current national regulations are designed to fit existing conventional electricity systems and need to be redesigned to fit \
             the P2P business model. [3] Blockchain shows a great potential to facilitate a P2P market, however questions in regards to scalability, security and decentralization arrises. [1] \
             ', style = {"color":"white"},
             
),


    
                                ], 
                                className="textboxtwelve", style= {"margin-left":"19%", "margin-right":"18%", "margin-buttom":"50px"}
                            ),
    
            # Row
            html.Div(
                                [
                                    
                                    html.H5(
                                        ["Barriers for implementation"], style={"color":"white"}
                                    ), 

    

            html.P(
             'EU has a goal of including more consumers in the energy market. Consumers are engaged in increasing the share of local renewables and are contributing to accelerating the shift from consumerism to prosumerism. Some barriers to end-user engagement are the lack of understanding of how to participate in the energy market, the amount of smart technology in buildings, and the regulatory framework  \
             ', style = {"color":"white"},
           
             
),
# html.Li("", style = {"color":"white"},),
# html.Li("", style = {"color":"white"},),

    
                                ], 
                                className="textboxtwelve", style= {"margin-left":"19%", "margin-right":"18%", "margin-buttom":"50px"}
                            ),
                    # Row 3
            html.Div(
                                [
                                    
                                    html.H5(
                                        ["Sources"], style={"color":"white"}
                                    ), 
            html.P("1. Wongthongtham, P., Marrable, D., Abu-Salih, B., Liu, X., & Morrison, G. (2021). Blockchain-enabled Peer-to-Peer energy trading. Computers & Electrical Engineering, 94, 107299. https://doi.org/10.1016/j.compeleceng.2021.107299", style = {"color":"white"},),
            html.P("2. Iskandarova, M., Vernay, A. L., Musiolik, J., Müller, L., & Sovacool, B. K. (2022). Tangled transitions: Exploring the emergence of local electricity exchange in France, Switzerland and Great Britain. Technological Forecasting and Social Change, 180, 121677. https://doi.org/10.1016/j.techfore.2022.121677", style = {"color":"white"},),
            html.P("3. Junlakarn, S., Kokchang, P., & Audomvongseree, K. (2022). Drivers and Challenges of Peer-to-Peer Energy Trading Development in Thailand. Energies, 15(3), 1229. https://doi.org/10.3390/en15031229", style = {"color":"white"},),

    
                                ], 
                                className="textboxtwelvesources", style= {"margin-left":"19%", "margin-right":"18%"}
                            ),
                    # Row 3
                    
                    
                    
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
