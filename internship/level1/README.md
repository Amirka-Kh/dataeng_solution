# Level 1
## Content
1.[Task description](#task-description)
2.[Solution](#solution)
3.[Faced problems](#faced-problems)

## Task description
### Data processing description
1. Read csv file
2. Match images for each user
3. Combine data from CSV and image path
4. Update processed_data/output.csv CSV file and add new data. Important we can update data for previously processed
   user. In output CSV and DB we should not duplicate records. Output CSV file format: user_id, first_name,
   last_name, birthts, img_path
### Task
Implement a script to process files from the `src_data` folder.

## Solution
First, I found a way how to get a data from dataeng repository, for that I used `request` library. Then 
since user's information where in csv format I used `pandas` to process it. 
```
read_data = requests.get(temp_url).content
file = pd.read_csv(io.StringIO(read_data.decode('utf-8')))
```
After I added to file `user_id` and `img_path`.
```
file['img_path'] = img_path
file.insert(0, "user_id", index, True)
```
Amazing. After that I had to think about changes, if in origin file a new data will appear or an old data will
be changed, what should I do? Of course, apply this changes to my `processed_file`. 
The easiest way was delete `processed_file` and create new one. I did it in another way.

Firstly, I created 2 dictionaries `hash_id` and `img_paths`. I used them for checking records in `processed_file`.

For example, I get a record from origin, I check if its `id` in `hash_id`, if it so (which means we already have 
this data in `processed_file`), I chechk if `img_path` has changed (this is the only thing which can change, okey 
other items also can change, I didn't thought about it), if so it applies changes to `processed_data`.
```
if str(index) in hash_id.keys():
    if img_path in img_urls.keys():
        index += 1
        continue
```
Then I save changes.

DB cho tam? do pishi

## Faced problems
hash id, request, path, db(vashe ujaas)
