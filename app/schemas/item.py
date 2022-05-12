from pydantic import BaseModel


# Shared properties
class ItemBase(BaseModel):
    title: str | None = None
    description: str | None = None


# Properties to receive via API on creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive via API on update
class ItemUpdate(ItemBase):
    pass


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int | None = None
    owner_id: int | None = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Item(ItemInDBBase):
    pass


# Additional properties stored in DB
class ItemInDB(ItemInDBBase):
    pass
