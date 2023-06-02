# IMPORTS ----
import sqlalchemy as sql
import pandas as pd
# COLLECT DATA ----
def collect_data(
    conn_string= "sqlite:///00_database/bike_orders_database.sqlite"
    ):
    """
    Collects and combines the bike orders data

    Args:
        conn_string (str, optional): A SQLAlchemy connection string. Defaults to "sqlite:///00_database/bike_orders_database.sqlite".

    Returns:
        DataFrame: Pandas dataframe that combines data from tables:
            - orderlines
            - bikes
            - bikeshops
    """
    engine = sql.create_engine(conn_string)
    conn = engine.connect()
    table_names = ['bikes', 'bikeshops', 'orderlines']
    data_dict = {}
    for table in table_names:
        data_dict[table] = pd.read_sql(f"SELECT * FROM {table}", con=conn)
    conn.close()
    
    joined_df = pd.DataFrame(data_dict["orderlines"]) \
        .merge(right=data_dict['bikes'],
                how='left',
                left_on='product.id',
                right_on='bike.id') \
        .merge(right=data_dict['bikeshops'],
        how='left',
        left_on='customer.id',
        right_on='bikeshop.id')
    joined_df['order.date'] = pd.to_datetime(joined_df['order.date'])
    
    temp_df = joined_df['description'].str.split(" - ", expand=True)
    joined_df['category.1'] = temp_df[0]
    joined_df['category.2'] = temp_df[1]
    joined_df['frame.material'] = temp_df[2]
    
    temp_df = joined_df['location'].str.split(", ", expand=True)
    joined_df['city'] = temp_df[0]
    joined_df['state'] = temp_df[1]
    
    joined_df['total.price'] = joined_df['quantity'] * joined_df['price']
    
    cols_to_keep_list = ['order.id', 'order.line', 'order.date', 'model', 'quantity',  
        'price', 'total.price', 'bikeshop.name', 'category.1', 'category.2','frame.material', 
        'city', 'state']

    joined_df = joined_df[cols_to_keep_list]
    joined_df.columns = joined_df.columns.str.replace(".", "_")
    
    return joined_df
