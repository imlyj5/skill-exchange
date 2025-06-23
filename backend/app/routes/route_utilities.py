from flask import abort, make_response
from ..db import db

def validate_model(cls, model_id):
    """
    Validate a model instance by its ID.
    
    Args:
        cls: The model class
        model_id: The ID of the model to validate
    """
    try:
        model_id = int(model_id)
    except:
        response = {"message": f"{cls.__name__} {model_id} invalid"}
        abort(make_response(response , 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)
    
    if not model:
        response = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))
    
    return model

def create_model(cls, model_data, status_code=201, additional_fields=None):
    """
    Create a model instance and save it to database.
    
    Args:
        cls: The model class
        model_data: Dictionary of data to create the model
        status_code: HTTP status code to return
        additional_fields: Dict of additional fields to include in response
    
    Returns:
        Tuple of (response_data, status_code)
    """
    try:
        new_model = cls.from_dict(model_data)
    except KeyError as e:
        response = {"details": f"Invalid data: {str(e)}"}
        abort(make_response(response, 400))
    
    db.session.add(new_model)
    db.session.commit()

    response_data = new_model.to_dict()
    if additional_fields:
        response_data.update(additional_fields)
    
    return response_data, status_code

