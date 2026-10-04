import joblib
import os

from common.audit_logger import log_audit
from config.config import (
    CONFIDENCE_THRESHOLD,
    DEPARTMENT_EMAILS,
    MANUAL_REVIEW_EMAIL,
)


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MODEL_DIR = os.path.join(BASE_DIR, "models")



# Spam Detection Model
spam_model = joblib.load(
    os.path.join(MODEL_DIR, "spam_model.pkl")
)

spam_vectorizer = joblib.load(
    os.path.join(MODEL_DIR, "vectorizer.pkl")
)


# Department Classification
dept_model = joblib.load(
    os.path.join(MODEL_DIR, "department_model.pkl")
)

dept_vectorizer = joblib.load(
    os.path.join(MODEL_DIR, "dept_vectorizer.pkl")
)

label_encoder = joblib.load(
    os.path.join(MODEL_DIR, "dept_label_encoder.pkl")
)


def orchestrate_email(
    sender,
    subject,
    body,
    send_email_func,
    log_func
):

    text = (subject or "") + " " + (body or "")

   

    log_func("Running spam detection...")

    spam_input = spam_vectorizer.transform([text])
    spam_prob = spam_model.predict_proba(spam_input)[0][1]

    log_func(f"Spam probability: {round(spam_prob,3)}")

    if spam_prob >= 0.5:

        log_func("SPAM detected → Blocked")

        log_audit(
            sender=sender,
            subject=subject,
            department="spam",
            confidence=float(spam_prob),
            decision="blocked"
        )

        return


    log_func("Running department classification...")

    dept_input = dept_vectorizer.transform([text])

    dept_pred = dept_model.predict(dept_input)

    department = label_encoder.inverse_transform(
        dept_pred
    )[0].lower()

    # CalibratedClassifierCV gives predict_proba; use max class probability as confidence
    proba = dept_model.predict_proba(dept_input)[0]
    confidence = float(max(proba))

    log_func(f"Department: {department}")
    log_func(f"Confidence: {round(confidence, 3)}")



    if confidence < CONFIDENCE_THRESHOLD:

        receiver = MANUAL_REVIEW_EMAIL
        decision = "manual_review"

    else:

        receiver = DEPARTMENT_EMAILS.get(
            department,
            MANUAL_REVIEW_EMAIL
        )

        decision = "auto_forward"

    log_func(f"Decision: {decision}")
    log_func(f"Forwarding to: {receiver}")


    message_body = f"""
Department: {department}
Confidence: {confidence:.2f}

Original Email:
{text}
"""

    send_email_func(
        receiver,
        f"Forwarded: {subject}",
        message_body
    )


    log_audit(
        sender=sender,
        subject=subject,
        department=department,
        confidence=confidence,
        decision=decision
    )