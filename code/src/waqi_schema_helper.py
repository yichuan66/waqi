from shared_utils import *

class WaqiSchemaHelper:    
    @staticmethod
    def parse_waqi_json_packet_to_csv_row(packet):
        if not packet.get('data'):
            return None

        data = packet['data']
        if not type(data) is dict:
            return None

        # general info
        aqi = ''
        if data.get('aqi'):
            aqi = str(data['aqi'])

        station_index = ''
        if data.get('idx'):
            station_index = str(data['idx'])

        latitude = ''
        longitude = ''
        city_name = ''
        city_url = ''
        if data.get('city'):
            city = data['city']
            if city.get('geo'):
                if len(city['geo']) == 2:
                    latitude = str(city['geo'][0])
                    longitude = str(city['geo'][1])
            if city.get('name'):
                city_name = city['name']
            if city.get('url'):
                city_name = city['url']
                
        date_time = ''
        if data.get('time'):
            if data['time'].get('s'):
                date_time = data['time']['s']

        time_zone = ''
        if data.get('time'):
            if data['time'].get('tz'):
                time_zone = data['time']['tz']

        row = [
            station_index,
            latitude,
            longitude,
            date_time,
            time_zone,
            aqi,
            city_name,
            city_url,
        ]

        # pollution info
        dominant_pollution = ''
        if data.get('dominentpol'):
            dominant_pollution = data['dominentpol']
        row.append(dominant_pollution)

        detailed_pollution = None
        if data.get('iaqi'):
            detailed_pollution = data['iaqi']
            
        for item in WaqiSchemaHelper._pollution_list:
            if not detailed_pollution or not detailed_pollution.get(item):
                row.append('')
            else:
                row.append(str(detailed_pollution[item]['v']))             
        return row

    @staticmethod
    def is_valid_row(row):
        if len(row) != len(WaqiSchemaHelper.schema):
            return False

        for i in range(len(row)):
            field_name = WaqiSchemaHelper.schema[i]
            item = row[i]
            if type(item) != str:
                return False

            if field_name == WaqiSchemaHelper.station_index:
                if not item.isdigit():
                    return False
            elif field_name == WaqiSchemaHelper.latitude:
                if not is_valid_latitude(item):
                    return False
            elif field_name == WaqiSchemaHelper.longitude:
                if not is_valid_longitude(item):
                    return False
            elif field_name == WaqiSchemaHelper.date_time:
                if item == None or item == '':
                    return False
            elif field_name == WaqiSchemaHelper.time_zone:
                if item == None or item == '':
                    return False
            elif field_name == WaqiSchemaHelper.aqi:
                if not item.isdigit():
                    return False
            elif field_name == WaqiSchemaHelper.city_name:
                if item == None or item == '':
                    return False
            elif field_name == WaqiSchemaHelper.dominant_pollution:
                if item not in WaqiSchemaHelper._pollution_list:
                    return False

        return True

     # variables
    station_index = 'station_index'
    latitude = 'latitude'
    longitude = 'longitude'
    date_time = 'date_time'
    time_zone = 'time_zone'
    aqi = 'aqi'
    city_name = 'city_name'
    city_url = 'city_url'
    dominant_pollution = 'dominant_pollution'
    pollution_co = 'pollution_co'
    pollution_dew = 'pollution_dew'
    pollution_h = 'pollution_h'
    pollution_o3 = 'pollution_o3'
    pollution_p = 'pollution_p'
    pollution_pm10 = 'pollution_pm10'
    pollution_pm25 = 'pollution_pm25'
    pollution_r = 'pollution_r'
    pollution_so2 = 'pollution_so2'
    pollution_t = 'pollution_t'

    schema = [   
        station_index,
        latitude,
        longitude,
        date_time,
        time_zone,
        aqi,
        city_name,
        city_url,
        dominant_pollution,
        pollution_co,
        pollution_dew,
        pollution_h,
        pollution_o3,
        pollution_p,
        pollution_pm10,
        pollution_pm25,
        pollution_r,
        pollution_so2,
        pollution_t]
    
    _pollution_list = [
            'co',
            'dew',
            'h',
            'o3',
            'p',
            'pm10',
            'pm25',
            'r',
            'so2',
            't']
