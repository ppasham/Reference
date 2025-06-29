# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 20:24:45 2025

@author: prash
"""

#
# Streamlit equivalent of final Gradio app
#
import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import datetime
import psycopg2
# from psycopg2 import sql
# from psycopg2 import pool

# Initialize connection pool
try:
    connection_pool = psycopg2.pool.ThreadedConnectionPool(
        minconn=5,
        maxconn=20,
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
except psycopg2.Error as e:
    st.error(f"Error creating connection pool: {e}")


def get_connection():
    try:
        return connection_pool.getconn()
    except psycopg2.Error as e:
        st.error(f"Error getting connection from pool: {e}")
        return None


def release_connection(conn):
    try:
        connection_pool.putconn(conn)
    except psycopg2.Error as e:
        st.error(f"Error releasing connection back to pool: {e}")
