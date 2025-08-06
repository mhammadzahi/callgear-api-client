import psycopg2
from psycopg2 import sql

class Database:

    def __init__(self, db_url):
        self.db_url = db_url

    def connect(self):
        return psycopg2.connect(self.db_url)

    def insert_call_report(self, report_data):
        # A list of all column names in the correct order for insertion.
        columns = [
            'id', 'source', 'is_lost', 'direction', 'start_time', 'finish_time',
            'call_records', 'cpn_region_id', 'finish_reason', 'hold_duration',
            'talk_duration', 'wait_duration', 'total_duration', 'cpn_region_name',
            'communication_id', 'wav_call_records', 'communication_type',
            'clean_talk_duration', 'total_wait_duration', 'contact_phone_number',
            'virtual_phone_number', 'call_records_url'
        ]

        # Dynamically and safely build the SQL INSERT statement.
        insert_statement = sql.SQL("INSERT INTO call_reports ({}) VALUES ({})").format(
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(columns))
        )

        # Create a tuple of values from the report_data dictionary.
        # Using .get(col) ensures that if a key is missing, it defaults to None (which becomes NULL in SQL).
        values = tuple(report_data.get(col) for col in columns)

        try:
            # The 'with' statement ensures the connection and cursor are automatically closed.
            with self.connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(insert_statement, values)
                conn.commit()
            print(f"Successfully inserted report with id: {report_data.get('id')}")
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error while inserting data: {error}")
            # The 'with' block will handle connection closing, but a rollback is good practice.
            if 'conn' in locals() and conn:
                conn.rollback()

# ### Key Changes and Improvements:

# 1.  **Correct Table and Column Names**: The `INSERT` statement now targets the `call_reports` table and includes all 22 columns defined in your table schema.
# 2.  **Dynamic and Safe SQL**: It uses the `psycopg2.sql` module to build the query. This is the standard, recommended way to construct queries with dynamic table or column names, as it properly quotes identifiers and protects against SQL injection.
# 3.  **Complete Record Insertion**: The method is designed to insert a full row. It takes a dictionary, `report_data`, where keys correspond to the column names.
# 4.  **Robust Connection Handling**: The use of `with` statements for the connection and cursor is a best practice. It guarantees that these resources are closed automatically, even if errors occur during the process.
# 5.  **Error Handling**: A `try...except` block has been added to catch and report any database errors that might occur during the insertion process.

# ### How to Use the Class:

# To use this class, you would first create an instance of it with your database URL. Then, for each row of data you want to insert, you would create a dictionary and pass it to the `insert_call_report` method.

# ```python
# # Example Usage:

# # 1. IMPORTANT: Replace with your actual database connection URL
# db_connection_url = "postgresql://your_user:your_password@your_host:5432/your_database"

# # 2. Create an instance of the Database class
# db = Database(db_connection_url)

# # 3. Prepare your data as a dictionary. Keys MUST match table columns.
# #    Use None for fields that should be NULL in the database.
# report_to_insert = {
#     'id': 147146139,
#     'source': 'va',
#     'is_lost': False,
#     'direction': 'in',
#     'start_time': '2025-06-15 14:59:50',
#     'finish_time': '2025-06-15 15:01:40',
#     'call_records': ['ed75814d4d0433f40fe39b895552efb1'],
#     'cpn_region_id': 5587,
#     'finish_reason': 'operator_disconnects',
#     'hold_duration': 0,
#     'talk_duration': 105,
#     'wait_duration': 4,
#     'total_duration': 109,
#     'cpn_region_name': 'UAE / unknown',
#     'communication_id': 147146139,
#     'wav_call_records': [],
#     'communication_type': 'call',
#     'clean_talk_duration': 105,
#     'total_wait_duration': 4,
#     'contact_phone_number': '971509071556',
#     'virtual_phone_number': '97128160525',
#     'call_records_url': 'https://app.callgear.ae/system/media/talk/147146139/ed75814d4d0433f40fe39b895552efb1/'
# }

# # 4. Call the insert method
# # Make sure you have created the table in your database first.
# # db.insert_call_report(report_to_insert)
