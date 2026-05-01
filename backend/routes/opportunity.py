from flask import Blueprint, request, jsonify
from models import Opportunity
from extensions import db
from flask_login import current_user

opp_bp = Blueprint('opportunity', __name__)


# ✅ GET all opportunities
@opp_bp.route('/', methods=['GET'])
def get_opportunities():
    if not current_user.is_authenticated:
        return jsonify([]), 200   # return empty instead of crash

    opps = Opportunity.query.filter_by(admin_id=current_user.id).all()

    return jsonify([
        {
            "id": o.id,
            "name": o.name,
            "description": o.description,
            "category": o.category
        } for o in opps
    ])


# ✅ CREATE opportunity
@opp_bp.route('/', methods=['POST'])
def create_opportunity():
    if not current_user.is_authenticated:
        return jsonify({"error": "Not logged in"}), 401

    data = request.json

    opp = Opportunity(
        name=data['name'],
        duration=data['duration'],
        start_date=data['start_date'],
        description=data['description'],
        skills=data['skills'],
        category=data['category'],
        future_opportunities=data['future_opportunities'],
        max_applicants=data.get('max_applicants'),
        admin_id=current_user.id
    )

    db.session.add(opp)
    db.session.commit()

    return jsonify({"message": "Created"}), 201