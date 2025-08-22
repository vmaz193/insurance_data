-- This model creates a comprehensive and dynamic date dimension table.
-- It includes a wide range of pre-calculated attributes to support
-- advanced time-based analysis and reporting.

with spined_dates as (
    {{ dbt_utils.date_spine(
        datepart="day",
        start_date="DATE '2024-01-01'",
        end_date="DATE '2025-12-31'"
       )
    }}
)

select
    -- Primary Key (formatted as YYYYMMDD for easy joining and sorting)
    to_char(date_day, 'YYYYMMDD')::int as date_id,

    -- Full Date Attributes
    cast(date_day as date) as full_date,
    to_char(date_day, 'Day, Month DD, YYYY') as full_date_description,

    -- Calendar Components
    extract(year from date_day) as calendar_year,
    extract(quarter from date_day) as calendar_quarter,
    extract(month from date_day) as calendar_month,
    extract(day from date_day) as calendar_day,
    extract(week from date_day) as calendar_week_of_year,
    
    -- Day Information
    extract(isodow from date_day) as day_of_week,
    to_char(date_day, 'Day') as day_name,
    to_char(date_day, 'Dy') as day_name_short,
    extract(doy from date_day) as day_of_year,

    -- Month Information
    to_char(date_day, 'Month') as month_name,
    to_char(date_day, 'Mon') as month_name_short,

    -- Quarter Information
    'Q' || extract(quarter from date_day) as quarter_name,

    -- Year Information
    to_char(date_day, 'YYYY-MM') as year_month,
    to_char(date_day, 'YYYY-"Q"Q') as year_quarter,

    -- Flags
    case 
        when extract(isodow from date_day) in (6, 7) then true 
        else false 
    end as is_weekend_flag,
    
    case
        when extract(day from date_day) = 1 then true
        else false
    end as is_start_of_month_flag,

    -- *** THIS IS THE CORRECTED LOGIC FOR POSTGRESQL ***
    case
        when date_day = (date_trunc('month', date_day) + interval '1 month' - interval '1 day')::date then true
        else false
    end as is_end_of_month_flag

from spined_dates