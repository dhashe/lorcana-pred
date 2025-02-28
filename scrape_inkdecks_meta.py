#!/usr/bin/env python3

import re
import requests
from bs4 import BeautifulSoup
import sqlite3
import os

# SQLite database file name
db_name = "inkdecks_meta_cards.db"

if os.path.exists(db_name):
    os.remove(db_name)

directory = "./meta_decks"
for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)
    if os.path.isfile(filepath):  # Check if it's a file
        print(filename)

    # Open the webpage
    with open(filepath) as f:
        text = f.read()

    # Parse the webpage using BeautifulSoup
    soup = BeautifulSoup(text, 'html.parser')

    # Find the target subtree with the class "card-title text-theme mt-4"
    h2_element = soup.find('h2', class_="card-title text-theme mt-4", string="Key Cards")
    if not h2_element:
        raise Exception("Target <h2> element not found.")

    # Find the <table> element within the subtree
    table = h2_element.find_next('table', class_="table table-responsive table-condensed sortable")
    if not table:
        raise Exception("Target <table> element not found.")

    # Extract rows from the table with the specified class
    rows = table.find_all('tr', class_="card-list-item")
    if not rows:
        raise Exception("No rows found in the table.")

    # Extract data from each row and prepare for database insertion
    data = []
    for row in rows:
        quantity = row.get('data-quantity')
        image_src = row.get('data-image-src')
        if quantity and image_src:
            # Extract the 4th and 5th components from the image_src
            parts = image_src.split('/')
            if len(parts) >= 6:
                set_code = parts[4]  # 4th item (1-indexed)
                match = re.match(r'(\d+)-', parts[5])  # Extract the first number in the 5th item
                card_number = match.group(1) if match else None
                if card_number:
                    data.append((filename, int(quantity), image_src, set_code, card_number))

    # Process the second table for "Less Frequent Cards Included"
    h2_element_less_frequent = soup.find('h2', class_="card-title text-theme mt-4", string="Less Frequent Cards Included")
    if h2_element_less_frequent:
        table_less_frequent = h2_element_less_frequent.find_next('table', class_="table table-responsive table-condensed sortable")
        if table_less_frequent:
            rows_less_frequent = table_less_frequent.find_all('tr', class_="card-list-item")
            for row in rows_less_frequent:
                quantity = row.get('data-quantity')
                image_src = row.get('data-image-src')
                if quantity and image_src:
                    # Check the value in the 4th <td> element
                    cells = row.find_all('td')
                    if len(cells) >= 4:
                        sort_value = cells[3].get('data-sort')
                        if sort_value and float(sort_value) >= 20:
                            # Extract the 4th and 5th components from the image_src
                            parts = image_src.split('/')
                            if len(parts) >= 6:
                                set_code = parts[4]  # 4th item (1-indexed)
                                match = re.match(r'(\d+)-', parts[5])  # Extract the first number in the 5th item
                                card_number = match.group(1) if match else None
                                if card_number:
                                    data.append((filename, int(quantity), image_src, set_code, card_number))


    # Save the data to SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS key_cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        archetype TEXT,
        quantity INTEGER,
        image_src TEXT,
        set_code TEXT,
        card_number TEXT
    )
    """)

    # Insert data into the table
    cursor.executemany("""
    INSERT INTO key_cards (archetype, quantity, image_src, set_code, card_number) VALUES (?, ?, ?, ?, ?)
    """, data)

    cursor.execute("""update key_cards set card_number = '016' where set_code == 'ITI' and card_number == '223'""")
    cursor.execute("""update key_cards set card_number = '195' where set_code == 'ITI' and card_number == '222'""")
    cursor.execute("""update key_cards set card_number = '190' where set_code == 'ITI' and card_number == '221'""")
    cursor.execute("""update key_cards set card_number = '110' where set_code == 'ROTF' and card_number == '211'""")
    cursor.execute("""update key_cards set card_number = '114' where set_code == 'TFC' and card_number == '212'""")
    cursor.execute("""update key_cards set card_number = '142' where set_code == 'TFC' and card_number == '214'""")
    cursor.execute("""update key_cards set card_number = '193' where set_code == 'TFC' and card_number == '216'""")
    cursor.execute("""update key_cards set card_number = '125' where set_code == 'URSU' and card_number == '215'""")

    # Commit and close connection
    conn.commit()
    conn.close()

    print(f"Data successfully saved to {db_name}.")
