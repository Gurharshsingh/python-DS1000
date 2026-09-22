#pip install fastapi
# pip install uvicorn
# uvicorn main:app --reload


from fastapi import FastAPI

app = FastAPI(title="Fast API Class")


# GET
# POST
# PUT
# DELETE


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI"}


@app.get("/about")
def about():
    return {"class": "First class" }


@app.get("/greet")
def greet():
    return {"message":"Hello how are you?"}


#PATH PARAMETERS

@app.get("/greet/{name}")
def greeting(name:str):
    return {"message":f"Hello {name}"}


@app.get('/square/{num}')
def square(num:int):
    return {"message":f"The square of {num} is {num*num}"}

@app.get('/item/{itemid}')
def getitem(itemid:int):

    db = {
        1:"laptop",
        2:"mouse",
        3:'keyboard',
        4:'monitor',
        5:'headphone',
    }

    item = db.get(itemid, "Item not found")

    return {"Item id:": itemid ,
            "item:" : item}

#QUERY PARAMETERS

@app.get("/search")
def search_items(keyword:str, limit:int=10, skip: int = 0):

    results = []

    startnumber = skip+1

    endnumber = skip + limit +1
    for i in range(startnumber,endnumber):
        item_name = f"{keyword} result {i}"
        results.append(item_name)

    return{"keyword":keyword,
    "results":results
    }

@app.get('/users')
def get_user(active:bool=True,role:str="student"):
    all_users = [
        {"id":1, "name":"Alice", "role":"student", "active":True},
        {"id":2, "name":"Bob", "role":"student", "active":True},
        {"id":3, "name":"Charlie", "role":"student", "active":False},
        {"id":4, "name":"David", "role":"teacher", "active":True}
    ]
    
    filtered = [u for u in all_users if u.get("active")==active and u.get("role")==role]

    return {"users" : filtered
    , 'count' : len(filtered)}

@app.get("/users/{user_id}/orders")
def get_user_orders(user_id:int,status:str='all',limit:int=5):
    orders = [
        {"order_id": 101, "items":"mobile", "status":"delivered"},
        {"order_id": 102, "items":"laptop", "status":"shipped"},
        {"order_id": 103, "items":"mouse", "status":"pending"},
        {"order_id": 104, "items":"keyboard", "status":"delivered"},
        {"order_id": 105, "items":"monitor", "status":"shipped"},
        {"order_id": 106, "items":"headphone", "status":"pending"}
    ]
    

    if status != "all":
        orders = [o for o in orders if o["status"] == status]

    return{ "user_id": user_id,
            "status":status,
            "orders": orders[:limit]}


