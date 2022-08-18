from entsoe import EntsoeRawClient, EntsoePandasClient
import pandas as pd
#Country codes
    # Country_Codes
    # 'DE': '10Y1001A1001A63L',  # DE-AT-LU
    # 'LU': '10Y1001A1001A63L',  # DE-AT-LU
    # 'IT_NORD': '10Y1001A1001A73I',
    # 'IT_CNOR': '10Y1001A1001A70O',
    # 'IT_CSUD': '10Y1001A1001A71M',
    # 'IT_SUD': '10Y1001A1001A788',
    # 'IT_FOGN': '10Y1001A1001A72K',
    # 'IT_ROSN': '10Y1001A1001A77A',
    # 'IT_BRNN': '10Y1001A1001A699',
    # 'IT_PRGP': '10Y1001A1001A76C',
    # 'IT_SARD': '10Y1001A1001A74G',
    # 'IT_SICI': '10Y1001A1001A75E',
    # 'IT_CALA': '10Y1001C--00096J',
    # 'NO_1': '10YNO-1--------2',
    # 'NO_2': '10YNO-2--------T',
    # 'NO_3': '10YNO-3--------J',
    # 'NO_4': '10YNO-4--------9',
    # 'NO_5': '10Y1001A1001A48H',
    # 'SE_1': '10Y1001A1001A44P',
    # 'SE_2': '10Y1001A1001A45N',
    # 'SE_3': '10Y1001A1001A46L',
    # 'SE_4': '10Y1001A1001A47J',
    # 'DK_1': '10YDK-1--------W',
    # 'DK_2': '10YDK-2--------M'


    # Country_code (ex 'NO_1', 'DK_2', 'DE') - startedate(ex '20201230')  - enddate(ex '20210130)
    # Timezone is Brussels

def spot_market_API_enstoe(contry_code, startdate, enddate):

    client = EntsoePandasClient(api_key='00cacba3-44b1-475b-bba7-7fa7419d7451')

    start = pd.Timestamp(startdate, tz='Europe/Oslo')
    end = pd.Timestamp(enddate, tz='Europe/Oslo')
    country_code = contry_code  # Belgium
    #country_code_from = 'FR'  # France
    #country_code_to = 'DE_LU' # Germany-Luxembourg
    type_marketagreement_type = 'A01'

    # methods that return XML
    client.query_day_ahead_prices(country_code, start=start, end=end)

    # xml_string = client.query_day_ahead_prices(country_code, start=start, end=end)

    ts = client.query_day_ahead_prices(country_code, start=start, end=end)
    ts = pd.DataFrame(ts)

    #ts.to_csv('outfile.csv')
    # with open('outfile.xml', 'w') as f:
    #      f.write(xml_string)
    return ts

ts = spot_market_API_enstoe(contry_code='NO_3', startdate='20210908', enddate='20210909')