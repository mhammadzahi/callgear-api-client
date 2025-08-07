import psycopg2
import psycopg2.extras
from psycopg2 import sql
import json


class Database:
    def __init__(self, db_url):
        self.db_url = db_url

    def connect(self):
        return psycopg2.connect(self.db_url)

    def insert_call_reports(self, reports_list):
        """
        Inserts multiple call reports efficiently from a list of dictionaries.
        This is the primary method you should use.

        :param reports_list: A list of dictionaries, where each dict is a report.
        """
        # Do nothing if the list is empty
        if not reports_list:
            print("Received an empty list of reports. Nothing to insert.")
            return []

        # --- FIX 1: The 'id' column is REMOVED from the list ---
        # The database will auto-generate the ID for each new row.
        columns = [
            'source', 'is_lost', 'direction', 'start_time', 'finish_time',
            'call_records', 'cpn_region_id', 'finish_reason', 'hold_duration',
            'talk_duration', 'wait_duration', 'total_duration', 'cpn_region_name',
            'communication_id', 'wav_call_records', 'communication_type',
            'clean_talk_duration', 'total_wait_duration', 'contact_phone_number',
            'virtual_phone_number', 'call_records_url'
        ]

        # --- FIX 2: Prepare a list of tuples from your list of dictionaries ---
        # We use .get(col) on each dictionary to safely get the value.
        values_list = [
            tuple(report.get(col) for col in columns) for report in reports_list
        ]

        # Create the efficient bulk INSERT statement
        insert_query = sql.SQL(
            "INSERT INTO call_reports ({fields}) VALUES %s RETURNING id"
        ).format(
            fields=sql.SQL(', ').join(map(sql.Identifier, columns))
        )

        try:
            with self.connect() as conn:
                with conn.cursor() as cur:
                    # psycopg2.extras.execute_values is the best tool for bulk inserts
                    inserted_ids = psycopg2.extras.execute_values(
                        cur, insert_query, values_list, fetch=True
                    )
                conn.commit()
            
            # Flatten the list of tuples returned by the query
            flat_ids = [item[0] for item in inserted_ids]
            print(f"Successfully inserted {len(flat_ids)} reports.")
            return flat_ids
            
        except (Exception, psycopg2.DatabaseError) as err:
            print(f"Error during bulk insert: {err}")
            if 'conn' in locals() and conn:
                conn.rollback()
            return []


    # def insert_call_report(self, report_dict):
    #     if not isinstance(report_dict, dict):
    #         print("Error: A dictionary is required for insert_call_report.")
    #         return None
            
    #     # Call the main batch function with a list containing just one item
    #     inserted_ids = self.insert_call_reports([report_dict])
    #     return inserted_ids[0] if inserted_ids else None



    def insert_chat_messages_reports(self, chat_report):
        """
        Inserts or updates multiple chat messages from a report dictionary.

        This function parses the main report dictionary, extracts the list of messages,
        and uses a single bulk "upsert" command for high efficiency. If a message
        with the same 'id' already exists, it will be updated; otherwise, it will be inserted.

        :param chat_report: The raw dictionary containing the list of chat messages.
        :return: A list of the integer IDs for all successfully inserted/updated messages.
        """
        # 1. Extract the list of messages from the main dictionary
        try:
            messages_list = chat_report['result']['data']
        except (KeyError, TypeError):
            print("Error: 'chat_report' dictionary is malformed or missing data. Expected structure: {'result': {'data': [...]}}")
            return []

        if not messages_list:
            print("Received a report with no messages. Nothing to insert.")
            return []

        # 2. Define the columns that match your 'chat_logs' table
        # This ensures the data maps to the correct database fields.
        columns = [
            'id', 'text', 'source', 'chat_id', 'resource', 'date_time',
            'channel_id', 'visitor_id', 'employee_id', 'channel_type',
            'is_group_chat', 'employee_full_name'
        ]

        # 3. Prepare the list of values (as tuples) for insertion
        # This loop transforms the list of dictionaries into a list of tuples.
        values_list = []
        for msg in messages_list:
            # For the 'resource' column (which is JSONB), we serialize the dict to a JSON string.
            # psycopg2 will correctly handle the conversion to the JSONB type.
            resource_json = None
            if msg.get('resource') is not None:
                resource_json = json.dumps(msg.get('resource'))
            
            values_tuple = tuple(
                json.dumps(msg.get(col)) if col == 'resource' and msg.get(col) is not None else msg.get(col)
                for col in columns
            )
            values_list.append(values_tuple)


        # 4. Construct the bulk UPSERT query using ON CONFLICT
        # This powerful query inserts new rows. If a row with a conflicting 'id'
        # already exists, it updates that existing row instead of causing an error.
        update_clause = sql.SQL(', ').join(
            sql.SQL("{} = EXCLUDED.{}").format(sql.Identifier(col), sql.Identifier(col))
            for col in columns if col != 'id' # Exclude the ID from the update set
        )

        insert_query = sql.SQL(
            """
            INSERT INTO chat_reports ({fields}) VALUES %s
            ON CONFLICT (id) DO UPDATE SET {update_fields}
            RETURNING id
            """
        ).format(
            fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
            update_fields=update_clause
        )

        # 5. Execute the query and commit the transaction
        try:
            with self.connect() as conn:
                with conn.cursor() as cur:
                    # execute_values is the most efficient way to perform bulk operations in psycopg2
                    inserted_ids = psycopg2.extras.execute_values(
                        cur, insert_query, values_list, fetch=True
                    )
                conn.commit()

            # Flatten the list of tuples returned by the RETURNING clause
            flat_ids = [item[0] for item in inserted_ids]
            print(f"Successfully inserted or updated {len(flat_ids)} chat messages.")
            return flat_ids

        except (Exception, psycopg2.DatabaseError) as err:
            print(f"Error during bulk chat message insert: {err}")
            # Rollback the transaction on error
            if 'conn' in locals() and conn:
                conn.rollback()
            return []

   