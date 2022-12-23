import requests
from flask import Flask, jsonify, request
from flask.views import MethodView
from sqlalchemy import Column, Integer, String, DateTime, create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



app = Flask('app')

DSN = 'postgresql://1:1@localhost:5430/flask_db'
engine = create_engine(DSN)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class AdModel(Base):

    __tablename__ = 'ad'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    owner = Column(String, nullable=False)

Base.metadata.create_all(engine)

class AdView(MethodView):

     def post(self):
         json_data = request.json
         with Session() as session:
             new_ad = AdModel(**json_data)
             session.add(new_ad)
             session.commit()
             return jsonify({
                 'status': 'ok',
                 'id': new_ad.id,
                 'title': new_ad.title,
                 'owner': new_ad.owner,
                 'created_at': new_ad.created_at
             })

     def get(self, id_ad):
         with Session() as session:
             ad = session.query(AdModel).filter(AdModel.id == id_ad).first()
             return jsonify({
                 'id': ad.id,
                 'title': ad.title,
                 'created_at': ad.created_at,
                 'description': ad.description,
                 'owner': ad.owner,
             })

     def delete(self, id_ad: str):
         with Session() as session:
             ad = session.query(AdModel).filter(AdModel.id == id_ad).first()
             session.delete(ad)
             session.commit()
             return jsonify({
                 'status': 'success'
             })

app.add_url_rule("/ad/", view_func=AdView.as_view('ad_create'),
                 methods=['POST'])

app.add_url_rule("/ad/<int:id_ad>/", view_func=AdView.as_view('ad_delete'),
                 methods=['DELETE', 'GET'])

app.run()


