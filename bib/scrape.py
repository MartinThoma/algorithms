#!/usr/bin/env python

"""Get data of seat estimations for KIT libraries."""

import os
import json
import urllib2
import sqlite3

import logging
import sys

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def main():
    """Orchestrate."""
    path_to_db = "data.db"
    if not os.path.isfile(path_to_db):
        logging.info("Database '%s' was not found. Create it.", path_to_db)
        create_db(path_to_db)
    locations = ['LSG', 'LST', 'LSW', 'LSM', 'LSN', 'LBS', 'FBC', 'LAF',
                 'FBW', 'FBM', 'FBP', 'FBI', 'FBA', 'BIB-N', 'FBH', 'FBD',
                 'TheaBib']
    for location in locations:
        logging.info("Get data for '%s'", location)
        for weeks in range(1, 140):
            logging.info("Week %i", weeks)
            tables = ['seatestimate', 'manualcount', 'wlanclients', 'ltaports']
            for table in tables:
                data = get_data(location, weeks, nr_type=table)
                add_data(path_to_db, data, table)


def create_db(path_to_db):
    """
    Create SQLite DB.

    Parameters
    ----------
    path_to_db : str
    """
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()
    sql = ("CREATE TABLE IF NOT EXISTS `seatestimate` ("
           "`date_str` varchar(20) NOT NULL,"
           "`timezone_type` varchar(2) NOT NULL,"
           "`timezone` varchar(50) NOT NULL,"
           "`location_name` varchar(255) NOT NULL,"
           "`free_seats` int(11) NOT NULL,"
           "`occupied_seats` int(11) NOT NULL, "
           "PRIMARY KEY(date_str, location_name)"
           ");")
    cur.execute(sql)
    sql = ("CREATE TABLE IF NOT EXISTS `manualcount` ("
           "`date_str` varchar(20) NOT NULL,"
           "`timezone_type` varchar(2) NOT NULL,"
           "`timezone` varchar(50) NOT NULL,"
           "`location_name` varchar(255) NOT NULL,"
           "`free_seats` int(11) NOT NULL,"
           "`occupied_seats` int(11) NOT NULL, "
           "PRIMARY KEY(date_str, location_name)"
           ");")
    cur.execute(sql)
    sql = ("CREATE TABLE IF NOT EXISTS `wlanclients` ("
           "`date_str` varchar(20) NOT NULL,"
           "`timezone_type` varchar(2) NOT NULL,"
           "`timezone` varchar(50) NOT NULL,"
           "`location_name` varchar(255) NOT NULL,"
           "`number_of_clients` int(11) NOT NULL,"
           "PRIMARY KEY(date_str, location_name)"
           ");")
    cur.execute(sql)
    sql = ("CREATE TABLE IF NOT EXISTS `ltaports` ("
           "`date_str` varchar(20) NOT NULL,"
           "`timezone_type` varchar(2) NOT NULL,"
           "`timezone` varchar(50) NOT NULL,"
           "`location_name` varchar(255) NOT NULL,"
           "`number_of_ports` int(11) NOT NULL,"
           "PRIMARY KEY(date_str, location_name)"
           ");")
    cur.execute(sql)


def get_data(location, weeks=1, nr_type='seatestimate'):
    """
    Get all available data for the given location.

    Parameters
    ----------
    location : LSG,LST,LSW,LSM,LSN,LBS,FBC,LAF,FBW,FBM,FBP,FBI,FBA,
               BIB-N,FBH,FBD,TheaBib
    weeks : int
    nr_type : manualcount,seatestimate,wlanclients,ltaports

    """
    url = ("http://seatfinder.bibliothek.kit.edu/karlsruhe/getdata.php?"
           "values[0]={table}"
           "&location[0]={location}"
           "&after[0]=-{weeks}weeks"
           "&limit[0]=20000"
           "&legend[0]=true").format(table=nr_type,
                                     location=location,
                                     weeks=weeks)
    loaded = json.load(urllib2.urlopen(url))[0][nr_type]
    return loaded[location]


def add_data(path_to_db, data, table):
    """Add the data to the database."""
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()
    for el in data:
        if table in ['seatestimate', 'manualcount']:
            sql = ("INSERT INTO `{table}` "
                   "(`date_str`, `timezone_type`, `timezone`, "
                   "`location_name`, "
                   "`free_seats`, `occupied_seats`) "
                   "VALUES ('{date}', '{timezone_type}', "
                   "'{timezone}', '{location_name}',"
                   "'{free_seats}', '{occupied_seats}');"
                   "").format(table=table,
                              date=el['timestamp']['date'],
                              timezone_type=el['timestamp']['timezone_type'],
                              timezone=el['timestamp']['timezone'],
                              location_name=el['location_name'],
                              occupied_seats=el['occupied_seats'],
                              free_seats=el['free_seats'])
        else:
            row_counter = 'number_of_ports'
            if table == 'wlanclients':
                row_counter = 'number_of_clients'

            sql = ("INSERT INTO `{table}` "
                   "(`date_str`, `timezone_type`, `timezone`, "
                   "`location_name`, `{row_counter}`) "
                   "VALUES ('{date}', '{timezone_type}', "
                   "'{timezone}', '{location_name}',"
                   "'{counter}');"
                   "").format(table=table,
                              row_counter=row_counter,
                              date=el['timestamp']['date'],
                              timezone_type=el['timestamp']['timezone_type'],
                              timezone=el['timestamp']['timezone'],
                              location_name=el['location_name'],
                              counter=el[row_counter])
        try:
            cur.execute(sql)
        except sqlite3.IntegrityError:
            pass  # This data is already in the DB. Just ignore it.
    con.commit()
    con.close()


if __name__ == '__main__':
    main()
