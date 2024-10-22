# # app/crud/todo_crud.py
# from sqlmodel import Session ,select
# from app.models.todo_model import Todo, TodoCreate, TodoUpdate

# def create_todo(todo: TodoCreate, session: Session) -> Todo:
#     db_todo = Todo.from_orm(todo)
#     session.add(db_todo)
#     session.commit()
#     session.refresh(db_todo)
#     return db_todo

# def get_todo_by_id(todo_id: int, session: Session) -> Todo:
#     return session.get(Todo, todo_id)

# def get_all_todos(session: Session) -> list[Todo]:
#     return session.exec(select(Todo)).all()

# def update_todo(todo_id: int, todo_update: TodoUpdate, session: Session) -> Todo:
#     db_todo = session.get(Todo, todo_id)
#     if db_todo:
#         for key, value in todo_update.dict(exclude_unset=True).items():
#             setattr(db_todo, key, value)
#         session.add(db_todo)
#         session.commit()
#         session.refresh(db_todo)
#         return db_todo
#     return None

# def delete_todo(todo_id: int, session: Session) -> dict:
#     db_todo = session.get(Todo, todo_id)
#     if db_todo:
#         session.delete(db_todo)
#         session.commit()
#         return {"message": "Todo deleted"}
#     return {"message": "Todo not found"}
