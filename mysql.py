import pymysql

def set_mysql(item_info, count):

    db = pymysql.connect(host='127.0.0.1', port=3306, user='root',
                         passwd='gkaquf1@', db='bsetproducts', charset='utf8')
    cursor = db.cursor()

    jungbog_check = f"""select count(*) from items where item_code ='{item_info['item_code']}'"""

    cursor.execute(jungbog_check)
    result = cursor.fetchone()

    if result[0] == 0:  # include with count in one column
        sql_item = f"""insert into items values(\
        '{item_info['item_code']}',\
        '{item_info['title']}',\
        {item_info['ori_price']},\
        {item_info['dis_price']},\
        {item_info['discount_percent']},\
        '{item_info['provider']}')\
        """
        # print(sql_item)
        cursor.execute(sql_item)

    sql_ranking = f"""insert into ranking (main_category, sub_category, item_ranking, item_code)values(
        '{item_info['category_name']}',\
        '{item_info['sub_category_name']}',\
         {item_info['ranking']},\
        '{item_info['item_code']}')\
    """

    print(f"total_count : {count}")

    # print(sql_ranking)
    cursor.execute(sql_ranking)

    db.commit()
    db.close()
