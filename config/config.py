import glob
import os

from jinja2 import Environment, FileSystemLoader

def generate():
    datasets = [os.path.basename(x).split('.json')[0] for x in glob.glob("datasets/*.json")]
    sites = filter(lambda x: x != 'global', next(os.walk('sites/'))[1])

    env = Environment(loader=FileSystemLoader('config/'), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('config.j2')
    
    return template.render({"datasets": datasets, "sites": sites})    
