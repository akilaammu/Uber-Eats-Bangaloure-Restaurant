import streamlit as st
import pandas as pd
import mysql.connector as ms

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Dashboard", "📊 Business Q&A"]
)

if page == "🏠 Dashboard":
    conn = ms.connect(
        host='localhost', 
        user='root', 
        password='Ayyappa@310525', 
        database='MiniProject1'
        )

    cursor = conn.cursor()

    query = """ 
        select * from uber_eats
    """

    #df_results = pd.read_sql(query,conn)


    cursor.execute(query)

    results = cursor.fetchall()

    df_results = pd.DataFrame(results,columns=['Restaurant Name','Online Order','Book Table','Rate','Vote','Phone','Location','Restaurant Type','Dishes Liked','Cuisines','Approximate Cost For Two People','Type','City'])

    # Sidebar CSS


    st.sidebar.markdown("""
    <h2 style="
    background:#009688;
    color:white;
    padding:10px;
    border-radius:10px;
    text-align:center;">
    🔍 Filters
    </h2>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("""
    <h3 style='
    color:#009688;
    '> Select Restaurant
    </h3>
    """, unsafe_allow_html=True)

    restaurant = st.sidebar.selectbox(
        "",
        ["All"] + sorted(df_results["Restaurant Name"].dropna().unique().tolist())
    )

    st.sidebar.markdown("""
    <h3 style='
    color:#009688;
    '> Online Order
    </h3>
    """, unsafe_allow_html=True)

    onlineorder = st.sidebar.selectbox(
        "",
        ["All"] + sorted(df_results["Online Order"].dropna().unique().tolist())
    )

    st.sidebar.markdown("""
    <h3 style='
    color:#009688;
    '> Location
    </h3>
    """, unsafe_allow_html=True)

    location = st.sidebar.selectbox(
        "",
        ["All"] + sorted(df_results["Location"].dropna().unique().tolist())
    )

    st.sidebar.markdown("""
    <h3 style='
    color:#009688;
    '> Cuisines
    </h3>
    """,unsafe_allow_html=True)
    
    cuisines = st.sidebar.selectbox(
        "",
        ["All"] + sorted(df_results["Cuisines"].dropna().unique().tolist())
    )
    
    st.sidebar.markdown("""
    <h3 style = '
    colour:#009688;
    '> City
    </h3>                    
    """, unsafe_allow_html=True)
    
    city = st.sidebar.selectbox(
        "",
        ["All"] + sorted(df_results["City"].dropna().unique().tolist())
    )
    
    filtered_df = df_results.copy()

    if restaurant != "All":
        filtered_df = filtered_df[filtered_df["Restaurant Name"] == restaurant
        ]
    if onlineorder != "All":
        filtered_df = filtered_df[filtered_df["Online Order"] == onlineorder
        ]    
    if location != "All":
        filtered_df = filtered_df[filtered_df["Location"] == location
        ]    
    if cuisines != "All":
        filtered_df = filtered_df[filtered_df["Cuisines"] == cuisines
        ]
    if city != "All":
        filtered_df = filtered_df[filtered_df["City"] == city
        ]
              
    #st.title("Uber Eats Restaurant Dashboard")
    st.markdown("""
    <h1 style="
        text-align:center;
        color:white;
        background:#009688;
        padding:15px;
        border-radius:12px;
        font-family:Arial;
        margin: 11px;
        box-shadow:2px 2px 10px rgba(0,0,0,0.3);">
        🍽️ Uber Eats Restaurant Analytics Dashboard
    </h1>
    """, unsafe_allow_html=True)
    st.dataframe(filtered_df,use_container_width=True)

    #st.dataframe(df_results)

elif page == "📊 Business Q&A":
    st.markdown(
    "<h1 style='color:#009688;text-align:center;'>Answers</h1>",
    unsafe_allow_html=True)

    st.title("")
    business_queries = {"Which Bangalore locations have the highest average restaurant ratings?":
        """ 
            select location, round(avg(rate),2) as avg_rating,count(*) from uber_eats
            where rate is not null group by location having count(*) > 5 
            order by avg_rating desc limit 10;
            """,
            "Which locations are over-saturated with restaurants?":
            """ 
            SELECT location,COUNT(*) AS restaurant_count,round(avg(rate),2) as avg_rating
            FROM uber_eats
            where rate is not null
            GROUP BY location
            ORDER BY restaurant_count DESC
            LIMIT 10
            """,
            "Does online ordering improve restaurant ratings?":
            """
            SELECT
            online_order, ROUND(AVG(rate), 2) AS average_rating,COUNT(*) AS total_restaurants
            FROM uber_eats
            WHERE rate IS NOT NULL
            GROUP BY online_order;
            """,
            "Does table booking correlate with higher customer ratings?":
            """
            SELECT book_table,ROUND(AVG(rate), 2) AS average_rating,COUNT(*) AS total_restaurants
            FROM uber_eats
            WHERE rate IS NOT NULL
            GROUP BY book_table
            """,
            "How do low, mid, and premium-priced restaurants perform in terms of ratings?":
            """
            SELECT
            CASE
                WHEN approx_cost_for_two_people < 500 THEN 'Low'
                WHEN approx_cost_for_two_people BETWEEN 500 AND 1000 THEN 'Mid'
                ELSE 'Premium'
            END AS price_category,
            ROUND(AVG(rate), 2) AS average_rating,
            COUNT(*) AS total_restaurants
            FROM uber_eats
            WHERE rate IS NOT NULL
            GROUP BY price_category
            ORDER BY
            CASE
                WHEN price_category = 'Low' THEN 1
                WHEN price_category = 'Mid' THEN 2
                WHEN price_category = 'Premium' THEN 3
            END
            """,
            "Which cuisines are most common in Bangalore?":
            """ 
            SELECT cuisines,COUNT(*) AS restaurant_count
            FROM uber_eats
            WHERE cuisines IS NOT NULL
            GROUP BY cuisines
            ORDER BY restaurant_count DESC
            LIMIT 10;
            """,
            "Which cuisines receive the highest average ratings?":
            """ 
            SELECT cuisines,ROUND(AVG(rate), 2) AS average_rating,COUNT(*) AS total_restaurants
            FROM uber_eats
            WHERE rate IS NOT NULL
            AND cuisines IS NOT NULL
            GROUP BY cuisines
            HAVING COUNT(*) >= 10
            ORDER BY average_rating DESC
            LIMIT 10;
            """,
            "Which locations show high demand but lower average ratings?":
            """ 
            SELECT location,COUNT(*) AS total_restaurants,ROUND(AVG(rate), 2) AS average_rating
            FROM uber_eats
            WHERE rate IS NOT NULL
            GROUP BY location
            HAVING COUNT(*) >= 20
            ORDER BY total_restaurants DESC, average_rating ASC
            LIMIT 10;
            """,
            "Do restaurants offering both online ordering and table booking perform better?":
            """ 
            SELECT online_order,book_table,ROUND(AVG(rate), 2) AS average_rating,COUNT(*) AS total_restaurants
            FROM uber_eats
            WHERE rate IS NOT NULL
            GROUP BY online_order, book_table
            ORDER BY average_rating DESC;
            """,
            "What combination of factors maximizes restaurant success on Uber Eats?(Pricing + Location + Cuisine + Platform Features)":
            """ 
            SELECT location,cuisines,
            CASE
                WHEN approx_cost_for_two_people < 500 THEN 'Low Cost'
                WHEN approx_cost_for_two_people BETWEEN 500 AND 1000 THEN 'Medium Cost'
                ELSE 'Premium Cost'
            END AS price_category,online_order,book_table,ROUND(AVG(rate), 2) AS average_rating,
            ROUND(AVG(votes), 0) AS average_votes,COUNT(*) AS total_restaurants
            FROM uber_eats
            WHERE rate IS NOT NULL AND cuisines IS NOT NULL
            GROUP BY location,cuisines,price_category,online_order,book_table
            HAVING COUNT(*) >= 5
            ORDER BY average_rating DESC,average_votes DESC
            LIMIT 20;
            """,
            "Which restaurants have high average order value?":
            """ 
            select restaurant_name,round(avg(order_value),2)avg_value,count(*) restaurant from orders 
            group by restaurant_name having count(*) > 5 order by avg_value desc
            """,
            "Which Restaurants have high UPI transactions? ":
            """ 
            select count(*)count,restaurant_name,round(avg(order_value),2)avg_value from orders where payment_method= 'UPI'
            group by restaurant_name having count(*) > 5
            order by avg_value desc
            """ ,         
            "What are payment method orders we have, and their average order value is?":
            """ 
            select count(*)count,payment_method,round(avg(order_value),2) avg_value from orders group by payment_method
            order by avg_value desc
            """,
            "Does discount order has high order value?" :
            """ 
            select count(*)count,discount_used,round(avg(order_value),2) avg_value from orders group by discount_used 
            order by avg_value desc;
            """,
            "List the orders of December Month 2025?" :
            """ 
            select count(*) restaurant_count,restaurant_name, round(avg(order_value) ,2) avg_value,order_date 
            from orders where order_date between '2025-12-01' and '2025-12-31' group by restaurant_name,order_date
            order by avg_value desc
            """
        }
    
    st.sidebar.markdown("""<h3 
                    style="color:#009688;">
                    Choose Restaurant & Order Questions
                    </h2>""",unsafe_allow_html=True)
    selected = st.sidebar.selectbox(
        "",
        list(business_queries.keys())
    )
    
    if selected:
        
        # Your SQL question code     
        conn = ms.connect(
            host = 'localhost',
            user = 'root',
            password = 'Ayyappa@310525',
            database = 'MiniProject1'
        )

        #create cursor
        cursor = conn.cursor()
        cursor.execute(business_queries[selected])
        results = cursor.fetchall()
        
        columns = [i[0] for i in cursor.description]
        df = pd.DataFrame(results, columns=columns)
        st.dataframe(df, use_container_width=True)        
           
        cursor.close()
        conn.close()
    
