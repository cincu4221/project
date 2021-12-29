import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_pivottable
import pandas as pd
import numpy as np
import plotly.express as px
from dash.dependencies import Output, Input

data = pd.read_csv("data/kaggle_survey_2021_responses.csv", index_col=0)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "2021 Kaggle Survey!!"
server = app.server

colors = {
    'background': '#111827',
    'content-background': '#1B263D',
    'plot_background': '#324773',
    'text': '#d3d3d3'
}


# Chart.1
@app.callback(
    Output('id_fig_age', 'figure'),
    Input('country-filter', 'value'))
def age_chart_func(value):
    fig_age = px.bar(data,
                     x=data[data['Q3'] == value]['Q1'][1:].value_counts().sort_index().index,
                     y=data[data['Q3'] == value]['Q1'][1:].value_counts().sort_index().values,
                     )
    fig_age.update_traces(hovertemplate='%{x}: %{y:.0f}',
                          marker_color='#E08E79',
                          marker_line_width=0,)
    fig_age.update_layout(paper_bgcolor=colors['content-background'],
                          font_color=colors['text'],
                          plot_bgcolor=colors['plot_background'],
                          autosize=True)
    fig_age.update_xaxes(title_text='Age Distribution')
    fig_age.update_yaxes(title_text='Counts')
    return fig_age


# Chart.2
@app.callback(
    Output('id_fig_gender', 'figure'),
    Input('country-filter', 'value'))
def gender_chart_func(value):
    fig_gender = px.pie(data,
                        names=data[data['Q3'] == value]['Q2'][1:].value_counts().sort_index().index,
                        values=data[data['Q3'] == value]['Q2'][1:].value_counts().sort_index().values,
                        hole=.3
                        )
    fig_gender.update_traces(textinfo = 'label+percent',
                             hovertemplate='%{label}: %{value:.0f}')
    fig_gender.update_layout(paper_bgcolor=colors['content-background'],
                             font_color=colors['text'],
                             showlegend=True,
                             autosize=True)
    return fig_gender


# Chart.3
@app.callback(
    Output('id_fig_job', 'figure'),
    Input('country-filter', 'value'))
def job_chart_func(value):
    fig_job = px.bar(data,
                     y=data[data['Q3'] == value]['Q5'][1:].value_counts(ascending=True).index,
                     x=data[data['Q3'] == value]['Q5'][1:].value_counts(ascending=True).values,
                     orientation='h'
                     )
    fig_job.update_traces(hovertemplate='%{y}: %{x:.0f}',
                          marker_color=px.colors.qualitative.Dark24[0:], # px 내장 색상 : px.colors.qualitative
                          marker_line_width=0,)
    fig_job.update_layout(paper_bgcolor=colors['content-background'],
                          font_color=colors['text'],
                          plot_bgcolor=colors['plot_background'],
                          autosize=True)
    fig_job.update_xaxes(title_text='Jobs')
    fig_job.update_yaxes(title_text='Counts')
    return fig_job


# Chart.4
@app.callback(
    Output('id_fig_career', 'figure'),
    Input('country-filter', 'value'))
def career_chart_func(value):
    fig_career = px.bar(data,
                        x=data[data['Q3'] == value]['Q6'][1:].value_counts().index,
                        y=data[data['Q3'] == value]['Q6'][1:].value_counts().values
                        )
    fig_career.update_traces(hovertemplate='%{x}: %{y:.0f}',
                             marker_color='#efebd8',
                             marker_line_width=0, )
    fig_career.update_layout(paper_bgcolor=colors['content-background'],
                             font_color=colors['text'],
                             plot_bgcolor=colors['plot_background'],
                             autosize=True)
    fig_career.update_xaxes(title_text='Career')
    fig_career.update_yaxes(title_text='Counts')
    return fig_career


# Tab_CSS
Tab_deco = {
    'background-color': '#1B263D',
    'color': 'lightgrey',
    'border': '1px solid #1B263D',
    'margin': '5px',
    'border-radius': '10px 10px 0 0',
}

sel_Tab_deco = {
    'background-color': '#324773',
    'color': 'lightgrey',
    'border': 'none',
    'margin': '5px',
    'border-bottom': '5px solid',
    'border-radius': '10px 10px 0 0'
}

