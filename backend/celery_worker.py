import pickle
from celery import Celery
from database import SessionLocal
from models import User, Messages
from celery.signals import worker_process_init

celery_app = Celery(
    "worker", 
    backend="redis://localhost:6379/0", 
    broker="redis://localhost:6379/0"
)

# Global variables for model & vectorizer
spam_model, vectorizer = None, None

@worker_process_init.connect
def load_model(**kwargs):
    """Load spam detection model and vectorizer when a worker starts."""
    global spam_model, vectorizer
    print("Loading spam model and vectorizer...")

    with open("spam.pkl", "rb") as model_file:
        spam_model = pickle.load(model_file)

    with open("vectorizer.pkl", "rb") as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)

    print("Spam model and vectorizer loaded successfully!")

@celery_app.task
def predict_spam(text: str, user_id: int):
    """Predict if a message is spam or ham and store it in the database."""
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        db.close()
        return {"error": "User not found"}
    
    if spam_model is None or vectorizer is None:
        db.close()
        return {"error": "Model not loaded"}

    message_features = vectorizer.transform([text])
    prediction = spam_model.predict(message_features)
    result = "Spam" if prediction[0] == 1 else "Ham"
    
    # Save prediction result in DB
    db_message = Messages(labels=result, text=text, user_id=user_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    db.close()

    return {"prediction": result}
