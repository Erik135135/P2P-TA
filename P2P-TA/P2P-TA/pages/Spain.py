from dash import dcc
from dash import html
from utils import Header, make_dash_table
from API import p2p_fig, user_names, textp2p_transfig, fig_bar_text, textp2p_transfigH5 #fig_bar


def create_layout(app):
    return html.Div(
        [
            Header(app),
            # page 4
            html.Div(
                [
                    # Row 1
                    html.Div(
                        [
                            html.Div(
                                [html.H5(["Introduction to Spain"],style = {"color":"rgb(69,157,175)"}), 
                                  html.P("Spain is......"),
                                  html.Br([])

],
                                 
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                        style={"margin-left": "13%", "margin-right":"13%", "margin-buttom":"20px", "font-size": "130%"},
                    ),
                    # Row 2
                    html.Div(
                        [
                            html.Div(

                                [html.H5(["Slider"],style = {"color":"rgb(69,157,175)"}), 
                                  html.P("Drag the slider to investigate for each user"),
                                  html.Div(
                                                          dcc.Slider(id="house",
    min=0,
    max=len(p2p_fig)-1,
    step=1,
    marks = {str(t):{"label":''+str(user_names[t])+''} for t in range(0,len(p2p_fig),1)},
    value=0
), 
                        className="row ",
                        style={"margin-left": "0%", "margin-right":"0%", "margin-top":"1%"}
                    ),
                                  html.Br([]),
                                  html.Br([]), 
                                  html.Div(
                                        [
                                    html.H5(["Overview of import/export"],style = {"color":"rgb(69,157,175)"}),
                                    html.P(
                                        "The line chart is showing how much each user are importing or exporting. Import/export can be done through grid or the P2P market.\
                                        The green bars on the linechart is showing how much each selling or buying from the P2P market. Note that if the user does not have the green bars\
                                            it does not sell/buy any power from the P2P market. The red line is showing....\
                                                The blue line is showing......"), 

                                        ],
                                        className="row"

                                    ),
                                    html.Div(
                                        [
                                            
                                            dcc.Graph(id="transspain",config = {'displayModeBar': False,
    'editable': False,
    'showLink':False,
    'displaylogo': False}, figure={}, 
                                                
                                            ),
                                        ],
                                        className="row", style={"margin-top": "-5%"}

                                    ),
                                 

],
                                 
                                className="twelve columns",
                                
                            )
                        ],
                        className="row ",
                        style={"margin-left": "13%", "margin-right":"13%", "margin-buttom":"-0px"}
                    ),
                    

                    # Row 3
                    
                    #%% 
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5(["Profit & costs"],style = {"color":"rgb(69,157,175)"} ),
                                    html.P(
                                            fig_bar_text),
                                    
                                    html.Br([]),
                                    html.Div(
                                        [
                                            
                                            dcc.Graph(id="barspain",config = {'displayModeBar': False,
    'editable': False,
    'showLink':False,
    'displaylogo': False}, figure={}, 
                                                
                                            ),
                                        ],
                                        className="row",
                                        style={"margin-top":"-0%"}

                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row",
                        style={"margin-left": "13%", "margin-right":"13%","margin-bottom": "35px", "margin-top":"-0px"}
                    ),
                    
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5(textp2p_transfigH5,style = {"color":"rgb(69,157,175)"} ),
                                    html.P(
                                        textp2p_transfig),
                                    
                                    html.Br([]),
                                    html.Div(
                                        [
                                            
                                            dcc.Graph(id="p2ptransspain", config = {'displayModeBar': False,
    'editable': False,
    'showLink':False,
    'displaylogo': False}, figure={},
                                                
                                            ),
                                        ],
                                        className="row",
                                        style={"margin-top":"0%"}

                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row",
                        style={"margin-left": "13%", "margin-right":"13%","margin-bottom": "35px", "margin-top":"-200px"}
                    ),

                ],
                className="sub_page",
            ),
        ],
        className="page",
    )


