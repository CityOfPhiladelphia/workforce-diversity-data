import csv
import sys
import logging
from logging.config import dictConfig

import click
import yaml
from sqlalchemy import create_engine
from smart_open import smart_open

csv.field_size_limit(sys.maxsize)

BATCH_SIZE = 10000

def get_logger(logging_config):
    try:
        with open(logging_config) as file:
            config = yaml.load(file)
        dictConfig(config)
    except:
        FORMAT = '[%(asctime)-15s] %(levelname)s [%(name)s] %(message)s'
        logging.basicConfig(format=FORMAT, level=logging.INFO, stream=sys.stderr)

    logger = logging.getLogger('workforce-diversity-extract')

    def exception_handler(type, value, tb):
        logger.exception("Uncaught exception: {}".format(str(value)), exc_info=(type, value, tb))

    sys.excepthook = exception_handler

    return logger

def fopen(file, mode='r'):
    if file == None:
        if mode == 'r':
            return sys.stdin
        elif mode == 'w':
            return sys.stdout
    else:
        return smart_open(file, mode=mode, encoding='utf-8')

@click.command()
@click.argument('connection-string')
@click.argument('table')
@click.option('--output-file')
@click.option('--logging-config', default='logging_config.conf')
def main(connection_string, table, output_file, logging_config):
    logger = get_logger(logging_config)

    logger.info('Extracting {}'.format(table))

    try:
        engine = create_engine(connection_string)

        with fopen(output_file, mode='w') as file:
            writer = csv.writer(file)

            conn = engine.raw_connection()
            cur = conn.cursor()

            cur.execute('select * from {}'.format(table))

            headers = []
            for field in cur.description:
                headers.append(field[0].lower())

            writer.writerow(headers)

            count = 0
            rows = cur.fetchmany(BATCH_SIZE)
            while rows:
                logger.info('Fetched batch of {} rows'.format(BATCH_SIZE))
                for row in rows:
                    outrow = []
                    for cell in row:
                        if cell == '\x00':
                            outrow.append(None)
                        else:
                            outrow.append(cell)
                    writer.writerow(outrow)
                count += len(rows)
                rows = cur.fetchmany(BATCH_SIZE)

            logger.info('Extracted {} rows'.format(count))
    except:
        logger.exception('Exception extracting {}'.format(table))
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    main()
