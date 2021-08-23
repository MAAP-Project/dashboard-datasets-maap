from matplotlib import pyplot as plt
from PyInquirer import prompt, print_json, Separator

import matplotlib
import random as rd

import json
import re
import urllib


# ======================================================================#
#                           VARIABLES                                   #
# ======================================================================#

CATEGORICAL = 'categorical'
GRADIENT = 'gradient'
RASTER = 'raster'
VECTOR = 'vector'
MOSAICJSON = 'mosaicjson'
GEOTIFF = 'geotiff'

# ======================================================================#
#                   UTILITY FUNCTIONS                                   #
# ======================================================================#

def to_camel_case(text):
  return ''.join(a.capitalize() for a in re.split('([^a-zA-Z0-9])', text)
       if a.isalnum())

def to_snake_case(text):
  camel_case = to_camel_case(text)
  return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_case).lower()

def create_color_stops_from_cmap(cmap_name):
  cmap = matplotlib.cm.get_cmap(cmap_name, 12)
  colors = [matplotlib.colors.to_hex(cmap(i)) for i in range(cmap.N)]
  return colors

def get_mapping(x):
  return {
    MOSAICJSON: {
      'endpoint': MOSAICJSON,
      'url': x.get(f'{MOSAICJSON}_url')
    },
    GEOTIFF: {
      'endpoint': 'cog',
      'url': x.get(f'{GEOTIFF}_url')
    }
  }

def create_source(answers):
  mapping = get_mapping(answers)
  source = {
    'type': answers['type']
  }
  if answers['type'] == RASTER:
    params = ['bidx', 'rescale', 'resampling_method', 'colormap_name']
    url_params = { k: answers[k] for k in params if (k in answers and answers.get(k))}
    url_encoded = urllib.parse.urlencode(url_params)
    key = answers['url_type']
    source['tiles'] = [
      f'{{titiler_server_url}}/{mapping[key]["endpoint"]}/tiles/{{z}}/{{x}}/{{y}}.png?url={mapping[key]["url"]}&{url_encoded}'
    ]
  else:
    source['tiles'] = [
      f'{{vector_tileserver_url}}/{answers.get("mbtiles_url")}/{{z}}/{{x}}/{{y}}.pbf'
    ]
  return source

def create_legend(answers):
  legend = {
    'type': answers.get('legend_type'),
    'min': answers.get('data_min'),
    'max': answers.get('data_max'),
    'stops': create_color_stops_from_cmap(answers.get('cmap')) if answers.get('cmap') else ''
  }
  return legend

def create_swatch(answers):
  r_gen = lambda: rd.randint(0, 255)
  swatch = {
    'color': f'#{r_gen():02x}{r_gen():02x}{r_gen():02x}'
  }
  return swatch

def clean_json(answers):
  skip = ['url_type', 'mosaicjson_url', 'tif_url', 'legend_type', 'data_min', 'data_max', 'cmap', 'raster_opacity', 'resampling_method', 'colormap_name', 'rescale', 'bidx']
  for skippable in skip:
    try:
      answers.pop(skippable)
    except:
      continue
  return answers

def create_json(answers):
  answers['id'] = to_snake_case(answers['name'])
  answers['source'] = create_source(answers)
  answers['is_periodic'] = False
  answers['time_unit'] = 'day'
  answers['legend'] = create_legend(answers)
  answers['swatch'] = create_swatch(answers)
  answers['paint'] = {
    'raster-opacity': answers['raster_opacity']
  }
  answers = clean_json(answers)
  return answers

# ======================================================================#
#                   VALIDATION FUNCTIONS                                #
# ======================================================================#

def is_integer(n):
  try:
    int(n)
  except ValueError:
    return "The value should be an integer."
  return True

def is_number(n):
  try:
      float(n)
  except ValueError:
      return "The value should be a number."
  return True

def is_mosaicjson_url(url):
  if url.endswith('.json'):
    return True
  return False

def is_tif_url(url):
  if url.endswith('.tif') or url.endswith('.tiff'):
    return True
  return False

def is_valid_cmap(cmap):
  valid_cmaps = plt.colormaps()
  if cmap in valid_cmaps or cmap == '':
    return True
  return f'Invalid CMAP. Choose from {valid_cmaps}'

def is_valid_colormap(cmap):
  valid_cmaps = [
      'above', 'accent', 'accent_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'blues', 'blues_r', 'bone', 'bone_r', 'brbg', 'brbg_r', 'brg', 'brg_r', 'bugn', 'bugn_r', 'bupu', 'bupu_r', 'bwr', 'bwr_r', 'cfastie', 'cividis', 'cividis_r', 'cmrmap', 'cmrmap_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'dark2', 'dark2_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnbu', 'gnbu_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'greens', 'greens_r', 'greys', 'greys_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'oranges', 'oranges_r', 'orrd', 'orrd_r', 'paired', 'paired_r', 'pastel1', 'pastel1_r', 'pastel2', 'pastel2_r', 'pink', 'pink_r', 'piyg', 'piyg_r', 'plasma', 'plasma_r', 'prgn', 'prgn_r', 'prism', 'prism_r', 'pubu', 'pubu_r', 'pubugn', 'pubugn_r', 'puor', 'puor_r', 'purd', 'purd_r', 'purples', 'purples_r', 'rainbow', 'rainbow_r', 'rdbu', 'rdbu_r', 'rdgy', 'rdgy_r', 'rdpu', 'rdpu_r', 'rdylbu', 'rdylbu_r', 'rdylgn', 'rdylgn_r', 'reds', 'reds_r', 'rplumbo', 'schwarzwald', 'seismic', 'seismic_r', 'set1', 'set1_r', 'set2', 'set2_r', 'set3', 'set3_r', 'spectral', 'spectral_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r', 'wistia', 'wistia_r', 'ylgn', 'ylgn_r', 'ylgnbu', 'ylgnbu_r', 'ylorbr', 'ylorbr_r', 'ylorrd', 'ylorrd_r'
  ]
  if cmap in valid_cmaps or cmap == '':
    return True
  return f'Invalid colormap name. Choose from {valid_cmaps}'

