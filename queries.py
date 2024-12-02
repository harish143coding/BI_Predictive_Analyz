import sqlparse as sp

# query for ranking the employees

ranking_query = ("SELecT employee_id, department, RANK() OVER (PARTITION BY department ORder BY salary DESC) AS RANK"
                 " FROM Employees")

parsed_query_1 = sp.format(ranking_query,
                         keyword_case='upper',
                         reindent=True,
                         output_format='sql')

print(parsed_query_1)

# sample form of sub_query to find all the employees with above average salaries

salary_sub_query = "select employee_id, name FROM employees WHERE salary > SELECT AVG(salary) FROM employees"
parsed_query_2 = sp.format(salary_sub_query,
                           keyword_case='upper',
                           reindent=True,
                           output_format='sql')
print(parsed_query_2)

# sample SQL for PIVOTING the product categories

product_pivoting = ("SELect product_name, CASE WHEN product_type = 'powder' then category_1 END AS category_1,"
                    "CASE WHEN product_type = 'millets' then category_2 END AS category_2   FROM products")
formated_pivot = sp.format(product_pivoting,
                           keyword_case='upper',
                           reindent=True,
                           output_format='sql')
#print(formated_pivot.tokens)