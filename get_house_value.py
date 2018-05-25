from zoopla import Zoopla
import get_config

cfg = get_config.cfg['zoopla']

zoopla_api_key=cfg['key']

zoopla = Zoopla(api_key=zoopla_api_key)

average = zoopla.average_area_sold_price({'area': 'NR20', 'output_type': 'outcode'})
print(average.average_sold_price_7year)
print(average.average_sold_price_5year)
