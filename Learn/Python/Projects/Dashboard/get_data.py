# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 18:20:25 2025

@author: prash
"""
import dbConnect
# import pandasql
# import datetime
# import psycopg2
from psycopg2 import sql
# from psycopg2 import pool


class query:

    # def get_data(queryname):
    # return sqldf(query, locals())

    def _get_date_range(self):
        conn = dbConnect.get_connection()
        if conn is None:
            return None, None
        try:
            with conn.cursor() as cur:
                query = sql.SQL(self.Q_DATE_RANGE)
                cur.execute(query)
                return cur.fetchone()
        finally:
            dbConnect.release_connection(conn)

    def _get_unique_categories(self):
        conn = dbConnect.get_connection()
        if conn is None:
            return []
        try:
            with conn.cursor() as cur:
                query = sql.SQL(self.Q_UNIQUE_CATEGORIES)
                cur.execute(query)
                return [row[0].capitalize() for row in cur.fetchall()]
        finally:
            dbConnect.release_connection(conn)

    def _get_dashboard_stats(self, start_date, end_date, category):
        conn = dbConnect.get_connection()
        if conn is None:
            return None
        try:
            with conn.cursor() as cur:
                query = sql.SQL(self.Q_DASHBOARD_STATS)
                cur.execute(query, [start_date, end_date, category, category,
                                    start_date, end_date, category, category])
                return cur.fetchone()
        finally:
            dbConnect.release_connection(conn)
