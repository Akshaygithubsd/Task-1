from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from google.cloud import firestore
import os
from dotenv import load_dotenv

# Loading environment variable
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Initializing Firestore client
# setting GOOGLE_APPLICATION_CREDENTIALS environment variable
# we can also use the service account key file path
try:
    db = firestore.Client()
    print("Firestore client initialized successfully")
except Exception as e:
    print(f"Error initializing Firestore: {e}")
    print("Please ensure:")
    print("1. GOOGLE_APPLICATION_CREDENTIALS environment variable is set to your service account key file path")
    print("2. The service account key file exists and is valid")
    print("3. Firestore API is enabled in your Google Cloud project")
    print("4. The Firestore database instance has been created")
    db = None

# Collection name
CUSTOMER_COLLECTION = 'Customer'


@app.route('/')
def index():
    """Home page - displays all customers"""
    try:
        if db is None:
            flash('Firestore is not initialized. Please check your Google Cloud credentials and ensure GOOGLE_APPLICATION_CREDENTIALS is set correctly.', 'error')
            return render_template('index.html', customers=[])
        
        customers_ref = db.collection(CUSTOMER_COLLECTION)
        customers = customers_ref.stream()
        
        customer_list = []
        for customer in customers:
            customer_data = customer.to_dict()
            customer_data['id'] = customer.id
            customer_list.append(customer_data)
        
        return render_template('index.html', customers=customer_list)
    except Exception as e:
        flash(f'Error fetching customers: {str(e)}', 'error')
        return render_template('index.html', customers=[])


@app.route('/add', methods=['GET', 'POST'])
def add_customer():
    """Add a new customer"""
    if request.method == 'POST':
        try:
            if db is None:
                flash('Firestore is not initialized. Please check your Google Cloud credentials and ensure GOOGLE_APPLICATION_CREDENTIALS is set correctly.', 'error')
                return redirect(url_for('add_customer'))
            
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            
            if not name or not email:
                flash('Name and email are required fields', 'error')
                return redirect(url_for('add_customer'))
            
            # Creating customer data
            customer_data = {
                'name': name,
                'email': email,
                'phone': phone if phone else None
            }
            
            # Adding to Firestore
            doc_ref = db.collection(CUSTOMER_COLLECTION).add(customer_data)
            flash('Customer added successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error adding customer: {str(e)}', 'error')
            return redirect(url_for('add_customer'))
    
    return render_template('add_customer.html')


