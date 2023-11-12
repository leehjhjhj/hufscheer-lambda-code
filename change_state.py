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
            port=os.environ.get('DB_PORT'),
            db=3306,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
        )
    target = event['target']
    comment_id = event['commentId']
    report_id = event['reportId']
    try:
        with conn.cursor() as cursor:
            if check_badword(target):
                cursor.execute(f"UPDATE sports_live.comments SET is_blocked = 1 WHERE id = {comment_id};")
                report_state = 'VALID'
                response = '검거? 완료.'
            else: 
                report_state = 'PENDING'
                response = '보류'

            cursor.execute(f"UPDATE sports_live.reports SET state = '{report_state}' WHERE id = {report_id};")
            result = cursor.fetchall()
            if result:
                for row in result:
                    logging.info(row)
            conn.commit() 
            return response
        
    except Exception as e:
        logging.error(f'DB 에러 발생: {e}')
    finally:
        conn.close()