import pymysql
import logging
import os
from check_badword import check_badword

pymysql.install_as_MySQLdb()

def change_state(event):
    conn = pymysql.connect(
            host=os.environ.get('DB_HOST'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            port=3306,
            db=os.environ.get('DB_NAME'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
        )
    target = event['target']
    comment_id = event['commentId']
    report_id = event['reportId']
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM sports_live.comments WHERE id = {comment_id};")
            if cursor.rowcount == 0:
                status_code = '404'
                return status_code
            cursor.execute(f"SELECT * FROM sports_live.reports WHERE id = {report_id};")
            if cursor.rowcount == 0:
                status_code = '404'
                return status_code

            if check_badword(target):
                cursor.execute(f"UPDATE sports_live.comments SET is_blocked = 1 WHERE id = {comment_id};")
                if cursor.rowcount == 0:
                    status_code = '400'
                    return status_code
                report_state = 'VALID'
            else: 
                report_state = 'PENDING'

            cursor.execute(f"UPDATE sports_live.reports SET state = '{report_state}' WHERE id = {report_id};")
            if cursor.rowcount == 0:
                status_code = '400'
                return status_code
            conn.commit()
            status_code = '200'
            return status_code
        
    except Exception as e:
        logging.error(f'DB 에러 발생: {e}')
    finally:
        conn.close()