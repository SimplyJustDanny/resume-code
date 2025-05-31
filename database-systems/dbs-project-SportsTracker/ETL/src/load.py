# Creates and returns query string for columns in current table like "(col_1, col_2, ... col_n)"
def create_columns_query(table):
    columns_to_query = "("
    table_columns = table.columns
    for column in table_columns:
        columns_to_query += str(column) + ", "
    columns_to_query = columns_to_query[:len(columns_to_query) - 2] + ")"
    return columns_to_query

# Creates and returns query string for row to add given the current row like "(row_item_1, row_item_2 ... row_item_n)"
def create_values_query(row):
    values_to_query = "("
    row_values = list(row.values())
    for row_value in row_values:
        if isinstance(row_value, str):
            if "'" in str(row_value): # Replace single quotes with double quotes.                            
                row_value = row_value.replace("'", "''")                    
            values_to_query += "'" + str(row_value) + "', "
        else:
            values_to_query += str(row_value) + ", "
    values_to_query = values_to_query[:len(values_to_query) - 2] + ")"
    return values_to_query

# Loads a table to the db. The type of table must be DataFrame. table is the DataFrame object to work with in current loop. 
def load_table(db, tablename, table):
    columns_to_query = create_columns_query(table)  # Prepare columns to map query. 
    # Query_string structure to query the table later.
    query_string = f""" 
    INSERT INTO {tablename}
    {columns_to_query}
    VALUES
    """
    # Add values to fill out the table with into the query string. 
    for row in table.to_dicts(): 
        values_to_query = create_values_query(row)
        query_string += values_to_query + ",\n"
    query_string = query_string[:len(query_string)-2] + ";" # Remove the final comma and replace it with semicolon. 
    return query_string # Return query string. 

def load(db, tables):
    # Tables must be added in a specific order for the FKs, hence the list. 
    table_order_list = ['athletes', 'exercises', 'sports', 'teams', 'championships', 'practices', 'exercise_instructions', 'exercise_primary_muscles', 'exercise_secondary_muscles', 'exercise_images', 'sport_exercises']
    print("Loading into table...")
    master_query = "" # This will contain all the instructions to load the data in one query. 
    for name in table_order_list:
        table = dict(tables.items())[name]
        master_query += load_table(db, name, table) # Append the queries to the string. 
    db.query(master_query) # Execute the query with the master_query string. 
    print("Done!")
    db.close_cursors()