Data_Tab = {
    'color': 'lightgrey',
    'background-color': '#1B263D',
    'border-radius': '10px 10px 0 0',
    'border': 'none',
    'margin': '0px 3px 0px 3px'
}

Data_Tab_selected = {
    'background-color': '#BAD9D6',
    'border-radius': '10px 10px 0 0',
    'border': 'none',
    'margin': '0px 3px 0px 3px'
}

# pivottable data
data_pivot = [['Age', 'Gender', 'Country', 'Job', 'Career']]
for num in list(range(25973)):
    data_pivot.append([
        data['Q1'][1:].values[num],
        data['Q2'][1:].values[num],
        data['Q3'][1:].values[num],
        data['Q5'][1:].values[num],
        data['Q6'][1:].values[num]])



# step 3. HTML
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Button(className='Red-btn'),
                        html.Button(className='Yellow-btn'),
                        html.Button(className='Green-btn'),
                        html.Div(
                            className='Div_center',
                            children=[
                                html.P(
                                    children="2021 Kaggle Machine Learning & Data Science Survey.dashboard",
                                    className="Top_bar_title"
                                )
                            ]
                        )
                    ],
                    className='Top_bar'
                ),
                html.Div(
                    children=[
                        html.H1(children="2021 Kaggle Machine Learning & Data Science Survey", className="header_title"),
                        html.P(children="My Notebook submitted to kaggle", className="header_description")
                    ],
                    className='header'
                ),
                dcc.Tabs([
                    dcc.Tab(
                        label='Visualization', style=Tab_deco, selected_style=sel_Tab_deco,
                        children=[
                            html.Div(
                                children=[
                                    html.Div(
                                        children=[
                                            dcc.Dropdown(
                                                id="country-filter",
                                                options=[
                                                    {"label": country, "value": country}
                                                    for country in np.sort(data.Q3[1:].unique())
                                                ],
                                                value="United States of America",
                                                style={
                                                    'background-color': colors['content-background'],
                                                    'border': 'none',
                                                    'border-radius': '5px',
                                                    'color': '#1B263D',
                                                    'display': 'table',
                                                    'margin': '10px auto 0 auto',
                                                    'width': '450px',
                                                }
                                            ),
                                        ],className='dropdown_border'
                                    ),
                                    html.Div(
                                        children=[
                                            html.Div(children=[
                                                html.P("Age Graph", className='sub_title')
                                            ]),
                                            html.Div(dcc.Graph(id='id_fig_age',
                                                               style={'margin': 5}), className='under_radius')
                                        ],
                                        className='section_age'
                                    ),
                                    html.Div(
                                        children=[
                                            html.Div(children=[
                                                html.P("Gender Graph", className='sub_title')
                                            ]),
                                            html.Div(dcc.Graph(id='id_fig_gender',
                                                               style={'margin': 5}), className='under_radius')
                                        ],
                                        className='section_gen'
                                    ),
                                    html.Div(
                                        children=[
                                            html.Div(children=[
                                                html.P("Job Graph", className='sub_title')
                                            ]),
                                            html.Div(dcc.Graph(id='id_fig_job',
                                                               style={'margin': 5}), className='under_radius')
                                        ],
                                        className='section_job'
                                    ),
                                    html.Div(
                                        children=[
                                            html.Div(children=[
                                                html.P("Career Graph", className='sub_title')
                                            ]),
                                            html.Div(dcc.Graph(id='id_fig_career',
                                                               style={'margin': 5}), className='under_radius')
                                        ],
                                        className='section_career'
                                    ),
                                ],className='contents-padding'
                            ),
                        ],
                    ),
                    dcc.Tab(
                        label='PivotTable', style=Tab_deco, selected_style=sel_Tab_deco, children=[
                            html.Div(
                                className='pivot_deco',
                                children=[
                                    html.Div(children=[
                                                html.P("PivotTable", className='sub_title_pivot')
                                            ]),
                                    dash_pivottable.PivotTable(
                                        id='PivotTable_KGL',
                                        data=data_pivot,
                                        cols=['Age'],
                                        rows=['Country'],
                                    )
                                ]
                            )
                        ]
                    ),
                    dcc.Tab(
                        label='Data & Description', style=Tab_deco, selected_style=sel_Tab_deco, children=[
                            html.Div(
                                style={'padding': '0 10px 10px 10px'},
                                children=[
                                    dcc.Tabs(
                                        [
                                            dcc.Tab(
                                                label='Description',
                                                style=Data_Tab,
                                                selected_style=Data_Tab_selected,
                                                children=[
                                                    html.Div(
                                                        className='Data_Tab_Div',
                                                        children=[
                                                            html.Div(
                                                                className='Data_Tab_Div_deco',
                                                                children=[
                                                                    html.H1('Description', className='Data_Tab_title'),
                                                                    html.P("Welcome to Kaggle's annual Machine Learning and Data Science Survey competition! You can read our executive summary here."),
                                                                    html.P("The survey was live from 09/01/2021 to 10/04/2021, and after cleaning the data we finished with 25,973 responses!"),
                                                                    html.P("This year Kaggle is once again launching an annual Data Science Survey Challenge, where we will be awarding a prize pool of $30,000 to notebook authors who tell a rich story about a subset of the data science and machine learning community."),
                                                                    html.P("The challenge objective: tell a data story about a subset of the data science community represented in this survey, through a combination of both narrative text and data exploration. A “story” could be defined any number of ways, and that’s deliberate. The challenge is to deeply explore (through data) the impact, priorities, or concerns of a specific group of data science and machine learning practitioners. That group can be defined in the macro (for example: anyone who does most of their coding in Python) or the micro (for example: female data science students studying machine learning in masters programs). This is an opportunity to be creative and tell the story of a community you identify with or are passionate about!"),
                                                                    html.H3("Submissions will be evaluated on the following:", className='Data_Tab_title'),
                                                                    html.P("▪ Composition - Is there a clear narrative thread to the story that’s articulated and supported by data? The subject should be well defined, well researched, and well supported through the use of data and visualizations."),
                                                                    html.P("▪ Originality - Does the reader learn something new through this submission? Or is the reader challenged to think about something in a new way? A great entry will be informative, thought provoking, and fresh all at the same time."),
                                                                    html.P("▪ Documentation - Are your code, and notebook, and additional data sources well documented so a reader can understand what you did? Are your sources clearly cited? A high quality analysis should be concise and clear at each step so the rationale is easy to follow and the process is reproducible"),
                                                                    html.A('Kaggle Competition Page Link', className='profile_A', href="https://www.kaggle.com/c/kaggle-survey-2021/overview"),
                                                                    html.Br(),
                                                                    html.Br(),
                                                                    html.Br(),
                                                                    html.H1('Timeline', className='Data_Tab_title'),
                                                                    html.P("▪ Submission deadline: November 28th, 2021"),
                                                                    html.P("▪ Winners announced: December 16th, 2021"),
                                                                    html.P("All deadlines are at 11:59 PM UTC on the corresponding day unless otherwise noted. The competition organizers reserve the right to update the contest timeline if they deem it necessary."),
                                                                    html.Br(),
                                                                    html.Br(),
                                                                    html.Br(),
                                                                    html.H1('Prizes', className='Data_Tab_title'),
                                                                    html.P("There will be 5 prizes for the best data storytelling submissions:"),
                                                                    html.P("▪ 1st prize: $10,000"),
                                                                    html.P("▪ 2nd prize: $5,000"),
                                                                    html.P("▪ 3rd prize: $5,000"),
                                                                    html.P("▪ 4th prize: $5,000"),
                                                                    html.P("▪ 5th prize: $5,000"),
                                                                    html.P("Kaggle will also give a Notebook Award of $1,000 to recognize our favorite notebook that gets published prior to 11:59:00 PM UTC on Sunday, November 7th."),
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                ]
                                            ),
                                            dcc.Tab(
                                                label='Data',
                                                style=Data_Tab,
                                                selected_style=Data_Tab_selected,
                                                children=[
                                                    html.Div(
                                                        className='Data_Tab_Div',
                                                        children=[
                                                            html.Div(
                                                                className='Data_Tab_Div_deco',
                                                                children=[
                                                                    html.H1('Data', className='Data_Tab_title'),
                                                                    html.H3('Main Data:'),
                                                                    html.P('kaggle_survey_2021_responses.csv: 42+ questions and 25,973 responses'),
                                                                    html.P("▪ Responses to multiple choice questions (only a single choice can be selected) were recorded in individual columns. Responses to multiple selection questions (multiple choices can be selected) were split into multiple columns (with one column per answer choice)."),
                                                                    html.H3('Supplementary Data:'),
                                                                    html.P('kaggle_survey_2021_answer_choices.pdf: list of answer choices for every question'),
                                                                    html.P("▪ With footnotes describing which questions were asked to which respondents."),
                                                                    html.P('kaggle_survey_2021_methodology.pdf: a description of how the survey was conducted'),
                                                                    html.P("▪ You can ask additional questions by posting in the pinned Q&A thread."),
                                                                    html.H3('Download Data'),
                                                                    html.Form(method='get', action='https://github.com/cincu4221/kagglesurvey2021dashboard/raw/main/data/kaggle-survey-2021.zip',
                                                                        children=[
                                                                            html.Button('Download Data',
                                                                                        type='submit'
                                                                            ),
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                ]
                                            ),
                                            dcc.Tab(
                                                label='Creator',
                                                style=Data_Tab,
                                                selected_style=Data_Tab_selected,
                                                children=[
                                                    html.Div(
                                                        className='Data_Tab_Div',
                                                        children=[
                                                            html.Div(
                                                                className='Data_Tab_Div_deco',
                                                                children=[
                                                                    html.H1('Creator :', className='Data_Tab_title'),
                                                                    html.H2('Jeon WooJeong'),
                                                                    html.A('Simple Profile', href='https://github.com/cincu4221/project', className='profile_A'),
                                                                    html.Br(),html.Br(),
                                                                    html.A('My Github Overview', href='https://github.com/cincu4221', className='profile_A'),
                                                                    html.Br(),html.Br(),
                                                                    html.A("View the submitted notebook", href='https://www.kaggle.com/kwdoku145/the-latest-trends-in-east-asia-japan-and-china', className='profile_A'),
                                                                    html.Br(),html.Br(),
                                                                    html.Form(method='get', action='https://github.com/cincu4221/project/raw/main/Kaggle_Survey_2021/docs/Kaggle_Survey_2021.pdf',
                                                                        children=[
                                                                            html.Button('Download Survey PDF',
                                                                                        type='submit'
                                                                            ),
                                                                        ]
                                                                    ),
                                                                    html.H3('The period of learning data visualization'),
                                                                    html.P("▪ less than 1 months"),
                                                                    html.H3('Production period'),
                                                                    html.P("▪ One week"),
                                                                    html.H3('Programming Language and Library Version Used'),
                                                                    html.P("▪ Python - 3.9.0"),
                                                                    html.P("▪ Pandas - 1.3.5"),
                                                                    html.P("▪ Numpy - 1.21.4"),
                                                                    html.P("▪ Plotly - 5.4.0"),
                                                                    html.H2('References.'),
                                                                    html.A('Heroku Dash Distribute Posting - Evan', href='https://torch-law-f0b.notion.site/Heroku-Dash-Windows-10-b3a5d5e6ecea4ff5a896f18b24c080ab', className='profile_A'),
                                                                    html.Br(),html.Br(),
                                                                    html.A('Interactive Dashboards and Data Apps with Plotly and Dash - Elias Dabbas', href='https://book.naver.com/bookdb/book_detail.naver?bid=20695329', className='profile_A'),
                                                                    html.Br(),html.Br(),
                                                                    html.A('HTML ', href='http://tcpschool.com/html/intro', className='profile_A'),
                                                                    html.A('& ', className='profile_A'),
                                                                    html.A('CSS ', href='http://tcpschool.com/css/intro', className='profile_A'),
                                                                    html.A('- TCP SCHOOL', className='profile_A'),
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                ]
                                            ),
                                        ], className='Data_Tabs'
                                    )
                                ]
                            )
                        ],
                    ),
                ], className='Tabs-cover')
            ], className='Dash-cover'
        )
    ], className='Page-cover'
)




if __name__ == "__main__":
    app.run_server(debug=True)
