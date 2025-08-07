import psycopg2
import psycopg2.extras
from psycopg2 import sql

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
