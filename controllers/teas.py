from fastapi import APIRouter, HTTPException
from models.tea_data import teas_db

router = APIRouter()

@router.get('/teas')
def get_teas():
  return teas_db

@router.get("/teas/{tea_id}")
def get_single_tea(tea_id: int):
  for tea in teas_db['teas']:
        if tea['id'] == tea_id:
            return tea
  raise HTTPException(status_code=404, detail="Cannot find Tea")


@router.post("/teas")
def create_tea(tea: dict):
    # Create a new tea
    teas_db["teas"].append(tea)
    return tea

# teas.py

@router.put("/teas/{tea_id}")
def update_tea(tea_id: int, tea: dict):

    # Find the tea to update
    for existing_tea in teas_db['teas']:
        if existing_tea['id'] == tea_id:
            existing_tea.update(tea)  # Update the existing tea's data
            return existing_tea

    # If tea was not found, raise an error
    raise HTTPException(status_code=404, detail="Tea not found")

# teas.py

@router.delete("/teas/{tea_id}")
def delete_tea(tea_id: int):
    # Delete a tea by ID
    for tea in teas_db['teas']:
        if tea['id'] == tea_id:
            teas_db['teas'].remove(tea)  # Remove the tea from the database
            return {"message": f"Tea with ID {tea_id} has been deleted."}

    # If tea was not found, raise an error
    raise HTTPException(status_code=404, detail="Tea not found")