def is_valid_resampling_method(input_value):
    valid_values = ['nearest', 'bilinear', 'cubic', 'cubic_spline', 'lanczos', 'average', 'mode', 'gauss', 'max', 'min', 'med', 'q1', 'q3']
    if input_value in valid_values:
        return True
    return f'Invalid resampling method. Choose from {valid_values}'

# ======================================================================#
#                           QUESTIONS                                   #
# ======================================================================#


questions = [
  {
    'type': 'input',
    'name': 'name',
    'message': 'Dataset name:',
  },
  {
    'type': 'list',
    'name': 'type',
    'message': 'Data type:',
    'choices': [RASTER, VECTOR],
    'default': RASTER
  },
  {
    'type': 'input',
    'name': 'info',
    'message': 'Dataset info:'
  },
  {
    'type': 'input',
    'name': 'order',
    'message': 'Dataset order:',
    'validate': is_integer
  },
  {
    'type': 'list',
    'name': 'url_type',
    'message': 'URL type:',
    'choices': [GEOTIFF, MOSAICJSON]
  },
  {
    'type': 'input',
    'name': 'mosaicjson_url',
    'message': 'Mosaicjson url:',
    'validate': is_mosaicjson_url,
    'when': lambda answers: answers.get('type') == RASTER and answers.get('url_type') == MOSAICJSON
  },
  {
    'type': 'input',
    'name': 'geotiff_url',
    'message': 'Geotiff url:',
    'validate': is_tif_url,
    'when': lambda answers: answers.get('type') == RASTER and answers.get('url_type') == GEOTIFF
  },
  {
    'type': 'input',
    'name': 'bidx',
    'message': 'Titiler param: band index (bidx)',
    'validate': lambda x: x=='' or is_integer(x),
    'when': lambda answers: answers.get('type') == RASTER
  },
  {
    'type': 'input',
    'name': 'resampling_method',
    'message': 'Titiler param: resampling method (resampling_method)',
    'validate': lambda x: is_valid_resampling_method(x) or x=='',
    'when': lambda answers: answers.get('type') == RASTER
  },
  {
    'type': 'input',
    'name': 'rescale',
    'message': 'Titiler param: comma delimited Min,Max bounds (rescale)',
    'when': lambda answers: answers.get('type') == RASTER
  },
  {
    'type': 'input',
    'name': 'colormap_name',
    'message': 'Titiler param: Colormap name (colormap_name)',
    'validate': lambda x: is_valid_colormap(x) or x=='',
    'when': lambda answers: answers.get('type') == RASTER
  },
  {
    'type': 'input',
    'name': 'mbtiles_url',
    'message': 'MB Tiles url:',
    'when': lambda answers: answers.get('type') == VECTOR
  },
  {
    'type': 'list',
    'name': 'legend_type',
    'message': 'Legend type:',
    'choices': [CATEGORICAL, GRADIENT]
  },
  {
    'type': 'input',
    'name': 'data_min',
    'message': 'Data minimum:',
    'validate': is_number
  },
  {
    'type': 'input',
    'name': 'data_max',
    'message': 'Data max:',
    'validate': is_number
  },
  {
    'type': 'input',
    'name': 'cmap',
    'message': 'If using matplotlib cmap, enter the name:',
    'validate': is_valid_cmap,
    'default': '',
    'when': lambda answers: answers.get('legend_type') == GRADIENT
  },
  {
    'type': 'input',
    'name': 'color_stops',
    'message': 'Comma separated list of color hex (eg. #FFFFF, #FEFEFE, #EEEEEE)',
    'default': '',
    'filter': lambda x: x.split(','),
    'when': lambda answers: answers.get('legend_type') == GRADIENT and (not answers.get('cmap'))
  },
  {
    'type': 'input',
    'name': 'categorical_color_stops',
    'message': 'Comma separated list of hex: label (eg. #FFFFF: Winter, #FEFEFE: Summer, #EEEEEE: Spring)',
    'default': '',
    'filter': lambda input_string: [{'color': x.split(':')[0].strip(), 'label': x.split(':')[1].strip()} for x in input_string.split(',')],
    'when': lambda answers: answers.get('legend_type') == CATEGORICAL
  },
  {
    'type': 'input',
    'name': 'raster_opacity',
    'message': 'Opacity of the raster in map:',
    'validate': lambda x: is_number(x) and (float(x) >= 0 and float(x) <= 1),
    'default': '1'
  }
]


if __name__=="__main__":
    print('''
        Hi!
        This interactive script is meant to help you create the json for a dataset for the dashboard.
        Before using this, make sure you go through the notebook `test_raster_dataset.ipynb` and determine your visualization is working.

        The dataset json file is created inside the `../datasets/` folder.

        You can create/edit the json file yourself too.
        ''')
    answers = prompt(questions)
    generated_json = create_json(answers)

    with open(f'../datasets/{generated_json["id"]}.json', 'w') as fp:
        json.dump(generated_json, fp)
