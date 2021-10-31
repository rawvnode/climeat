from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session, query_expression
from sqlalchemy.sql.functions import count
from sqlalchemy import func, or_, and_, select, join

from app.schemas.meat_city import MeatPerCapita

def get_meat_cities(db: Session):
    result = db.execute("""
        select ct1.account, c.city, c.country, c.year_reported, cp2.population as population, ct1.meat as meat_per_capita
        from city_populations cp2 
        inner join
        (select account, meat
        from crosstab(
            $$
                select cr.account_number, cr."row_number", sum(cast(cr.response_answer as numeric)::numeric)
                from 
                    city_responses cr 
                where  
                    cr.question_name = 'What is the per capita meat and dairy consumption (kg/yr) in your city?'
                    and cr.row_name = 'Meat consumption per capita (kg/year)'
                    and cr.column_name  = 'Amount'
                    and cr.response_answer not in ('0', 'NA', 'Question not applicable')
                    and cast(cr.response_answer as numeric) < 1000
                    group by cr.account_number, cr."row_number" 
            $$
            ) as ct("account" int4, "meat" numeric)
        ) as ct1
        on 
            cp2.account_number = ct1.account
        inner join cities c 
        on
            c.account_number = ct1.account
            and c.year_reported = 2020
        order by ct1.meat desc
    """
    )

    rlist = result.fetchall()

    for row in rlist:
        print(row)
    
    return rlist

def get_meat_overconsumption(db: Session):
    result = db.execute("""
        select ct1.account, c.city, c.country, c.year_reported, cp2.population as population, ct1.meat as meat_per_capita, (ct1.meat - 52.56) as meat_overconsumption_kgs, ((ct1.meat - 52.56) * cp2.population) /1000 as meat_overconsumption_kpi
        from city_populations cp2 
        inner join
        (select account, meat
        from crosstab(
            $$
                select cr.account_number, cr."row_number", sum(cast(cr.response_answer as numeric)::numeric)
                from 
                    city_responses cr 
                where  
                    cr.question_name = 'What is the per capita meat and dairy consumption (kg/yr) in your city?'
                    and cr.row_name = 'Meat consumption per capita (kg/year)'
                    and cr.column_name  = 'Amount'
                    and cr.response_answer not in ('0', 'NA', 'Question not applicable')
                    and cast(cr.response_answer as numeric) < 1000
                    group by cr.account_number, cr."row_number" 
            $$
            ) as ct("account" int4, "meat" numeric)
        ) as ct1
        on 
            cp2.account_number = ct1.account
        inner join cities c 
        on
            c.account_number = ct1.account
            and c.year_reported = 2020
        order by meat_overconsumption_kpi desc
    """
    )

    rlist = result.fetchall()

    for row in rlist:
        print(row)
    
    return rlist