@app.route('/edit/<customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    """Update an existing customer"""
    if request.method == 'POST':
        try:
            if db is None:
                flash('Firestore is not initialized. Please check your Google Cloud credentials and ensure GOOGLE_APPLICATION_CREDENTIALS is set correctly.', 'error')
                return redirect(url_for('edit_customer', customer_id=customer_id))
            
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            
            if not name or not email:
                flash('Name and email are required fields', 'error')
                return redirect(url_for('edit_customer', customer_id=customer_id))
            
            # Updating customer data
            customer_data = {
                'name': name,
                'email': email,
                'phone': phone if phone else None
            }
            
            db.collection(CUSTOMER_COLLECTION).document(customer_id).update(customer_data)
            flash('Customer updated successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error updating customer: {str(e)}', 'error')
            return redirect(url_for('edit_customer', customer_id=customer_id))
    
    # GET request - fetching customer data
    try:
        if db is None:
            flash('Firestore is not initialized. Please check your Google Cloud credentials and ensure GOOGLE_APPLICATION_CREDENTIALS is set correctly.', 'error')
            return redirect(url_for('index'))
        
        customer_doc = db.collection(CUSTOMER_COLLECTION).document(customer_id).get()
        if customer_doc.exists:
            customer_data = customer_doc.to_dict()
            customer_data['id'] = customer_doc.id
            return render_template('edit_customer.html', customer=customer_data)
        else:
            flash('Customer not found', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error fetching customer: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/delete/<customer_id>', methods=['POST'])
def delete_customer(customer_id):
    """Delete a customer"""
    try:
        if db is None:
            flash('Firestore is not initialized. Please check your Google Cloud credentials and ensure GOOGLE_APPLICATION_CREDENTIALS is set correctly.', 'error')
            return redirect(url_for('index'))
        
        db.collection(CUSTOMER_COLLECTION).document(customer_id).delete()
        flash('Customer deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting customer: {str(e)}', 'error')
    
    return redirect(url_for('index'))


@app.route('/search', methods=['GET', 'POST'])
def search_customers():
    """Search customers by name or email"""
    if request.method == 'POST':
        try:
            if db is None:
                flash('Firestore is not initialized. Please check your Google Cloud credentials and ensure GOOGLE_APPLICATION_CREDENTIALS is set correctly.', 'error')
                return redirect(url_for('index'))
            
            search_term = request.form.get('search_term', '').strip()
            search_type = request.form.get('search_type', 'name')
            
            if not search_term:
                flash('Please enter a search term', 'error')
                return redirect(url_for('index'))
            
            customers_ref = db.collection(CUSTOMER_COLLECTION)
            
            # Firestore query based on type of search
            if search_type == 'name':
                query = customers_ref.where('name', '>=', search_term).where('name', '<=', search_term + '\uf8ff')
            elif search_type == 'email':
                query = customers_ref.where('email', '>=', search_term).where('email', '<=', search_term + '\uf8ff')
            else:
                query = customers_ref
            
            customers = query.stream()
            
            customer_list = []
            for customer in customers:
                customer_data = customer.to_dict()
                customer_data['id'] = customer.id
                customer_list.append(customer_data)
            
            return render_template('index.html', customers=customer_list, search_term=search_term, search_type=search_type)
        except Exception as e:
            flash(f'Error searching customers: {str(e)}', 'error')
            return redirect(url_for('index'))
    
    return redirect(url_for('index'))


# API endpoints for accessing the data
@app.route('/api/customers', methods=['GET'])
def api_get_customers():
    """API endpoint to get all customers"""
    try:
        if db is None:
            return jsonify({'success': False, 'error': 'Firestore is not initialized. Please check your Google Cloud credentials and ensure GOOGLE_APPLICATION_CREDENTIALS is set correctly.'}), 500
        
        customers_ref = db.collection(CUSTOMER_COLLECTION)
        customers = customers_ref.stream()
        
        customer_list = []
        for customer in customers:
            customer_data = customer.to_dict()
            customer_data['id'] = customer.id
            customer_list.append(customer_data)
        
        return jsonify({'success': True, 'customers': customer_list})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/customers', methods=['POST'])
def api_create_customer():
    """API endpoint to create a new customer"""
    try:
        if db is None:
            return jsonify({'success': False, 'error': 'Firestore is not initialized. Please check your Google Cloud credentials and ensure GOOGLE_APPLICATION_CREDENTIALS is set correctly.'}), 500
        
        data = request.get_json()
        
        if not data or not data.get('name') or not data.get('email'):
            return jsonify({'success': False, 'error': 'Name and email are required'}), 400
        
        customer_data = {
            'name': data.get('name'),
            'email': data.get('email'),
            'phone': data.get('phone')
        }
        
        doc_ref = db.collection(CUSTOMER_COLLECTION).add(customer_data)
        return jsonify({'success': True, 'id': doc_ref[1].id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/customers/<customer_id>', methods=['PUT'])
def api_update_customer(customer_id):
    """API endpoint to update a customer"""
    try:
        if db is None:
            return jsonify({'success': False, 'error': 'Firestore is not initialized. Please check your Google Cloud credentials and ensure GOOGLE_APPLICATION_CREDENTIALS is set correctly.'}), 500
        
        data = request.get_json()
        
        if not data or not data.get('name') or not data.get('email'):
            return jsonify({'success': False, 'error': 'Name and email are required'}), 400
        
        customer_data = {
            'name': data.get('name'),
            'email': data.get('email'),
            'phone': data.get('phone')
        }
        
        db.collection(CUSTOMER_COLLECTION).document(customer_id).update(customer_data)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/customers/<customer_id>', methods=['DELETE'])
def api_delete_customer(customer_id):
    """API endpoint to delete a customer"""
    try:
        if db is None:
            return jsonify({'success': False, 'error': 'Firestore is not initialized. Please check your Google Cloud credentials and ensure GOOGLE_APPLICATION_CREDENTIALS is set correctly.'}), 500
        
        db.collection(CUSTOMER_COLLECTION).document(customer_id).delete()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

