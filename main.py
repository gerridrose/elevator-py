from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ElevatorState(BaseModel):
    current_floor: int
    total_floors: int
    door_open: bool

elevator = ElevatorState(current_floor=1, total_floors=10, door_open=False)

@app.get("/status", response_model=ElevatorState)
def get_status():
    return elevator

@app.post("/move_up")
def move_up():
    if elevator.current_floor >= elevator.total_floors:
        raise HTTPException(status_code=400, detail="Elevator is already at the top floor.")
    if elevator.door_open:
        raise HTTPException(status_code=400, detail="Close the door before moving.")
    elevator.current_floor += 1
    return {"message": "Elevator moved up.", "current_floor": elevator.current_floor}

@app.post("/move_down")
def move_down():
    if elevator.current_floor <= 1:
        raise HTTPException(status_code=400, detail="Elevator is already at the ground floor.")
    if elevator.door_open:
        raise HTTPException(status_code=400, detail="Close the door before moving.")
    elevator.current_floor -= 1
    return {"message": "Elevator moved down.", "current_floor": elevator.current_floor}

@app.post("/open_door")
def open_door():
    if elevator.door_open:
        raise HTTPException(status_code=400, detail="Door is already open.")
    elevator.door_open = True
    return {"message": "Elevator door opened."}

@app.post("/close_door")
def close_door():
    if not elevator.door_open:
        raise HTTPException(status_code=400, detail="Door is already closed.")
    elevator.door_open = False
    return {"message": "Elevator door closed."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)