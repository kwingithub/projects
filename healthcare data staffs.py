# %%
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# 初始化 Dash 应用
app = dash.Dash(__name__)

# 示例数据集
data_1 = {
    'Region': ['全国', '全国', '全国', '北京', '北京', '北京', '天津', '天津', '天津', '河北', '河北', '河北', 
               '山西', '山西', '山西'],
    'Year': [2023, 2022, 2021, 2023, 2022, 2021, 2023, 2022, 2021, 2023, 2022, 2021, 
             2023, 2022, 2021],
    'Health_Workers': [13474992, 13985363, 14410844, 348066, 361004, 368629, 143185, 152473, 154995, 
                       674956, 710338, 732878, 351369, 362910, 364389]
}

data_2 = {
    'Region': ['全国', '全国', '全国', '北京', '北京', '北京', '天津', '天津', '天津', '河北', '河北', '河北', 
               '山西', '山西', '山西'],
    'Year': [2023, 2022, 2021, 2023, 2022, 2021, 2023, 2022, 2021, 2023, 2022, 2021, 
             2023, 2022, 2021],
    'Healthcare_Institutions': [1070800, 1032918, 1030935, 12518, 10897, 10699, 6801, 6282, 6076, 
                                92825, 90194, 88162, 41140, 41007, 39661]
}

data_3 = {
    'Region': ['全国', '全国', '全国', '北京', '北京', '北京', '天津', '天津', '天津', '河北', '河北', '河北', 
               '山西', '山西', '山西'],
    'Year': [2023, 2022, 2021, 2023, 2022, 2021, 2023, 2022, 2021, 2023, 2022, 2021, 
             2023, 2022, 2021],
    'Healthcare_Services': [95.6, 84.16, 77.41, 5.6, 7.1, 8.2, 1.1, 2.5, 3.3, 1.9, 2.2, 3.4, 
                            1.0, 2.0, 2.5]
}

df_1 = pd.DataFrame(data_1)
df_2 = pd.DataFrame(data_2)
df_3 = pd.DataFrame(data_3)

df = pd.merge(df_1, df_2, on=['Region', 'Year'], how='outer')
df = pd.merge(df, df_3, on=['Region', 'Year'], how='outer')

# 地图面板：按指标选择的地理可视化
fig_map = px.choropleth(df, 
                        locations='Region', 
                        color='Health_Workers', 
                        hover_name='Region', 
                        color_continuous_scale="Viridis", 
                        labels={'Health_Workers': 'Healthcare Workers'},
                        title="Healthcare Workers Distribution by Region")

# 趋势分析面板：按年份展示医院数量柱状图
fig_trend = px.bar(df, x='Year', y='Healthcare_Institutions', color='Year',
                   title='Healthcare Institutions by Year', labels={'Healthcare_Institutions': 'Healthcare Institutions'})

# 数据比较面板：选择多个省份并展示医疗资源对比的散点图
fig_comparison = px.scatter(df[df['Year'] == 2023], x='Health_Workers', y='Healthcare_Institutions', 
                            size='Healthcare_Services', color='Region', hover_name='Region', 
                            title='Comparison of Healthcare Resources by Region (2023)', 
                            labels={'Health_Workers': 'Healthcare Workers', 'Healthcare_Institutions': 'Healthcare Institutions'})

# Dash Layout
app.layout = html.Div([
    html.H1("Healthcare Data Analysis"),
    
    # 地图面板：选择指标
    html.Div([
        html.Label('Select Indicator for Map:'),
        dcc.Dropdown(
            id='indicator-dropdown',
            options=[
                {'label': 'Healthcare Workers', 'value': 'Health_Workers'},
                {'label': 'Healthcare Institutions', 'value': 'Healthcare_Institutions'},
                {'label': 'Healthcare Services', 'value': 'Healthcare_Services'}
            ],
            value='Health_Workers'
        ),
        dcc.Graph(id='map-graph', figure=fig_map)
    ], style={'width': '48%', 'display': 'inline-block'}),
    
    # 趋势分析面板：选择年份
    html.Div([
        html.Label('Select Year for Trend Analysis:'),
        dcc.Dropdown(
            id='year-dropdown',
            options=[
                {'label': '2021', 'value': 2021},
                {'label': '2022', 'value': 2022},
                {'label': '2023', 'value': 2023}
            ],
            value=2023
        ),
        dcc.Graph(id='trend-graph', figure=fig_trend)
    ], style={'width': '48%', 'display': 'inline-block'}),
    
    # 数据比较面板：选择省份
    html.Div([
        html.Label('Select Regions for Comparison:'),
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': region, 'value': region} for region in df['Region'].unique()],
            value=['北京', '天津'],
            multi=True
        ),
        dcc.Graph(id='comparison-graph', figure=fig_comparison)
    ], style={'width': '100%', 'display': 'inline-block'})
])

# 回调函数：根据下拉选择动态更新图表
@app.callback(
    Output('map-graph', 'figure'),
    [Input('indicator-dropdown', 'value')]
)
def update_map(selected_indicator):
    fig = px.choropleth(df, 
                        locations='Region', 
                        color=selected_indicator, 
                        hover_name='Region', 
                        color_continuous_scale="Viridis", 
                        labels={selected_indicator: selected_indicator.replace('_', ' ')},
                        title=f"{selected_indicator.replace('_', ' ').capitalize()} Distribution by Region")
    return fig

@app.callback(
    Output('trend-graph', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_trend(selected_year):
    filtered_df = df[df['Year'] == selected_year]
    fig = px.bar(filtered_df, x='Region', y='Healthcare_Institutions', color='Region',
                 title=f'Healthcare Institutions in {selected_year}', labels={'Healthcare_Institutions': 'Healthcare Institutions'})
    return fig

@app.callback(
    Output('comparison-graph', 'figure'),
    [Input('region-dropdown', 'value')]
)
def update_comparison(selected_regions):
    filtered_df = df[df['Region'].isin(selected_regions)]
    fig = px.scatter(filtered_df, x='Health_Workers', y='Healthcare_Institutions', size='Healthcare_Services', 
                     color='Region', hover_name='Region', 
                     title='Comparison of Healthcare Resources by Region',
                     labels={'Health_Workers': 'Healthcare Workers', 'Healthcare_Institutions': 'Healthcare Institutions'})
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)




