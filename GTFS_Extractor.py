import pandas as pd
# import json
import streamlit as st
# import folium as f
# from streamlit_folium import st_folium
# from streamlit_folium import folium_static
# from folium.plugins import Draw
# import geopandas as gpd

# st.set_page_config(layout = 'wide')

# polygons = gpd.read_file('Data/GEOJSONS/states.geojson')

st.header('GTFS Extractor - Germany')

gem_df = pd.read_csv('gem_data.csv', sep = ',')

states = sorted(gem_df['state'].unique())

state_selection = st.selectbox('State', options = states, index = None, placeholder = 'Please choose a state.')

cities = sorted(gem_df[gem_df['state'] == state_selection]['name'].tolist())

city_selection = st.selectbox('Municipality', options = cities, index = None, placeholder = 'Please choose a municipality.')

if state_selection != None and city_selection != None:
    selection = gem_df[(gem_df['state'] == state_selection) & (gem_df['name'] == city_selection)]
    min_x = selection['min_x'].to_list()[0]
    min_y = selection['min_y'].to_list()[0]
    max_x = selection['max_x'].to_list()[0]
    max_y = selection['max_y'].to_list()[0]

    if st.button('Extract GTFS Data'):

    # print(selection['min_x'].to_list()[0])

        stops_df = pd.read_csv('GTFS/stops.txt', sep = ',')

        selection_stops_df = stops_df[(stops_df['stop_lat'] <= max_y) & (stops_df['stop_lat'] >= min_y) & (stops_df['stop_lon'] <= max_x) & (stops_df['stop_lon'] >= min_x)]

        # stops_download = selection_stops_df.to_csv('stops_out.txt', index = False)

        selection_stop_ids = selection_stops_df['stop_id'].unique()

        stop_times_df = pd.read_csv('GTFS/stop_times.txt', sep = ',')

        selection_stop_times_df = stop_times_df[stop_times_df['stop_id'].isin(selection_stop_ids)]

        st.download_button('Download Stops', data = selection_stops_df.to_csv(index = False).encode('utf-8'), file_name = 'stops_out.txt')

# @st.cache_resource
# def get_json(file):
#     with open('Data/GEOJSONS/' + file + '.geojson', encoding = 'utf-8') as input_data:
#         data_dict = json.load(input_data)
#     return data_dict
#
# polygons = get_json('gem_bayern')
#
# st.header('GTFS Extractor')
#
# m = f.Map(location = [51.05535115216956, 10.373332944732669], zoom_start = 6)
# Draw(export=False, draw_options = {'polyline':False, 'polygon':False, 'circle':False, 'circlemarker':False, 'marker':False}).add_to(m)
# f.GeoJson(polygons, tooltip = f.features.GeoJsonTooltip(fields = ['name'], labels = False)).add_to(m)
#
# # st_data = folium_static(m, height = 600, width = 700)
#
# st_data = st_folium(m, height = 600, width = 700)
#
# print(st_data)


# stops_df = pd.read_csv('Data/GTFS/stops.txt', sep = ',')
