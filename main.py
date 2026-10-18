from fastapi import FastAPI, Depends
from fastapi import HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import auth
import jwt
import models
from database import engine, get_db

# This line creates your 'app.db' file and tables if they don't exist yet!
models.Base.metadata.create_all(bind=engine)

# this initializes your web application interface instance
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Security Dependency Function
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate session credentials.",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        # Decode the signature using your secret key parameters
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception 

    user = db.query(models.DBUser).filter(models.DBUser.username == username).first()
    if user is None:
        raise credentials_exception
    
    return user


# Define what an Asset must look like
class Asset(BaseModel):
    name: str = Field(json_schema_extra={"example": "Kali-WSL-Workstation"})
    asset_type: str = Field(json_schema_extra={"example": "Server"})
    ip_address: str = Field(json_schema_extra={"example": "192.168.1.50"})
    port: int = Field(json_schema_extra={"example": 80})


# this tells the server to look out for anyone visiting the main "/" homepage URL path
@app.get("/")
def read_root():
    return {"message": "Welcome to your secure API repository!"}


@app.post("/assets/")
def create_asset(asset: Asset, db: Session = Depends(get_db), current_user: models.DBUser = Depends(get_current_user)):
    # Convert the incoming Pydantic validation data into a Database Model Object
    db_item = models.DBAsset(
        name=asset.name,
        asset_type=asset.asset_type,
        ip_address=asset.ip_address,
        port=asset.port,
    )

    # Add and commit the item to your SQLite database
    db.add(db_item)
    db.commit()
    db.refresh(db_item)  # Grabs the unique ID assigned by the database automatically

    return {
        "status": "Saved successfully",
        "database_id": db_item.id,
        "saved_item": asset,
    }


@app.get("/assets/")
def get_all_assets(db: Session = Depends(get_db), current_user: models.DBUser = Depends(get_current_user)):

    # Query thge database to extract every row inside the assets table
    all_assets = db.query(models.DBAsset).all()

    # Return the records as a JSON list automatically
    return {"total_count": len(all_assets), "assets": all_assets}


@app.get("/assets/{asset_id}")
def get_single_asset(asset_id: int, db: Session = Depends(get_db), current_user: models.DBUser = Depends(get_current_user)):

    # Search for an asset matching the requested ID number
    target_asset = (
        db.query(models.DBAsset).filter(models.DBAsset.id == asset_id).first()
    )

    # Defensive Error Handling: If the item doesn't exist, don't crash-return a proper 404 code
    if not target_asset:
        raise HTTPException(
            status_code=404, detail=f"Asset with ID {asset_id} was not found."
        )

    return target_asset


@app.put("/assets/{asset_id}")
def update_todo(asset_id: int, updated_asset: Asset, db: Session = Depends(get_db), current_user: models.DBUser = Depends(get_current_user)):

    # Search for the asset we want to update
    db_asset = db.query(models.DBAsset).filter(models.DBAsset.id == asset_id).first()

    # Defensive check: If it doesn't exist, return a 404 error
    if not db_asset:
        raise HTTPException(
            status_code=404, detail=f"Asset with ID {asset_id} does not exist."
        )

    # Update the fields safely using a loop
    for key, value in updated_asset.model_dump().items():
        setattr(db_asset, key, value)

    # Commit the changes to your app.db file
    db.commit()
    db.refresh(db_asset)

    return {"status": "Updated successfully!", "updated_item": db_asset}

@app.delete("/assets/{asset_id}")
def delete_asset(asset_id: int, db: Session = Depends(get_db), current_user: models.DBUser = Depends(get_current_user)):

    # Search for the target asset
    db_asset = db.query(models.DBAsset).filter(models.DBAsset.id == asset_id).first()

    # Defensive check: If it's not found, alert the user
    if not db_asset:
        raise HTTPException(status_code=404, detail=f"Asset with ID {asset_id} does not exist.")

    # Delete the item from the session state and save changes
    db.delete(db_asset)
    db.commit()

    return {
        "status": "Removal finalized successfully!",
        "deleted_asset_id": asset_id
    }

class UserCreate(BaseModel):
    username: str
    password: str

@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):

    # Check if the username already exist in the app.db file
    existing_user = db.query(models.DBUser).filter(models.DBUser.username == user.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken.")

    # Hash the text string password securely using native bcrypt via auth.py
    hash_pwd = auth.get_password_hash(user.password)

    # Map variables explicitly to match your exact models.py database columns
    new_user = models.DBUser(username=user.username, hashed_password=hash_pwd)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"status": "User registered successfully!"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # Look up inside the database table
    user = db.query(models.DBUser).filter(models.DBUser.username == form_data.username).first()

    # Verify plain text password matches the cryptographic database hash
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password credentials.")

    # Generate the signed JSON Web Token session window
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}