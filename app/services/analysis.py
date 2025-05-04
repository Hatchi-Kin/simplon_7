from datetime import datetime

from core.database import get_connection, execute_query
from models.tables import (
    TOTAL_REVENUE_QUERY,
    SALES_BY_PRODUCT_QUERY,
    SALES_BY_REGION_QUERY,
    INSERT_TOTAL_REVENUE,
    INSERT_PRODUCT_SALES,
    INSERT_REGION_SALES,
    LATEST_ANALYSIS_DATE_QUERY,
    TOTAL_REVENUE_BY_DATE_QUERY,
    PRODUCT_SALES_BY_DATE_QUERY,
    REGION_SALES_BY_DATE_QUERY,
)


def run_analysis():
    """Run sales analysis and store results in the database"""
    analysis_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            # Total revenue analysis
            cursor.execute(TOTAL_REVENUE_QUERY)
            total_revenue = cursor.fetchone()[0] or 0

            # Store total revenue
            cursor.execute(INSERT_TOTAL_REVENUE, (analysis_date, total_revenue))

            # Sales by product analysis
            cursor.execute(SALES_BY_PRODUCT_QUERY)
            product_sales = cursor.fetchall()

            # Store product sales
            for product in product_sales:
                cursor.execute(
                    INSERT_PRODUCT_SALES,
                    (analysis_date, product[0], product[1], product[2]),
                )

            # Sales by region analysis
            cursor.execute(SALES_BY_REGION_QUERY)
            region_sales = cursor.fetchall()

            # Store region sales
            for region in region_sales:
                cursor.execute(
                    INSERT_REGION_SALES,
                    (analysis_date, region[0], region[1], region[2]),
                )

            conn.commit()
        return True
    except Exception as e:
        print(f"Error during analysis: {e}")
        return False


def get_latest_analysis():
    """Get the latest analysis results from the database"""
    try:
        # Get latest analysis date
        latest_date_result = execute_query(LATEST_ANALYSIS_DATE_QUERY)
        latest_date = latest_date_result[0][0] if latest_date_result else None

        if not latest_date:
            return None, None, None

        # Get total revenue
        total_revenue_result = execute_query(
            TOTAL_REVENUE_BY_DATE_QUERY, (latest_date,)
        )
        total_revenue = total_revenue_result[0][0] if total_revenue_result else 0

        # Get product sales
        product_sales = execute_query(PRODUCT_SALES_BY_DATE_QUERY, (latest_date,))

        # Get region sales
        region_sales = execute_query(REGION_SALES_BY_DATE_QUERY, (latest_date,))

        return total_revenue, product_sales, region_sales
    except Exception as e:
        print(f"Error fetching latest analysis: {e}")
        return None, None, None
