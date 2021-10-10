# Level 2
## Solution
To create web server I used flask library, using templates and css I made user interface.
I was planning to create my_module with `query_select` and `data_processing` functions, unfortunatly I have not successed. Therefore I implemented them directly in `main.py`. Afterwards, I was setting all variables to make web servise work. I do not know how to read values from form trough method 'get', therefore in function `create_query` I set results to default variables, I mean client inputs are not concerned:
```
@app.route('/output', methods=['GET', 'POST'])
def create_query() -> 'html':
    # img_status = requests.GET['is_image_exists']
    # min_age = requests.GET['min_age']
    # max_age = requests.GET['max_age']
    title = 'Here should be the results:'
    # results = str(query_select(img_status, min_age, max_age))
    results = str(query_select(True, 0, 60))
```
Anyway, data processing works fine, partially. It applies changes to DB only.
