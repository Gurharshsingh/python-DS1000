from fastapi import APIRouter,HTTPException,status
from schemas.models import Item


data=[{"id":1, "Name":"pen", "Price":10, "Tax":1},
    {"id":2,"Name":"pencil","Price":20,"Tax":2},
    {"id":3,"Name":"eraser","Price":30,"Tax":3},
    {"id":4,"Name":"notebook","Price":40,"Tax":4},
    {"id":5,"Name":"book","Price":50,"Tax":5},
    ]
#Create a router for the application
router = APIRouter(prefix="/users",tags=["UserData"])




@router.get("/getitems")
async def getitems():
    try:
        if data==[]:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="No items found")
        return data
    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))


#Fetching the item with the help of the id
@router.get("/item/{id}")
def get_item(id:int):
    for item in data:
        if item["id"]==id:
            return item
    return {"message":"Item not found"}

@router.get("/getitems")
def all_items():
    return data

@router.post("/postitem")
def postitem(item:Item):
    for i in data:
        if(item.id==i["id"]):
            return {"message":"Item already exists"}
    data.append(item)
    return {"message":"Item added successfully"}

@router.put("/updateitem")
def update_item(id:int,item:Item):
    for i in data:
        if(i["id"]==id):
            i["name"]=item.name
            i["price"]=item.price
            i["tax"]=item.tax
            return {"message":"Item updated successfully"}
    return {"message":"Item not found"}


@router.delete("/deletion{id}")
def delete_item(id:int):
    for i in data:
        if(i["id"]==id):
            data.remove(i)
            return {"message":"Item deleted successfully"}
    return {"message":"Item not found"}



