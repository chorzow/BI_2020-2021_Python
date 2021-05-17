import sqlite3
import pandas as pd
from functools import wraps


def connect(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except sqlite3.Error as e:
            raise e
    return wrapper


def create_connection(db):
    conn = None
    try:
        conn = sqlite3.connect(db)
    except sqlite3.Error as e:
        print(e)
    return conn


@connect
def create_table(conn, create_query):
    c = conn.cursor()
    c.execute(create_query)


@connect
def update_table(conn, update_query):
    c = conn.cursor()
    c.execute(update_query)


@connect
def delete_table(conn, delete_query):
    c = conn.cursor()
    c.execute(delete_query)


def main():
    # read csv files
    genstudio = pd.read_csv('genstudio.csv').drop('Unnamed: 0', axis=1)
    metadata = pd.read_csv('metadata.csv').drop('Unnamed: 0', axis=1)

    # rename columns for convenience
    genstudio.columns = ['SNP_name', 'SNP_id', 'SNP_aux', 'sample_id', 'SNP', 'allele1_top', 'allele2_top',
                         'allele1_forward', 'allele2_forward', 'allele1_AB', 'allele2_AB', 'chr', 'position',
                         'GC_score', 'GT_score', 'theta', 'R', 'B_allele_freq', 'log_R_ratio']

    # make subsets for SQL
    genotypes = genstudio.filter(items=['SNP_name', 'SNP_id', 'SNP_aux', 'sample_id', 'SNP', 'chr', 'position'],
                                 axis=1)
    statistics = genstudio.filter(items=['sample_id', 'SNP_id', 'GC_score', 'GT_score', 'theta', 'R', 'B_allele_freq',
                                         'log_R_ratio'], axis=1)
    alleles = genstudio.filter(items=['sample_id', 'SNP_id', 'allele1_top', 'allele2_top', 'allele1_forward',
                                      'allele2_forward', 'allele1_AB', 'allele2_AB'])

    # define queries
    database = 'SNP.db'

    table_genotypes = """CREATE TABLE IF NOT EXISTS genotypes (
                                    id INTEGER PRIMARY KEY,
                                    SNP_name TEXT,
                                    SNP_id INTEGER,
                                    SNP_aux TEXT,
                                    sample_id TEXT NOT NULL,
                                    SNP TEXT NOT NULL,
                                    chr TEXT NOT NULL,
                                    position INTEGER NOT NULL
                                    );"""

    table_metadata = """CREATE TABLE IF NOT EXISTS metadata (
                                   sample_id INTEGER PRIMARY KEY,
                                   dna_chip_id TEXT NOT NULL,
                                   breed TEXT,
                                   sex TEXT,
                                   FOREIGN KEY (dna_chip_id) REFERENCES genotypes (SNP_aux) ON DELETE CASCADE
                                   );"""

    table_statistics = """CREATE TABLE IF NOT EXISTS statistics (
                                     sample_id INTEGER,
                                     SNP_id INTEGER,
                                     GC_score REAL,
                                     GT_score REAL,
                                     theta REAL,
                                     R REAL,
                                     B_allele_freq REAL,
                                     log_R_ratio REAL,
                                     FOREIGN KEY (sample_id) REFERENCES metadata (sample_id) ON DELETE CASCADE,
                                     FOREIGN KEY (SNP_id) REFERENCES genotypes (SNP_id) ON DELETE CASCADE
                                     );"""

    table_alleles = """CREATE TABLE IF NOT EXISTS alleles (
                                  sample_id INTEGER,
                                  SNP_id INTEGER,
                                  allele1_top TEXT,
                                  allele2_top TEXT,
                                  allele1_forward TEXT,
                                  allele2_forward TEXT,
                                  allele1_AB TEXT,
                                  allele2_AB TEXT,
                                  FOREIGN KEY (sample_id) REFERENCES metadata (sample_id) ON DELETE CASCADE,
                                  FOREIGN KEY (SNP_id) REFERENCES genotypes (SNP_id) ON DELETE CASCADE
                                  );"""

    update_query = """UPDATE genotypes SET chr = 'I' WHERE SNP_aux = '202341831114R01C01'"""
    delete_query = """DELETE FROM alleles WHERE allele1_top = '-'"""

    # create a connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        create_table(conn, table_genotypes)
        create_table(conn, table_metadata)
        create_table(conn, table_statistics)
        create_table(conn, table_alleles)
        # write records to SQL tables
        genotypes.to_sql('genotypes', con=conn, if_exists='append', index=False)
        metadata.to_sql('metadata', con=conn, if_exists='append', index=False)
        statistics.to_sql('statistics', con=conn, if_exists='append', index=False)
        alleles.to_sql('alleles', con=conn, if_exists='append', index=False)
        # commit changes
        conn.commit()
        # update
        update_table(conn, update_query)
        conn.commit()
        # delete
        delete_table(conn, delete_query)
        conn.commit()
        conn.close()
    else:
        print('Cannot create connection with the database.')


if __name__ == '__main__':
    main()
