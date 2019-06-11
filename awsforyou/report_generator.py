import logging
import os
from datetime import datetime

import jinja2
import pandas as pd


TEMPLATE_FILE = 'template.html'
REPORT_FILE = 'report_{}.html'

LOGGER = logging.getLogger(__name__)


def generate_report(recommendations: pd.DataFrame):
    file_dir = os.path.dirname(os.path.realpath(__file__))
    template_dir = os.path.join(file_dir, 'ui')
    template_loader = jinja2.FileSystemLoader(searchpath=template_dir)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(TEMPLATE_FILE)

    output_text = template.render(recommendation_df=recommendations)
    suffix = datetime.today().strftime('%Y%m%d%H%M%S')
    report_file_name = REPORT_FILE.format(suffix)
    with open(report_file_name, 'w') as report_file:
        report_file.write(output_text)

    LOGGER.info('Created the report file {}'.format(report_file_name))
    return report_file_name
