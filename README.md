⚡️ Mini Flask API !!! You can Practice API Manual&Automation here

🚀A lightweight Flask + SQLite CRUD API for practicing with Postman and Python (PyCharm).
I created this Project to do everything from scratch: populate DB with data,
and learn how to design my own REST API. I can populate DB with data,
practice API with Postman and Python <requets> module🚀


🛠 Getting Started

✨ Install Flask
python -m pip install flask

▶️ Run the server
This project now supports two separate SQLite databases:
- **manual.db** → used for manual testing (Postman, etc.)
- **automation.db** → used for automated Python tests 

### Run with Manual DB (!don't forget chmod)
./manual.sh

### Run with Automation DB
./automation.sh
- run **python populate_auto_db.py** in other terminal
- run **pytest tests/test_products.py** to run automation tests

✅ Check Data base → run in Postman: http://127.0.0.1:5000/which_db

🌐 Check health in the browser: http://127.0.0.1:5000/health

✅ Expected response → {"status": "ok"} 


📌 Endpoints
➕ POST /products → create a new product
📋 GET /products → check for list all products
🔍 GET /products/<id> → get one product by id
✏️ PATCH /products/<id> → update a product
❌ DELETE /products/<id> → delete a product


🔍 Example Flow
➕ Create a product → POST /products
🔍 Fetch it → GET /products/<id>
✏️ Update it → PATCH /products/<id>
📋 List all → GET /products
❌ Delete it → DELETE /products/<id>

🧹 Resetting the Database

All products are stored in data.db (SQLite).
To reset:
⏹ Stop the server
🗑 Delete Data Base: run -> **rm manual.db** or **rm automation.db** (correspondingly)
▶️ Restart with corresponding script: **./manual.sh** or **./automation.sh**
